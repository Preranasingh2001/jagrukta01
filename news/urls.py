from django.urls import path , include
from . import views


urlpatterns = [
        path('login/', views.loginPage, name="login"),
        path('logout/', views.logoutUser, name="logout"),
        path('register/', views.registerUser, name="register"),
        path('home/', views.homePage, name="home"),  
        path('home/videos/', views.videoPage, name="videos"),  
        path('', include('home.urls')),   
]