from .bike_views import BikeFacade
from .user_views import UserFacade
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from users.models import Order, Bike


def register(request):
    return UserFacade.register_user(request)

def login(request):
    return UserFacade.login_user(request)

def logout(request):
    return UserFacade.logout_user(request)

def home(request):
    return render(request, 'index.html')

@login_required
def order_bike_view(request):
    if request.method == 'POST':
        bike_type = request.POST.get('type')
        color = request.POST.get('color')
        battery_capacity = request.POST.get('battery_capacity', None)

        try:
            order = BikeFacade.order_bike(
                user=request.user,
                bike_type=bike_type,
                color=color,
                battery_capacity=battery_capacity
            )
            return render(request, 'order_success.html', {'order': order})
        except Exception as e:
            return render(request, 'order_bike.html', {'error': str(e)})

    return render(request, 'order_bike.html')

@login_required
def user_profile(request):
    orders = Order.objects.filter(user=request.user).select_related('bike')
    bikes = Bike.objects.all()
    accepted_bikes = [order.bike for order in orders if order.accepted]

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if 'accept_order' in request.POST:
            UserFacade.accept_order(request.user, order_id)
            return redirect('user_profile')
        elif 'cancel_order' in request.POST:
            UserFacade.cancel_order(request.user, order_id)
            return redirect('user_profile')

    return render(request, 'user_profile.html', {
        'orders': orders,
        'bikes': bikes,
        'accepted_bikes': accepted_bikes,
    })