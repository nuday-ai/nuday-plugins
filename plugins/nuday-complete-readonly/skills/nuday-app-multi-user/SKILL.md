---
name: nuday-app-multi-user
description: Support multiple signed-in users in a NuDay app — read the current user
  from the platform's identity headers, derive admin/member roles, add the per-app
  Postgres datastore, and model per-user settings and ownership. Use when an app needs
  "who did this", per-user preferences, admin-only actions, or any data shared by
  a team.
metadata:
  source: nuday
  catalog: platform
  category: app-building
  priority: '6'
---

# Multi-user NuDay Apps

## When to use
Any app where more than one person signs in and reads or writes data:
team CRMs, trackers, dashboards with per-user preferences, anything with
"created by", "assigned to", or admin-only actions. This skill covers
**identity, roles, and the data model**. Creating, publishing and
operating the app itself is [[nuday-app-building]] — follow its workflow
and pull the pieces below into the files you write.

## 1. Identity comes from headers — never build a login
The platform's login proxy sits in front of every app and forwards the
signed-in user on **every request** as trusted headers. The app has no
accounts, no password table, no session store.

| header | value | use it for |
|---|---|---|
| `X-Forwarded-User` | OIDC `sub` — a stable opaque GUID | **the key for everything per-user** |
| `X-Forwarded-Preferred-Username` | the user's email (may be empty) | display + admin allowlist |
| `X-Forwarded-Groups` | comma-separated: `entity_<app_id>_can_view` / `_can_use` / `_can_manage`, `tenant_<tenant_id>`, `platform_admin` | roles |
| `X-Forwarded-Email` | **also the sub** (deliberate) | nothing — do not treat as an email |

Rules:
- Key rows on the **sub**, never the email (emails change; the sub does not).
- The similarly named `X-Auth-Request-*` headers are set on the proxy's
  *responses* and are **not visible to the app** — reading them makes
  every request look anonymous (the first CRM deploy 401'd on every call
  for exactly this reason).
- The proxy strips client-supplied copies, so the headers are trustworthy
  inside the pod. Outside the platform (local dev) there is no proxy: fall
  back to `DEV_SSO_SUB` / `DEV_SSO_EMAIL` / `DEV_SSO_GROUPS` env vars **only
  when not in production**; in production a missing sub is a 401.
- Sign-out link: `/oauth2/sign_out`. Sign-in: `/oauth2/start?rd=<path>`.
  The browser client should redirect to sign-in on a 401 and remember it
  did (a `sessionStorage` timestamp) so a broken identity cannot loop.

## 2. Roles from groups
Keep it tiny — two roles are enough for almost every app:
- **ADMIN** when groups contain `platform_admin` or any group ending in
  `_can_manage`, or the email is in the `APP_ADMIN_EMAILS` secret
  (comma-separated, case-insensitive; declare it in `env_refs`).
- **MEMBER** for everyone else the proxy let through.

One helper builds the principal; one guard protects admin routes.

Python (FastAPI):
```python
import os
from fastapi import Depends, HTTPException, Request

PROD = os.environ.get("NODE_ENV") == "production" or bool(os.environ.get("AGENT_VAULT_APP_URL"))
ADMIN_EMAILS = {e.strip().lower() for e in os.environ.get("APP_ADMIN_EMAILS", "").split(",") if e.strip()}

def current_principal(request: Request) -> dict:
    h = request.headers
    sub = h.get("x-forwarded-user")
    email = (h.get("x-forwarded-preferred-username") or "").lower()
    groups = [g.strip() for g in (h.get("x-forwarded-groups") or "").split(",") if g.strip()]
    if not sub:
        if PROD:
            raise HTTPException(401, "not signed in")
        sub = os.environ.get("DEV_SSO_SUB", "dev-local")
        email = os.environ.get("DEV_SSO_EMAIL", "dev@localhost")
        groups = os.environ.get("DEV_SSO_GROUPS", "dev_can_manage").split(",")
    is_admin = email in ADMIN_EMAILS or any(g == "platform_admin" or g.endswith("_can_manage") for g in groups)
    return {"sub": sub, "email": email, "groups": groups, "is_admin": is_admin}

def require_admin(p: dict = Depends(current_principal)) -> dict:
    if not p["is_admin"]:
        raise HTTPException(403, "admin only")
    return p
```

Node (Express) — same shape: read `req.headers["x-forwarded-user"]`,
`["x-forwarded-preferred-username"]`, `["x-forwarded-groups"]`, attach
`req.principal`, 401 in production when the sub is missing, and an
`adminOnly` middleware that 403s.

