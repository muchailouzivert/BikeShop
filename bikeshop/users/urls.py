from django.urls import path
from .views import main_views
urlpatterns = [
    path('', main_views.home, name='home'),
    path('register/', main_views.register, name='register'),
    path('login/', main_views.login, name='login'),
    path("logout/", main_views.logout, name='logout'),
    path('order-bike/', main_views.order_bike_view, name='order_bike'),
    path('profile/', main_views.user_profile, name='user_profile'),

]