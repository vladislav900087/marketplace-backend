
from app.core.celery_app import celery_app
from app.tasks.email_service import EmailService






@celery_app.task
def send_welcome_email(to: str, subject: str = 'Welcome message', message: str = 'Your registration has been completed!'):
    email_service = EmailService()

    email_service.send_email(subject=subject, message=message, to=to)

@celery_app.task
def send_order_confirmation_email(to: str, subject: str = 'Order confirmation email', message: str = 'Your order has been confirmed!'):
    email_service = EmailService()
    email_service.send_email(subject=subject, message=message, to=to)






