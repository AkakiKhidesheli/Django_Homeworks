from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/add/', views.add_book, name='add_book'),
    path('book/delete/<int:book_id>/', views.delete_book, name='delete_book'),
]