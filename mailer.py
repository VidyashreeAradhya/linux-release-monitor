import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

from config import (
    SMTP_SERVER,
    SMTP_PORT,
    SENDER_EMAIL,
    RECEIVER_EMAILS,
    MAIL_SUBJECT
)


def send_mail(html_content):

    try:

        # ==================================
        # Create Mail
        # ==================================

        message = MIMEMultipart(
            "alternative"
        )

        message["Subject"] = MAIL_SUBJECT

        message["From"] = SENDER_EMAIL

        message["To"] = ", ".join(
            RECEIVER_EMAILS
        )

        # ==================================
        # Attach HTML
        # ==================================

        html_part = MIMEText(
            html_content,
            "html"
        )

        message.attach(html_part)

        # ==================================
        # SMTP Connection
        # ==================================

        print(
            "Connecting to SMTP server..."
        )

        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=60
        )

        server.starttls()

        print(
            "Sending email..."
        )

        server.sendmail(
            SENDER_EMAIL,
            RECEIVER_EMAILS,
            message.as_string()
        )

        server.quit()

        print(
            "Mail Sent Successfully"
        )

    except Exception as e:

        print(
            f"Mail sending failed: {e}"
        )