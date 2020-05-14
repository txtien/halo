from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'qa'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.logged_in, name='dashboard'),
    path('<slug:question>/', views.question_detail, name='question_detail'),
]
