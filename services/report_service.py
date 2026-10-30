from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether
)


def generate_text_report(data):
    """Convert structured meeting data into a readable text report."""

    lines = ["AI Meeting Intelligence - MEETING REPORT", "=" * 40]

    lines.extend([
        "",
        "MEETING SUMMARY",
        data.get("summary", "No summary available."),
        ""
    ])

    for heading, key in [
        ("DISCUSSION POINTS", "discussion_points"),
        ("KEY DECISIONS", "decisions"),
        ("OPEN QUESTIONS", "open_questions")
    ]:
        lines.append(heading)

        items = data.get(key, [])

        if items:
            for index, item in enumerate(items, 1):
                lines.append(f"{index}. {item}")
        else:
            lines.append("None identified.")

        lines.append("")

    lines.append("ACTION ITEMS")

    actions = data.get("action_items", [])

    if actions:
        for index, item in enumerate(actions, 1):
            lines.append(
                f"{index}. {item['task']}\n"
                f"   Owner: {item['person']}\n"
                f"   Deadline: {item['deadline']}"
            )
    else:
        lines.append("No confirmed action items.")

    lines.append("")
    lines.append("ADDITIONAL INSIGHTS")

    insights = data.get("additional_insights", [])

    if insights:
        for index, item in enumerate(insights, 1):
            lines.extend([
                f"{index}. {item['category']}",
                f"   Details: {item['details']}",
                f"   Status: {item['status']}",
                f"   Evidence: {item['evidence']}",
                ""
            ])
    else:
        lines.append("None identified.")

    return "\n".join(lines)


def generate_pdf_report(data):
    """Generate a professional meeting report as PDF bytes."""

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=(595.28, 841.89),  # A4
        rightMargin=42,
        leftMargin=42,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontSize=20,
        leading=26,
        textColor=colors.HexColor("#183153"),
        alignment=TA_CENTER,
        spaceAfter=20
    ))

    styles.add(ParagraphStyle(
        name="SectionTitleCustom",
        parent=styles["Heading2"],
        fontSize=12,
        leading=17,
        textColor=colors.HexColor("#2563EB"),
        spaceBefore=18,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="ReportBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=15,
        spaceAfter=6
    ))

    story = []

    def add_section(title):
        story.append(
            Paragraph(title, styles["SectionTitleCustom"])
        )

    def add_text(value):
        safe_text = escape(str(value))
        story.append(
            Paragraph(safe_text, styles["ReportBody"])
        )

    def add_list_section(title, items):
        add_section(title)

        if not items:
            add_text("None identified.")
            return

        for index, item in enumerate(items, 1):
            add_text(f"{index}. {item}")

    # Report title
    story.append(
        Paragraph(
            "AI Meeting Intelligence",
            styles["ReportTitle"]
        )
    )

    story.append(
        Paragraph(
            "Meeting Intelligence Report",
            styles["ReportBody"]
        )
    )

    # Summary
    add_section("Meeting Summary")
    add_text(data.get("summary") or "No summary available.")

    # Discussion points
    add_list_section(
        "Discussion Points",
        data.get("discussion_points", [])
    )

    # Decisions
    add_list_section(
        "Key Decisions",
        data.get("decisions", [])
    )

    # Action items
    add_section("Action Items")

    actions = data.get("action_items", [])

    if actions:
        table_data = [[
            Paragraph("Task", styles["ReportBody"]),
            Paragraph("Owner", styles["ReportBody"]),
            Paragraph("Deadline", styles["ReportBody"])
        ]]

        for item in actions:
            table_data.append([
                Paragraph(
                    escape(item["task"]),
                    styles["ReportBody"]
                ),
                Paragraph(
                    escape(item["person"]),
                    styles["ReportBody"]
                ),
                Paragraph(
                    escape(item["deadline"]),
                    styles["ReportBody"]
                )
            ])

        table = Table(
            table_data,
            colWidths=[280, 100, 130],
            repeatRows=1,
            hAlign="LEFT"
        )

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#E8F0FE")),
            ("GRID", (0, 0), (-1, -1),
             0.3, colors.HexColor("#D5DDE8")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
        ]))

        story.append(table)
    else:
        add_text("No confirmed action items.")

    # Additional insights
    add_section("Additional Meeting Insights")

    insights = data.get("additional_insights", [])

    if insights:
        for item in insights:
            insight_block = [
                Paragraph(
                    escape(item["category"]),
                    styles["Heading3"]
                ),
                Paragraph(
                    escape(item["details"]),
                    styles["ReportBody"]
                ),
                Paragraph(
                    "Status: " + escape(item["status"]),
                    styles["ReportBody"]
                ),
                Paragraph(
                    "Evidence: " + escape(item["evidence"]),
                    styles["ReportBody"]
                ),
                Spacer(1, 8)
            ]

            story.append(KeepTogether(insight_block))
    else:
        add_text("None identified.")

    # Open questions
    add_list_section(
        "Open Questions",
        data.get("open_questions", [])
    )

    # Build PDF
    doc.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
