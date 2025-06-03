from django.test import TestCase
from users.models import Bike
from users.services import BikeDirector, RegularBikeBuilder, ElectricBikeBuilder

class BikeBuilderTests(TestCase):
    def test_regular_bike_builder_sets_correct_type(self):
        builder = RegularBikeBuilder()
        director = BikeDirector(builder)
        bike = director.construct_regular_bike("green")
        self.assertEqual(bike.type, "regular")
        self.assertEqual(bike.color, "green")
        self.assertIsNone(bike.battery_capacity)

    def test_electric_bike_builder_sets_battery(self):
        builder = ElectricBikeBuilder()
        director = BikeDirector(builder)
        bike = director.construct_electric_bike("black", 600)
        self.assertEqual(bike.type, "electric")
        self.assertEqual(bike.color, "black")
        self.assertEqual(bike.battery_capacity, 600)

    def test_builder_builds_and_saves_bike(self):
        builder = RegularBikeBuilder()
        builder.set_color("yellow")
        bike = builder.build()
        self.assertIsInstance(bike, Bike)
        self.assertTrue(Bike.objects.filter(id=bike.id).exists())