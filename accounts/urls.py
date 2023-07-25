from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register_user"),
    path('update_user', views.update_user, name="update_user"),
    path('change_pass', views.change_pass, name="change_pass"),
    path("unauthorised", views.unauthorised_page, name="unauthorised_page"),
]
