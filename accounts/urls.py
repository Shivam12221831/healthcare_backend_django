# accounts/urls.py
# from django.urls import path
# from .views import RegisterView

# urlpatterns = [
#     path("register/", RegisterView.as_view(), name="register"),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
]
