from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model  
from ..forms import CustomUserCreationForm
from ..notifications.email_strategy import EmailNotificationStrategy
from ..notifications.notifier import NotifierContext


from_email = settings.EMAIL_HOST_USER
User = get_user_model()  

class UserFacade:
    @staticmethod
    def send_email(subject, message, recipient_email):
        context = NotifierContext(EmailNotificationStrategy())
        context.notify(subject, message, recipient_email)

    @staticmethod
    def register_user(request):
        if request.user.is_authenticated:
            return redirect('/')

        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                if User.objects.filter(email=email).exists():
                    return render(request, 'register.html', {
                        'form': form,
                        'error': 'A user with this email already exists.'
                    })

                user = form.save()
                auth_login(request, user)

                UserFacade.send_email(
                    'Welcome to Our Platform!',
                    f'Thank you for registering on our platform, {user.username}.',
                    user.email
                )

                return redirect('/')
            else:
                return render(request, 'register.html', {'form': form, 'error': 'Invalid form submission.'})
        else:
            form = CustomUserCreationForm()

        return render(request, 'register.html', {'form': form})

    @staticmethod
    def login_user(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)

                UserFacade.send_email(
                    'Welcome Back!',
                    f'{user.username}, you have successfully logged in.',
                    user.email
                )

                return redirect('/')
            else:
                return render(request, "login.html", {"error": "Invalid username or password"})
        return render(request, "login.html")
    
    @staticmethod
    @login_required
    def logout_user(request):
        logout(request)
        return redirect("/")
    
    @staticmethod
    def accept_order(user, order_id):
        from users.models import Order
        order = Order.objects.filter(id=order_id, user=user, accepted=False).first()
        if order:
            order.accepted = True
            order.save()
            return True
        return False
    
    @staticmethod
    def cancel_order(user, order_id):
        from users.models import Order
        order = Order.objects.filter(id=order_id, user=user).first()
        if order:
            order.delete()
            return True
        return False
    

