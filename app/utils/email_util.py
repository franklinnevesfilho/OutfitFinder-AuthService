import smtplib
from email.mime.text import MIMEText
import os

_template_dir = os.path.join(os.path.dirname(__file__), "templates")
def _template(name: str):
    return _template_dir + f"/{name}.html"

_smtp_server: dict = {
    "host": os.getenv("SMTP_HOST", "live.smtp.mailtrap.io"),
    "port": os.getenv("SMTP_PORT", "587"),
    "user": os.getenv("SMTP_USER", "api"),
    "password": os.getenv("SMTP_PASSWORD", "837f38ee652502f596803309050872f5"),
}

def _send_email(to: str, subject: str, body: str) -> None:
    """
    Send an email
    :param to: The email address to send the email to
    :param subject: The subject of the email
    :param body: The body of the email
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = _smtp_server["user"]
    msg["To"] = to

    with smtplib.SMTP(_smtp_server["host"], _smtp_server["port"]) as server:
        server.starttls()
        server.login(_smtp_server["user"], _smtp_server["password"])
        server.sendmail(f"noreply@{_smtp_server["host"]}", to, msg.as_string())

def send_password_reset_email(to: str, reset_code: str) -> None:
    """
    Send a password reset email
    :param to: The email address to send the email to
    :param reset_code: The password reset code
    """
    with open(_template("password-reset")) as file:
        body = file.read().replace("{{reset_code}}", reset_code)
        _send_email(to, "Password Reset", body)

def send_verification_email(to: str, verification_code: str) -> None:
    """
    Send a verification email
    :param to: The email address to send the email to
    :param verification_code: The verification code
    """
    with open(_template("verification")) as file:
        body = file.read().replace("{{verification_code}}", verification_code)
        _send_email(to, "Email Verification", body)
