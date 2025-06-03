from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Order, Bike
from users.views.bike_views import BikeFacade

User = get_user_model()

class BikeFacadeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')

    def test_order_regular_bike(self):
        order = BikeFacade.order_bike(self.user, bike_type='regular', color='red')
        self.assertIsInstance(order, Order)
        self.assertEqual(order.bike.type, 'regular')
        self.assertEqual(order.bike.color, 'red')
        self.assertIsNone(order.bike.battery_capacity)
        self.assertEqual(order.user, self.user)

    def test_order_electric_bike(self):
        order = BikeFacade.order_bike(self.user, bike_type='electric', color='blue', battery_capacity=500)
        self.assertIsInstance(order, Order)
        self.assertEqual(order.bike.type, 'electric')
        self.assertEqual(order.bike.color, 'blue')
        self.assertEqual(order.bike.battery_capacity, 500)
        self.assertEqual(order.user, self.user)