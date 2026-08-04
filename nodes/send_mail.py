from graph.State import SQLAgentState
import os 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from typing import Literal
from langgraph.types import Command
from langgraph.graph import END

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


def send_alert_email(state:SQLAgentState)-> Command[Literal["error_router",END]]:
    """
    Sends an email whenever a harmful input is detected.
    """

    subject = "🚨 Harmful Input Detected"

    body = f"""
    A harmful request has been detected by the SQL AI Agent.

    ==========================================
    User Type : {state.get("user_type", "Unknown")}

    Reason:
    "this request will make changes to the database and is considered harmful"

    User Input:
    {state.get("input", "Unknown")}
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
        return Command(
            goto=END,
        )

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return Command(
            update={"Error": f"Failed to send email: {e}"},
            goto="error_router"
        )