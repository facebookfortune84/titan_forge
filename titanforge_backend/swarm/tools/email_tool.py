import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

from app.core.config import settings


class EmailTool:
    def __init__(self):
        self.smtp_server = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.sender_email = settings.SMTP_USER  # Sender is usually the SMTP user

        if not all(
            [self.smtp_server, self.smtp_port, self.smtp_user, self.smtp_password]
        ):
            print(
                "WARNING: EmailTool not fully configured. Missing SMTP environment variables."
            )
            # Depending on strictness, might raise an error or just disable functionality
            self._configured = False
        else:
            self._configured = True

    def send_email(
        self,
        to_email: str | List[str],
        subject: str,
        body: str,
        html_body: Optional[str] = None,
    ) -> bool:
        """
        Sends an email to the specified recipient(s).
        :param to_email: Recipient email address(es). Can be a single string or a list of strings.
        :param subject: Subject of the email.
        :param body: Plain text body of the email.
        :param html_body: Optional HTML body of the email. If provided, a multipart message is sent.
        :return: True if email sent successfully, False otherwise.
        """
        if not self._configured:
            print("EmailTool is not configured. Cannot send email.")
            return False

        msg = MIMEMultipart("alternative") if html_body else MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = ", ".join(to_email) if isinstance(to_email, list) else to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))
        if html_body:
            msg.attach(MIMEText(html_body, "html"))

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.sender_email, to_email, msg.as_string())
            print(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")
            return False


# Example usage (for testing purposes, not part of the tool itself)
if __name__ == "__main__":
    # Ensure you have SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD in your .env
    # For testing, you can temporarily set them here for quick local checks
    # os.environ["SMTP_HOST"] = "smtp.gmail.com"
    # os.environ["SMTP_PORT"] = "465"
    # os.environ["SMTP_USER"] = "your_email@gmail.com"
    # os.environ["SMTP_PASSWORD"] = "your_app_password" # Use app password for Gmail

    email_tool = EmailTool()
    if email_tool._configured:
        email_tool.send_email(
            to_email="test@example.com",  # Replace with a real email for testing
            subject="Test Email from TitanForge",
            body="This is a test email sent from the TitanForge EmailTool.",
            html_body="""
            <html>
                <body>
                    <p>Hello,</p>
                    <p>This is a <strong>test email</strong> sent from the <em>TitanForge EmailTool</em>.</p>
                    <p>Regards,<br>TitanForge Team</p>
                </body>
            </html>
            """,
        )
    else:
        print("EmailTool not configured, skipping test email send.")
