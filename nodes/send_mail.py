from graph.State import SQLAgentState
import os 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


def send_alert_email(user_input: str, user_type: str, reason: str):
    """
    Sends an email whenever a harmful input is detected.
    """

    subject = "🚨 Harmful Input Detected"

    body = f"""
    A harmful request has been detected by the SQL AI Agent.

    ==========================================
    User Type : {user_type}

    Reason:
    {reason}

    User Input:
    {user_input}
    ==========================================

    Please review this request.
    """

    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)

        print("✅ Alert email sent successfully.")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")