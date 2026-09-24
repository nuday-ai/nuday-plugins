---
name: nuday-app-building
description: Build, deploy, and operate NuDay apps (static sites, Streamlit, FastAPI,
  Flask, Node, hosted MCP servers, Postgres-backed apps) whose source lives in a tenant
  workspace. Use when a user wants to create, publish, update, debug, or roll back
  a deployed web app via the NuDay Apps, Workspace Files, and Web Tools MCP servers.
metadata:
  source: nuday
  catalog: platform
  category: app-building
  priority: '5'
---

# NuDay App Building

## Overview
This skill guides you through building and operating **apps** on the NuDay
platform — small web workloads that run per-tenant behind a per-app ingress
(`https://<app-id>.apps.<domain>/`) with SSO. App source files live in a
**workspace** (S3-backed); the platform tars them and runs them as a
Kubernetes workload. You never touch Kubernetes directly.

You have three MCP servers:

- **Workspace Files** — author the app's source files.
  `list_workspaces`, `list_files`, `read_file`, `grep`, `write_file`,
  `edit_file`, `create_folder`, `move_file`, `delete_file`.
- **NuDay Apps** — create, configure, publish, and operate the app. Every
  tool name carries the `nuday_` prefix:
  `nuday_list_apps`, `nuday_get_app`, `nuday_scaffold_app`,
  `nuday_create_app`, `nuday_update_app`, `nuday_delete_app`,
  `nuday_publish_app`, `nuday_unpublish_app`, `nuday_deploy_app`,
  `nuday_stop_app`, `nuday_get_app_status`, `nuday_get_app_logs`,
  `nuday_list_app_secret_keys`, `nuday_set_app_secret`,
  `nuday_delete_app_secret`, `nuday_list_app_versions`,
  `nuday_get_app_version`, `nuday_rollback_app_version`.
- **Web Tools** — research docs, libraries, and examples while building.
  `web_search`, `web_fetch`.

## Runtimes

| runtime       | manifest                          | entrypoint       | started as                       |
|---------------|-----------------------------------|------------------|----------------------------------|
| `static`      | —                                 | — (`index.html`) | nginx, served as-is              |
| `python-asgi` | requirements.txt / pyproject.toml | `main:app`       | uvicorn (FastAPI, Starlette)     |
| `python-wsgi` | requirements.txt / pyproject.toml | `app:app`        | gunicorn (Flask)                 |
| `streamlit`   | requirements.txt                  | `app.py`         | streamlit run                    |
| `node`        | package.json                      | `server.js`      | node (or npm start)              |

`nuday_scaffold_app` also knows two **starters** that deploy as `python-asgi`:
`mcp` (a hosted MCP server with bearer validation — needs a service
principal, pass `service_principal_id: "__new__"`) and `python-postgres`
(a team-notes app on the per-app Postgres that already implements the
multi-user pattern — identity from the headers, `principals` +
`user_settings` tables, per-user settings routes, owner-or-admin delete —
its returned config includes `release_command` and a `datastores` entry;
the app exits at start without that datastore, so pass both through
unchanged). Scaffold it when the app needs per-user data and build on it;
the pattern itself is explained in [[nuday-app-multi-user]].

**Every dynamic runtime MUST bind `0.0.0.0:$PORT`** (read `process.env.PORT`
/ let the launcher pass `$PORT`). The app filesystem is **ephemeral** —
wiped on every restart. Keep state in the app's own Postgres **datastore**
(below) or an external service reached over HTTPS; the pod can only egress
to the internet on 80/443 plus its own datastore on 5432.

## Before you build — confirm with the user
Confirm these once, in a single short message, before writing any file.
If the user says **skip the checklist**, or the request already answers
every item, do not ask — proceed with sensible defaults and state the
assumptions you made in your first reply.

1. **Name + workspace** — app name (unique per tenancy) and tenant vs
   personal workspace.
2. **Runtime** — runtime, `manifest_path`, `entrypoint` (or `command`),
   and that the server binds `0.0.0.0:$PORT`.
