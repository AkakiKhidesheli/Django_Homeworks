from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
]