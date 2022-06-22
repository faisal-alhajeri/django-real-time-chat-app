from django.urls import path 
from . import views 
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
   path('register/', views.RegisterView.as_view(), name='register'),
   path('', views.RegisterView.as_view(), name='register'),
   path('login/', views.MyLoginView.as_view(), name='login'),
   path('logout/', views.logout_request, name='logout'),
]