3. **Source path** — a subfolder such as `apps/<name>`, never the
   workspace root.
4. **Data** — does anything need to survive a restart? If yes: the
   Postgres `datastores` block plus an idempotent `release_command` that
   creates/migrates tables. No datastore means every restart starts empty.
5. **Users** — more than one signed-in person, per-user settings, "who did
   this", or admin-only actions? Then follow [[nuday-app-multi-user]]
   (identity headers, `principals` + `user_settings` tables, roles).
6. **Secrets** — the `env_refs` names the code reads; collect the values
   and set them with `nuday_set_app_secret` before publishing.
7. **Background work** — in-process cron, queues or websockets need
   `scale_to_zero: false`, `replicas: 1` (or a lease table for more), and
   must tolerate being restarted at any time.
8. **Build** — a `build_command` runs inside the pod on every start; keep
   it light (no `tsc` type-checks; transpile only) and ask for memory when
   it is heavy.
9. **Health** — `health_path` (default `/`) must answer 2xx/3xx with no
   login and no database dependency at boot.
10. **Done means** — `nuday_get_app_status` reports `running`, the live
    URL is in your final message, and you tell the user how to iterate
    (edit files → `nuday_deploy_app`).

## Workflow

### 1. Choose a workspace
Call `list_workspaces`. Use the **tenant** workspace for team apps (visible to
the tenancy); use a **personal** workspace for private apps. Note its
`workspace_id`. Tenancy is derived from that workspace, so no `X-Tenant-Id`
header is needed; if a call asks for one, `nuday_whoami` gives your
`principal_kind` (`single_tenancy`/`tenant_pinned`: never pass `tenant_id`;
`multi_tenancy`/`platform_admin`: pass it, finding ids with
`nuday_tenancies_list(query=…)`).

### 2. Check for an existing app
Call `nuday_list_apps` (optionally with `query`). App names are unique per
tenancy and re-creating one is rejected — if it exists, change it with
`nuday_update_app` and skip to step 6.

### 3. Lay down the source
Apps always live in a **subfolder** of the workspace (e.g. `apps/my-app`),
never at its root. Two options:
- **Scaffold** a runnable starter: `nuday_scaffold_app` with `workspace_id`,
  `source_path` (e.g. `apps/my-app`), and `runtime`. It writes the starter
  files and returns the recommended create config (`runtime`,
  `manifest_path`, `entrypoint`, `port`, plus any of `mcp_enabled`,
  `mcp_path`, `scale_to_zero`, `replicas`, `release_command`, `datastores`,
  `health_path`).
- **Author by hand** with `write_file` / `edit_file` under `source_path`
  (e.g. `apps/my-app/main.py`, `apps/my-app/requirements.txt`). Use
  `read_file`/`grep` to inspect existing files before editing, and
  `web_search` + `web_fetch` to pull current framework docs. Python
  dependencies must have prebuilt wheels (no compilers in the image).
- **File economy.** Every file costs one `write_file` call: prefer a
  handful of complete files (one server module, one static `index.html`
  + `app.js`, one `release.py`/`release.js`, the manifest) over many small
  ones, write each file once in full, then `edit_file` to fix — never
  re-write a whole file to change a line.

