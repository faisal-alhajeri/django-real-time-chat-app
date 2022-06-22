from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.LobbyView.as_view(), name='lobby'),
    path('<str:user_id>/', views.ChatView.as_view(), name='chat'),
    path('<str:user_id>/add/', views.AddView.as_view(), name='add-user'),
    # path('<str:user_id>/add', views.ChatView.as_view(), name='chat'),
]