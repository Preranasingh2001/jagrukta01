from django.urls import path , include
from . import views


urlpatterns = [
        path('login/', views.loginPage, name="login"),
        path('logout/', views.logoutUser, name="logout"),
        path('register/', views.registerUser, name="register"),
        path('', views.homePage, name="home"),  
        path('payment/', views.paymentPage, name="payment"),  
        path('', views.chatbotPage, name="chatbot"),  
        path('videos/', views.videoPage, name="videos"),  
        path('entertainment/', views.entertainmentPage, name = "entertainment"),
        path('astronomy/', views.astronomyPage, name = "astronomy"),
        path('automobile/', views.automobilePage, name = "automobile"),
        path('buis/', views.buisPage, name = "buis"),
        path('tech/', views.techPage, name = "tech"),
        path('defence/', views.defencePage, name = "defence"),
        path('international/', views.internationalPage, name = "international"),
        path('southindia/', views.southindiaPage, name = "southindia"),
        path('marathicinema/',views.marathicinemaPage, name = "marathicinema"),
        path('hollywood/',views.hollywoodPage, name ="hollywood"),
        path('economics/',views.economicsPage, name ="economics"),
        path('inteconomic/',views.inteconomicPage, name="inteconomic"),
        path('cricket/', views.cricketPage, name = "cricket"),
        path('wpl/',views.wplPage, name ="wpl"),
        path('ipl/',views.iplPage, name="ipl"),
        path('football/',views.footballPage, name="football"),
        path('tennis/',views.tennisPage, name="tennis"),
        path('NBA/',views.NBAPage, name="NBA"),
        path('othsports/',views.othsportsPage, name="othsports"),
        # path('', include('home.urls')),   
]