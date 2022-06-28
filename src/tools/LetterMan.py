
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Cheese.appSettings import Settings

class LetterMan:

    @staticmethod
    def sendMail(email, html, subject):
        smtp_user = "anticary@gmail.com"
        smtp_password = Settings.emailCode
        server = "smtp.gmail.com"
        port = 587
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = email

        part2 = MIMEText(html, "html")
        msg.attach(part2)

        s = smtplib.SMTP(server, port)
        s.ehlo()
        s.starttls()
        s.login(smtp_user, smtp_password)
        s.sendmail(smtp_user, email, msg.as_string())
        s.quit()