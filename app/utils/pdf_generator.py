import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER

def generate_interviewer_brief_pdf(
        candidate_name: str,
        role_title:str,
        brief_text: str
) -> str:
    os.makedirs("outputs",exist_ok=True)

    timestamp= datetime.now().strftime("%Y%m%d_%H%M%S")
    filename=f"outputs/brief_{candidate_name.replace(' ','_')}_{timestamp}.pdf"

    doc=SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )
    styles=getSampleStyleSheet()

    title_style= ParagraphStyle(
        "title",
        parent= styles["Heading1"],
        fontSize=18,
        textColor=colors.HexColor  ("#1a1a2e"),
        spaceAfter=4,
        alignment=TA_CENTER                          
    )

    subtitle_style= ParagraphStyle(
        "substitle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#555555"),
        spaceAfter=12,
        alignment= TA_CENTER
    )

    heading_style=ParagraphStyle(
        "heading",
        parent=styles["Heading2"],
        fontsize=13,
        textColor=colors.HexColor("#16213e"),
        spaceBefore=14,
        spaceAfter=4
    )
    body_style= ParagraphStyle(
        "body",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#333333"),
        spaceAfter=6,
        leading=16

    )

    elements=[]

    elements.append(Paragraph("Interviewer Brief", title_style))
    elements.append(Paragraph (f"{candidate_name} - {role_title}", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
    elements.append(Spacer(1,8))

    generated_on= datetime.now().strftime("%B %d, %Y at %I:%M %p")
    elements.append(Paragraph(f"Generated on: {generated_on}", body_style))
    elements.append(Spacer(1,12))

    for line in brief_text.split("\n"):
        line=line.strip()
        if not line:
            elements.append(Spacer(1,4))
        elif line.startswith("**") and line.endswith("**"):
            elements.append(Paragraph(line.replace("**", ""), heading_style))
        elif line.startswith("###"):
            elements.append(Paragraph(line.replace("###","").strip(), heading_style))
        elif line.startswith("##"):
            elements.append(Paragraph(line.replace("##", "").strip(), heading_style))
        elif line.startswith("-") or line.startswith("•"):
            elements.append(Paragraph(f"&nbsp;&nbsp;&nbsp;{line}", body_style))
        elif line[0].isdigit() and line[1] in [".", ")"]:
            elements.append(Paragraph(f"&nbsp;&nbsp;&nbsp;{line}", body_style))
        else:
            clean = line.replace("**", "<b>", 1).replace("**", "</b>", 1)
            elements.append(Paragraph(clean, body_style))

    doc.build(elements)
    return filename
                                                   