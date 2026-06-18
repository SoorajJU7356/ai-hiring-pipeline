import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

GMAIL_SENDER = os.getenv("GMAIL_SENDER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def send_email(to_email: str, subject: str, body: str) -> dict:
    try:
        msg = MIMEMultipart()
        msg["From"] = GMAIL_SENDER
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_SENDER, to_email, msg.as_string())

        return {"success": True, "message": f"Email sent to {to_email}"}

    except Exception as e:
        return {"success": False, "message": str(e)}


def parse_email_draft(draft_text: str) -> dict:
    subject = ""
    body_lines = []
    in_body = False

    for line in draft_text.split("\n"):
        line_stripped = line.strip()

        if line_stripped.lower().startswith("subject:"):
            subject = line_stripped.split(":", 1)[1].strip()
            in_body = True
            continue

        if in_body:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()

    if not subject:
        subject = "Update regarding your application"
    if not body:
        body = draft_text.strip()

    return {"subject": subject, "body": body}