from django.urls import path
from .views import RegistrationView, LoginUserView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
]