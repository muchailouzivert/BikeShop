from .models import Bike, Order

class BikeBuilder:
    def __init__(self):
        self.bike = Bike()

    def set_type(self, bike_type):
        self.bike.type = bike_type
        return self

    def set_color(self, color):
        self.bike.color = color
        return self

    def set_battery(self, battery_capacity):
        if self.bike.type == 'electric':
            self.bike.battery_capacity = battery_capacity
        return self

    def build(self):
        self.bike.save()
        return self.bike


class RegularBikeBuilder(BikeBuilder):
    def __init__(self):
        super().__init__()
        self.bike.type = 'regular'


class ElectricBikeBuilder(BikeBuilder):
    def __init__(self):
        super().__init__()
        self.bike.type = 'electric'


class BikeDirector:
    def __init__(self, builder):
        self.builder = builder

    def construct_regular_bike(self, color):
        return self.builder.set_color(color).build()

    def construct_electric_bike(self, color, battery_capacity):
        return self.builder.set_color(color).set_battery(battery_capacity).build()


def create_order(user, bike):
    return Order.objects.create(user=user, bike=bike)
