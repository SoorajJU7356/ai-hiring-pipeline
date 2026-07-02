import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SETTINGS_PATH = "settings.json"


def get_email_config() -> dict:
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r") as f:
            data = json.load(f)
            if data.get("gmail_address") and data.get("app_password"):
                return {
                    "sender_email": data["gmail_address"],
                    "app_password": data["app_password"],
                    "sender_name": data.get("sender_name", "HR Team"),
                    "company_name": data.get("company_name", "")
                }
    return {
        "sender_email": os.getenv("GMAIL_SENDER", ""),
        "app_password": os.getenv("GMAIL_APP_PASSWORD", ""),
        "sender_name": "HR Team",
        "company_name": ""
    }

def send_email(to_email: str, subject: str, body: str) -> dict:
    config = get_email_config()

    if not config["sender_email"] or not config["app_password"]:
        return {
            "success": False,
            "message": "Email credentials not configured. Please set up email in Settings."
        }

    try:
        msg = MIMEMultipart()
        msg["From"] = f"{config['sender_name']} <{config['sender_email']}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(config["sender_email"], config["app_password"])
            server.sendmail(config["sender_email"], to_email, msg.as_string())

        return {"success": True, "message": f"Email sent to {to_email}"}

    except Exception as e:
        return {"success": False, "message": str(e)}


def parse_email_draft(draft_text: str) -> dict:
    subject = ""
    body_lines = []
    in_body = False

    for line in draft_text.split("\n"):
        line_stripped = line.strip()

        if line_stripped.upper().startswith("SUBJECT:"):
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