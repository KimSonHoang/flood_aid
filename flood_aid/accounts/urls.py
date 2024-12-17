from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", LogoutView.as_view(next_page="home"), name="logout"),
    path("verify_otp", views.verify_otp, name="verify_otp"),
    path("profile", views.profile, name="profile"),
]
