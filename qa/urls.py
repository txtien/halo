from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'qa'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('new_question/', views.create_question, name='new_question'),
    path('<slug:question>/', views.question_detail, name='question_detail'),
    path('tag/<slug:tag_slug>', views.home, name="question_by_tag"),
    path('user/vote/', views.voting, name='vote'),

]
