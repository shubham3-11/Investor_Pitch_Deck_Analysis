from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles['Title']
    story.append(Paragraph("Pitch Deck Analysis App - System Documentation", title_style))
    story.append(Spacer(1, 12))

    # 1. System Architecture
    h1_style = styles['Heading1']
    story.append(Paragraph("1. System Architecture", h1_style))
    story.append(Spacer(1, 12))

    normal_style = styles['Normal']
    arch_text = """
    The Pitch Deck Analysis App is a modern web application designed to automate the analysis of startup pitch decks.
    It uses a decoupled architecture with a React frontend and a FastAPI backend.
    """
    story.append(Paragraph(arch_text, normal_style))
    story.append(Spacer(1, 12))

    # Architecture Components
    components_data = [
        ["Component", "Technology", "Description"],
        ["Frontend", "React, TypeScript, Vite", "User interface for uploading decks and viewing analysis."],
        ["Backend", "Python, FastAPI", "REST API for handling uploads and orchestration."],
        ["Database", "SQLite (SQLModel)", "Stores startup profiles, decks, and analysis results."],
        ["AI Services", "Gemini / OpenAI", "LLMs for summarization, claim extraction, and scoring."],
        ["Background Jobs", "APScheduler", "Asynchronous processing of PDF files."],
    ]

    t = Table(components_data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(t)
    story.append(Spacer(1, 24))

    # 2. Sample Inputs
    story.append(Paragraph("2. Sample Inputs", h1_style))
    story.append(Spacer(1, 12))
    
    input_intro = "The system accepts PDF files. Below is a text representation of a hypothetical pitch deck page."
    story.append(Paragraph(input_intro, normal_style))
    story.append(Spacer(1, 12))

    code_style = ParagraphStyle('Code', parent=styles['Code'], backColor=colors.lightgrey)
    sample_input = """
    <b>Slide 1: Title</b><br/>
    Acme Corp: Revolutionizing Widget Manufacturing<br/><br/>
    <b>Slide 2: Problem</b><br/>
    Current widget manufacturing is slow and expensive. 
    Factories waste 30% of raw materials.<br/><br/>
    <b>Slide 3: Solution</b><br/>
    Our AI-driven 3D printing technology reduces waste by 90% 
    and increases speed by 5x.
    """
    story.append(Paragraph(sample_input, code_style))
    story.append(Spacer(1, 24))

    # 3. Sample Outputs
    story.append(Paragraph("3. Sample Outputs", h1_style))
    story.append(Spacer(1, 12))

    output_intro = "The system generates a JSON analysis containing a summary, claims, and follow-up questions."
    story.append(Paragraph(output_intro, normal_style))
    story.append(Spacer(1, 12))

    # Summary
    story.append(Paragraph("<b>Generated Summary (JSON Segment)</b>", styles['Heading2']))
    sample_summary = """
    {
      "product": "AI-driven 3D printing technology for widgets.",
      "market": "Manufacturing sector looking for efficiency.",
      "traction": "Prototype complete, 2 pilot customers."
    }
    """
    story.append(Paragraph(sample_summary, code_style))
    story.append(Spacer(1, 12))

    # Claims
    story.append(Paragraph("<b>Extracted Claims & Scores</b>", styles['Heading2']))
    sample_claims = """
    [
      {
        "text": "Reduces waste by 90%",
        "category": "product",
        "score": 0.8,
        "notes": "Plausible but requires verification of specific test conditions."
      }
    ]
    """
    story.append(Paragraph(sample_claims, code_style))
    story.append(Spacer(1, 12))

    # Questions
    story.append(Paragraph("<b>Generated Questions</b>", styles['Heading2']))
    sample_questions = """
    [
      {
        "text": "Can you provide data from the pilot customers verifying the 90% waste reduction?",
        "category": "product"
      }
    ]
    """
    story.append(Paragraph(sample_questions, code_style))

    doc.build(story)
    print(f"PDF generated: {filename}")

if __name__ == "__main__":
    generate_pdf("System_Architecture_and_Samples.pdf")
