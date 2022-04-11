from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('room/<str:pk>', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    #User Authentication
    path('login/', views.userLogin, name="user-login"),
    path('logout/', views.userLogout, name="user-logout"),
    path('register/', views.userRegister, name="user-register"),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),


    #Room creation 
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),

]