from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm, UserLoginForm

class RegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        send_mail(
            'Добро пожаловать!',
            'Спасибо за регистрацию!',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        messages.success(self.request, 'Регистрация успешна!')
        return super().form_valid(form)

class LoginUserView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'