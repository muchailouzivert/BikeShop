from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.views.user_views import UserFacade
from users.models import Order, Bike

User = get_user_model()

class UserFacadeLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Testpass123!'
        )
        self.bike = Bike.objects.create(type='regular', color='red')
        self.order = Order.objects.create(user=self.user, bike=self.bike, accepted=False)

    def test_register_user_success(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'testuser2',
                'email': 'testuser2@example.com',
                'password1': 'Testpass123!',
                'password2': 'Testpass123!',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser2').exists())

    def test_register_user_duplicate_email(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'anotheruser',
                'email': 'testuser@example.com',  
                'password1': 'Testpass123!',
                'password2': 'Testpass123!',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User with this Email already exists.')

    def test_register_user_invalid_form(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': '',
                'email': 'not-an-email',
                'password1': '123',
                'password2': '456',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')
        self.assertContains(response, 'Enter a valid email address.')
        self.assertContains(response, 'The two password fields didn’t match.')

    def test_login_user_success(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'Testpass123!',
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_login_user_invalid_credentials(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'wrongpassword',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_logout_user(self):
        self.client.login(username='testuser', password='Testpass123!')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_accept_order(self):
        result = UserFacade.accept_order(self.user, self.order.id)
        self.order.refresh_from_db()
        self.assertTrue(result)
        self.assertTrue(self.order.accepted)

    def test_accept_order_invalid(self):
        result = UserFacade.accept_order(self.user, 9999)
        self.assertFalse(result)

    def test_cancel_order(self):
        result = UserFacade.cancel_order(self.user, self.order.id)
        self.assertTrue(result)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_cancel_order_invalid(self):
        result = UserFacade.cancel_order(self.user, 9999)
        self.assertFalse(result)
