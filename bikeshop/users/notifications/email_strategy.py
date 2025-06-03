from django.core.mail import send_mail
from django.conf import settings
from .strategies import NotificationStrategy

class EmailNotificationStrategy(NotificationStrategy):
    def send(self, subject, message, recipient):
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [recipient],
            fail_silently=False,
        )

    def notify(self, subject, message, recipient):
        self.send(subject, message, recipient)