## 3. Adding Postgres to the app
Persistent data lives in the app's own datastore (the filesystem is wiped
on every restart). In `nuday_create_app` / `nuday_update_app`:
```json
"datastores": [{"kind": "postgres", "name": "db", "env": "DATABASE_URL",
                "storage": "5Gi", "extensions": []}],
"release_command": "python release.py"
```
- The platform injects `DATABASE_URL` (`postgresql://…?sslmode=disable`).
  It is reserved: never set it as a secret, never add `?schema=` to it.
- `release_command` runs **before start on every pod start** — it must be
  idempotent. Simplest: a `release.py` / `release.js` with
  `CREATE TABLE IF NOT EXISTS …` statements (plus `CREATE INDEX IF NOT
  EXISTS`); for evolving schemas keep a `schema_migrations(version)` table
  and apply numbered SQL files not yet recorded. Node + Prisma: `npx
  prisma migrate deploy`.
- Use one small connection pool per process (`psycopg_pool` / `pg.Pool`);
  Python drivers need prebuilt wheels — `psycopg[binary]`.
- Optional `extensions`: `vector`, `pgcrypto`, `uuid-ossp`, `pg_trgm`,
  `citext` (applied at first init only).
- No backups in this version and the database is deleted with the app —
  say so to the user when the data matters.

## 4. Schema pattern for many users
Three tables plus one rule, in the release script:
```sql
CREATE TABLE IF NOT EXISTS principals (
  sub           TEXT PRIMARY KEY,
  email         TEXT,
  name          TEXT,
  groups        TEXT[] NOT NULL DEFAULT '{}',
  first_seen_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_seen_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS user_settings (
  sub          TEXT PRIMARY KEY REFERENCES principals(sub) ON DELETE CASCADE,
  display_name TEXT,
  prefs        JSONB NOT NULL DEFAULT '{}',
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);
-- every user-owned table:
--   created_by_sub TEXT NOT NULL, owner_sub TEXT NOT NULL, assigned_to_sub TEXT
--   + CREATE INDEX IF NOT EXISTS <table>_owner_idx ON <table>(owner_sub);
```
- **principals** is the app's own "who has been here" cache: upsert
  `(sub, email, name, groups, last_seen_at)` on each request, throttled
  in memory to once per sub per ~5 minutes.
- **user_settings** holds per-user preferences (display name, pinned
  items, theme…). Expose them at the app's own `/me` and `/me/settings`
  routes (GET + PATCH) that read the sub from the header — **never accept
  a `sub` from the request body or query string**.
- **Ownership columns** store the **sub**. "My items" = `WHERE owner_sub
  = <header sub>`; admins bypass the filter. Team apps (CRM, tracker)
  default to everyone-can-read, owner-or-admin-can-delete.
- Do not create a `users` table with passwords or roles — identity and
  membership are the platform's; the app only mirrors what it has seen.

## 5. Showing other users' names
Rows hold subs; the UI wants names. Two manager endpoints do this, both
called with the app's **service-principal token** (the platform injects
`AGENT_VAULT_API_TOKEN`, `AGENT_VAULT_MANAGER_URL`, `AGENT_VAULT_TENANT_ID`
once the app has an identity):
- `POST /api/users/resolve` with `{"user_ids": ["<sub>", …]}` →
  `emails`, `names`, `avatars` keyed by sub. Cache in memory ~10 minutes.
- `GET /api/users?tenant_id=$AGENT_VAULT_TENANT_ID` → the tenant roster
  for assignee pickers (needs the `users:list` permission on the SP).
Get the identity by passing `service_principal_id: "__new__"` to
`nuday_create_app` / `nuday_update_app`, then tell the user that a tenancy
admin must bind a role granting `users:list` to that service principal
(Service Principals page → Roles). Until then, fall back to the
`principals` table for names and to "unknown user" for subs never seen.

## Checklist for a multi-user app
- [ ] Identity read from `X-Forwarded-User` (+ username, groups); 401 in
      production when missing; dev shim only outside production.
- [ ] `APP_ADMIN_EMAILS` in `env_refs` and set with `nuday_set_app_secret`
      (or roles from groups only — say which).
- [ ] Datastore block + idempotent `release_command`; `DATABASE_URL` not
      a secret.
- [ ] `principals` + `user_settings` tables; ownership columns hold subs.
- [ ] `/me` route returns sub, email, name, role, settings, and the
      sign-out link so the UI can show who is signed in.
- [ ] Admin-only routes guarded server-side (not just hidden in the UI).

## Pitfalls
- Reading `X-Auth-Request-*` → every request anonymous.
- Treating `X-Forwarded-Email` as an email → it is the sub.
- Keying on email → breaks when the address changes; use the sub.
- A release script that fails the second time it runs (plain
  `CREATE TABLE`) → crash loop on every restart.
- Persisting connector or manager tokens in the database → never; keep
  them in memory until they expire.
- Setting `DATABASE_URL` as an app secret → the platform value wins and
  the secret is rejected as reserved.
