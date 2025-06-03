from django.test import TestCase
from unittest.mock import patch
from users.notifications.notifier import NotifierContext
from users.notifications.email_strategy import EmailNotificationStrategy

class NotifierContextTests(TestCase):
    @patch("users.notifications.email_strategy.send_mail", return_value=1)
    def test_email_strategy_context_interface(self, mock_send_mail):
        context = NotifierContext(EmailNotificationStrategy())
        self.assertTrue(hasattr(context, 'notify'))
        context.notify("Subject", "Message", "test@example.com")
        mock_send_mail.assert_called_once()