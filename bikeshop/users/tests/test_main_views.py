from django.test import TestCase, Client
from users.models import Bike, Order
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class MainViewsIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Testpass123!'
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_order_bike_view_get_requires_login(self):
        response = self.client.get(reverse('order_bike'))
        self.assertEqual(response.status_code, 302)  

    def test_order_bike_view_get_authenticated(self):
        self.client.login(username='testuser', password='Testpass123!')
        response = self.client.get(reverse('order_bike'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_bike.html')

    def test_order_bike_view_post_success(self):
        self.client.login(username='testuser', password='Testpass123!')
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            response = self.client.post(reverse('order_bike'), {
                'type': 'mountain',
                'color': 'red',
                'battery_capacity': '500'
            })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_success.html')


    def test_user_profile_view_orders_and_accept_cancel(self):
        self.client.login(username='testuser', password='Testpass123!')
        bike = Bike.objects.create(type='regular', color='red')
        order = Order.objects.create(user=self.user, bike=bike, accepted=False)

        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile.html')
        self.assertContains(response, bike.color)
        self.assertContains(response, 'Waiting')

        response = self.client.post(reverse('user_profile'), {
            'order_id': order.id,
            'accept_order': '1'
        }, follow=True)
        self.assertRedirects(response, reverse('user_profile'))
        order.refresh_from_db()
        self.assertTrue(order.accepted)

        response = self.client.post(reverse('user_profile'), {
            'order_id': order.id,
            'cancel_order': '1'
        }, follow=True)
        self.assertRedirects(response, reverse('user_profile'))
        self.assertFalse(Order.objects.filter(id=order.id).exists())
