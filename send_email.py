from mail_login import user, password, receivers
import smtplib, ssl
from email.message import EmailMessage

def send_fail_email(msg_body):
    msg = EmailMessage()
    msg.set_content(msg_body)
    msg["Subject"] = "Matanga scraping failed"
    msg["From"] = user
    msg["To"] = receivers.join(",")
    context = ssl.create_default_context()
    server = smtplib.SMTP("smtp.gmail.com", port=587)
    server.starttls(context=context)
    server.login(user, password)
    server.sendmail(user, receivers, msg.as_string())
    server.quit()
    print("Failure email sent")
