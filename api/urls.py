from django.urls import path
from api import views

urlpatterns = [
    path('genres/', views.genres),
    path('books/', views.BooksView.as_view()),
    path('books/create', views.BookCreateView.as_view()),

    path('genres/<int:id>/books/', views.books_by_genre),
    path('order/', views.order_book),

    path('users/register', views.RegistrationAPIView.as_view()),
    path('users/login', views.LoginAPIView.as_view()),

    path('genres/<int:id>/', views.genre),
    path('books/<int:id>/', views.BookDetailedView.as_view()),
    path('order/<int:id>/', views.OrderInfo.as_view()),
]