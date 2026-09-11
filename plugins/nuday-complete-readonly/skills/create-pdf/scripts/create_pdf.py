#!/usr/bin/env python3
"""PDF generation helper using ReportLab."""
import argparse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch


class PDFBuilder:
    """Simple PDF document builder."""

    def __init__(self, filename, title="Document", pagesize=letter):
        self.filename = filename
        self.title = title
        self.doc = SimpleDocTemplate(filename, pagesize=pagesize,
                                     topMargin=0.75*inch, bottomMargin=0.75*inch,
                                     leftMargin=0.75*inch, rightMargin=0.75*inch)
        self.styles = getSampleStyleSheet()
        self.story = []

    def add_heading(self, text, level=1):
        style_name = {1: "Heading1", 2: "Heading2", 3: "Heading3"}.get(level, "Heading1")
        self.story.append(Paragraph(text, self.styles[style_name]))
        self.story.append(Spacer(1, 12))

    def add_paragraph(self, text):
        self.story.append(Paragraph(text, self.styles["BodyText"]))
        self.story.append(Spacer(1, 8))

    def add_table(self, data):
        """data: list of lists. First row is treated as header."""
        t = Table(data)
        style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ])
        t.setStyle(style)
        self.story.append(t)
        self.story.append(Spacer(1, 12))

    def add_page_break(self):
        self.story.append(PageBreak())

    def save(self):
        self.doc.build(self.story)
        return self.filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a PDF document")
    parser.add_argument("--output", default="output.pdf", help="Output PDF path")
    parser.add_argument("--title", default="Document", help="Document title")
    args = parser.parse_args()

    pdf = PDFBuilder(args.output, title=args.title)
    pdf.add_heading(args.title)
    pdf.add_paragraph("This is a generated document. Add content programmatically using PDFBuilder.")
    pdf.save()
    print(f"PDF saved to {args.output}")