### 4. Create the app
Call `nuday_create_app` (pass the scaffold's returned config verbatim):
```json
{
  "name": "my-app",
  "workspace_id": "<workspace_id>",
  "source_path": "apps/my-app",
  "runtime": "python-asgi",
  "manifest_path": "requirements.txt",
  "entrypoint": "main:app",
  "port": 8080,
  "env_refs": ["API_KEY"],
  "replicas": 1
}
```
Other fields: `command` (explicit start command, overrides the runtime's),
`scale_to_zero` (default true: sleeps after ~1h idle, a visit wakes it),
`build_command` (e.g. `npm run build`, runs after dependency install on
every pod start), `release_command` (e.g. `python release.py` or
`npx prisma migrate deploy`, runs before start on every pod start — keep it
idempotent), `mcp_enabled` + `mcp_path` + `service_principal_id` for a
hosted MCP server, `health_path` (readiness probe; default `/`), and
`datastores`. Keep `replicas: 1` unless the app is stateless and holds no
in-process timers — cron/queues on 2+ replicas double-fire without a lease
table — and set `scale_to_zero: false` whenever background work must keep
running while nobody visits.

**Datastore (per-app Postgres).** Pass
`"datastores": [{"kind": "postgres", "name": "db", "env": "DATABASE_URL",
"storage": "5Gi", "extensions": []}]` and the platform provisions a small
Postgres in the tenancy and injects its connection string as
`DATABASE_URL` (a reserved name — never set it as a secret). Optional
`extensions`: `vector`, `pgcrypto`, `uuid-ossp`, `pg_trgm`, `citext`.
Create your tables in an idempotent `release_command`. The datastore is
**deleted with the app** and has no backups in this version; storage can
grow but not shrink; `datastores: []` on update removes it (and its data).

The app starts as a **draft** (preview only).

### 5. Set secrets (if any)
For each name in `env_refs`, call `nuday_set_app_secret` (`key` + `value`).
Values are encrypted and injected as env vars at deploy time; they are never
returned. Verify with `nuday_list_app_secret_keys`. Set secrets **before**
publishing so the first deploy has them.

### 6. Publish
Call `nuday_publish_app`. For `static` apps this requires `index.html` at
the source path. Then poll `nuday_get_app_status` until `deploy_status` is
`running` (or `deploy_failed`); it moves `none` → `deploying` → `running`
(`degraded` = some replicas unready) and also reports `ready`/`desired`
counts, a `reason`, and `needs_redeploy`. The readiness probe hits
`health_path` (default `/`, must answer 2xx/3xx); a deploy that never
becomes ready reports the failing probe / restarts in `reason` and moves to
`deploy_failed` once the Deployment gives up. On success the app is live at its
`ingress_host`. All deploy tools work for every runtime, static included.

### 7. Iterate + debug
- Change source with `write_file`/`edit_file`, then `nuday_deploy_app`
  (re-stage + redeploy) or `nuday_publish_app`.
- Change config (runtime, port, env_refs, replicas, commands, datastore)
  with `nuday_update_app`, then `nuday_deploy_app` to roll it out.
- Tail `nuday_get_app_logs` to debug a crash loop or `deploy_failed` —
  failed dependency installs and release commands show up there.
- The only way to run an app is to publish it: do not try to execute its
  source with a code sandbox or a local shell (the sandbox is often not
  configured, and the app's Postgres and identity headers only exist in
  the deployed pod). Review the code, publish, read the status and logs.
- Before `edit_file`, `read_file` the current content — the `find` text
  must match exactly, and your earlier draft may not be what is on disk.
- A hosted MCP app reporting "no service principal assigned": call
  `nuday_update_app` with `service_principal_id: "__new__"` and redeploy.
- `nuday_unpublish_app` / `nuday_stop_app` scale the workload to zero.

### 8. Versions + rollback
Each publish snapshots a version. Use `nuday_list_app_versions`,
`nuday_get_app_version`, and `nuday_rollback_app_version` to revert a bad
deploy.

## Best practices
- Bind `0.0.0.0:$PORT`; never hardcode a port or `localhost`.
- Never rely on the local filesystem for state; use a datastore or an
  external service.
- Reference secrets via `env_refs` + `nuday_set_app_secret` — never inline
  credentials in source files.
- Scaffold first when unsure of a runtime's layout, then customize.
- The platform login sits in front of every app; read the signed-in user
  from the `X-Forwarded-User` / `X-Forwarded-Preferred-Username` /
  `X-Forwarded-Groups` request headers instead of implementing auth (never
  `X-Auth-Request-*` — those are response headers the app never sees).
  Per-user tables, roles and rosters: [[nuday-app-multi-user]].
- `DATABASE_URL` is injected by the datastore — never set it as a secret
  and never hardcode a database host.
- After publishing, always confirm `nuday_get_app_status` reached `running`
  and report the live URL to the user.
- Use `web_search`/`web_fetch` to ground framework choices in current docs.
