from ..models import Order
from ..services import RegularBikeBuilder, ElectricBikeBuilder, BikeDirector

class BikeFacade:

    @staticmethod
    def order_bike(user, bike_type, color, battery_capacity=None):

        if bike_type == 'electric':
            builder = ElectricBikeBuilder()
        else:
            builder = RegularBikeBuilder()

        director = BikeDirector(builder)
        if bike_type == 'electric':
            bike = director.construct_electric_bike(color, battery_capacity)
        else:
            bike = director.construct_regular_bike(color)

        order = Order.objects.create(user=user, bike=bike)
        return order
