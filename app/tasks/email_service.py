import smtplib

from email.message import EmailMessage

from app.core.config import SMTP_EMAIL, SMTP_PASSWORD


class EmailService:
    def send_email(self, subject, message, to):

        if not to:
            raise ValueError('You must provide an email address')

        if '\n' in subject or '\r' in subject:
            raise ValueError('Invalid subject format')

        if '\n' in to or '\r' in to:
            raise ValueError('Invalid recipient format')

        try:
            msg = EmailMessage()

            msg['Subject'] = subject
            msg['From'] = SMTP_EMAIL
            msg['To'] = to

            msg.set_content(message)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(SMTP_EMAIL, SMTP_PASSWORD)

                response = smtp.send_message(msg)

                print('MESSAGE SENT!', response)

            print(SMTP_EMAIL)
            print(SMTP_PASSWORD)
        except smtplib.SMTPRecipientsRefused:
            print('No email address')