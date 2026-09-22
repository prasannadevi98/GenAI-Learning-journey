import json
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Preformatted

notebook_path = Path(r"d:\GenAI-Learning-journey\task -1,python basic ,operators ,if and else,loops.ipynb")
output_pdf = notebook_path.with_suffix(".pdf")

def clean_text(text: str) -> str:
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text

def add_cell(story, cell, styles):
    source = "".join(cell.get("source", []))
    if not source.strip():
        return

    if cell.get("cell_type") == "markdown":
        text = clean_text(source)
        paragraph = Paragraph(text.replace("\n", "<br/>"), styles["BodyText"])
        story.append(paragraph)
    else:
        code = clean_text(source)
        story.append(Spacer(1, 0.15 * inch))
        story.append(Preformatted(code, styles["Code"]))  # simple code block style

    story.append(Spacer(1, 0.2 * inch))

def main():
    with notebook_path.open("r", encoding="utf-8") as f:
        notebook = json.load(f)

    doc = SimpleDocTemplate(
        str(output_pdf),
        pagesize=A4,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch
    )

    styles = getSampleStyleSheet()
    styles["BodyText"].fontName = "Helvetica"
    styles["BodyText"].fontSize = 11
    styles["BodyText"].leading = 15

    styles["Code"].fontName = "Courier"
    styles["Code"].fontSize = 9
    styles["Code"].leading = 12
    styles["Code"].backColor = "#f5f5f5"

    story = []
    story.append(Paragraph("Python Basics, Operators, If/Else, Loops", styles["Title"]))
    story.append(Spacer(1, 0.3 * inch))

    for cell in notebook.get("cells", []):
        add_cell(story, cell, styles)

    doc.build(story)
    print(f"PDF created: {output_pdf}")

if __name__ == "__main__":
    main()