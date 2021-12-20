import smtplib
from email.message import EmailMessage


def send_mail_to(to_email,subject,body):
    EMAILADDRESS = "testvoiceassiatant@gmail.com"
    PASSWORD = "123456789test"
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAILADDRESS
    msg['To'] = to_email
    msg.set_content(body)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    try:
        server.login(EMAILADDRESS, PASSWORD)
        print("logged in ...")
        server.send_message(msg)
        return f"email sent to {msg['To']}"
    except smtplib.SMTPAuthenticationError:
        print("Error logging in")
        return "Error logging in please try again later "
