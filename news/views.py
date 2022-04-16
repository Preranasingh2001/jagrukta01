from unicodedata import name
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import lxml
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import pandas as pd 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from .forms import CustomUserCreationForm
# Create your views here.



def paymentPage(request):
    return render(request, 'pay.html')

def loginPage(request):
    page ='login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')


    return render(request, 'news/login_register.html',{'page': page})


def logoutUser(request):
    logout(request)
    return redirect('main')    

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('home')

    context = {'form': form, 'page': page}
    return render(request,'news/login_register.html',context)


def videoPage(request):
    if "state-name" in request.GET:
            
        state=request.GET.get('state-name')
        yt_video={
                  "chhattisgarh":"https://www.youtube.com/results?search_query=chhattisgarh+news&sp=EgYIARABGAE%253D",
                  "madhya-pradesh":"https://www.youtube.com/results?search_query=madhya+pradesh+news&sp=EgYIARABGAE%253D",
                  "rajasthan":"https://www.youtube.com/results?search_query=rajasthan+news&sp=EgYIARABGAE%253D",
                  "Andhra-Pradesh":"https://www.youtube.com/results?search_query=andhrapradesh+news&sp=EgYIARABGAE%253D",
                  "Karnataka":"https://www.youtube.com/results?search_query=karnataka+news&sp=EgQIARgB",
                  "Kerala":"https://www.youtube.com/results?search_query=kerala+news&sp=EgYIARABGAE%253D",
                  "Tamil-Nadu":"https://www.youtube.com/results?search_query=tamil+nadu+news&sp=EgYIARABGAE%253D",
                  "Telangana":"https://www.youtube.com/results?search_query=telangana+news&sp=EgYIARABGAE%253D",
                  "uttar-pradesh":"https://www.youtube.com/results?search_query=uttar+pradesh+news&sp=EgYIARABGAE%253D",
                  "delhi-ncr":"https://www.youtube.com/results?search_query=delhi+ncr+news&sp=EgYIARABGAE%253D",
                  "punjab":"https://www.youtube.com/results?search_query=punjab+news&sp=EgYIARABGAE%253D",
                  "bihar":"https://www.youtube.com/results?search_query=bihar+news&sp=EgYIARABGAE%253D",
                  "haryana":"https://www.youtube.com/results?search_query=haryana+news&sp=EgYIARABGAE%253D",
                  "uttarakhand":"https://www.youtube.com/results?search_query=uttarakhand+news&sp=EgYIARABGAE%253D",
                  "jharkhand":"https://www.youtube.com/results?search_query=jharkhand+news&sp=EgYIARABGAE%253D",
                  "himachal-pradesh":"https://www.youtube.com/results?search_query=himachal+pradesh+news&sp=EgYIARABGAE%253D",
                  "jammu-and-kashmir":"https://www.youtube.com/results?search_query=jammu+kashmir+news&sp=EgYIARABGAE%253D",
                  "west-bengal":"https://www.youtube.com/results?search_query=west+bengal+news&sp=EgYIARABGAE%253D",
                  "odisha":"https://www.youtube.com/results?search_query=odisha+news&sp=EgYIARABGAE%253D",
               }

        yt_state = yt_video[state]

        driver = webdriver.Chrome() 
        driver.get(yt_state)

        user_data = driver.find_elements(By.XPATH,'//*[@id="thumbnail"]')
        links = []
        for i in user_data:
            links.append(i.get_attribute('href'))

        links=links[1:10]

        lin=[]
        base_url="https://www.youtube.com/embed/"
        for i in links:
          lin.append(base_url + (i.partition("=")[2])) 

        return render(request, 'news/videos.html', {'lin':lin})
    return render(request, 'news/videos.html')    





@login_required(login_url='login')
def homePage(request):
        r=requests.get("https://indianexpress.com/section/india/")
        soup=BeautifulSoup(r.content,'lxml')
        heading=soup.find_all('h2',{'class':'title'})
    
        heading=heading[0:10]
    

        News=[]
        for news in heading:
            News.append(news.getText().strip())

        Image=[]
        for j in soup.find_all('div',{'class':'snaps'}):
            for k in j.find_all('img'):
                Image.append(k.get('src'))

        Image=Image[1::2]  
        Image=Image[0:10]      

        s_image="https://wallpaperaccess.com/full/6170275.jpg"
        
        url3="https://www.mohfw.gov.in/"
        r3=requests.get(url3)

        soup2 = BeautifulSoup(r3.content, 'html5lib')

        covid=[]

        for miter in soup2.find_all('span', {'class' : 'mob-show'}):
            for byiter in miter.find_all('strong'):
                covid.append(byiter.text)
        
        ACases=covid[0]
        DCases=covid[1]
        DeCases=covid[2]

        if "state-name" in request.GET:
            
            state=request.GET.get('state-name')
            

            if (state=="chhattisgarh" or state=="madhya-pradesh" or state=="rajasthan"):
                url=f"https://www.amarujala.com/{state}"
                r=requests.get(url)
                soup = BeautifulSoup(r.content,'html5lib')

                News=[]
                for h in soup.find_all('div',{'class':'image_description'}):
                   for x in h.find_all('a'):
                      News.append(x.get('title'))

                News=News[0:10]

                Image=[]
                for main in soup.find_all('figure',{'class':'auw-lazy-load'}):
                   for by in main.find_all('img'):
                       Image.append("https:" + by.get('data-src'))


                Image=Image[0:10]

                dict={
                  "chhattisgarh":"https://static.toiimg.com/photo/61783642/.jpg",
                  "madhya-pradesh":"https://wallpapercave.com/wp/wp10785224.jpg",
                  "rajasthan":"https://www.mapsofindia.com/maps/rajasthan/images/rajasthan.jpg",
                   }

                s_image = dict[state] 

            elif (state=="Andhra-Pradesh" or state=="Karnataka" or state=="Kerala" or state=="Tamil-Nadu" or state=="Telangana"):
               url2=f"https://www.thenewsminute.com/section/{state}"  
               r=requests.get(url2)
               soup10=BeautifulSoup(r.content, 'html5lib')
                
               News=[]
               for h in soup10.find_all('h3',{'class':'article-title'}):
                    News.append(h.getText())    
                
               News=News[4:14]


               Image=[]
               for i in soup10.find_all('img',{'class':'card-image'}):
                   Image.append(i.get('src'))

               Image=Image[0:10] 


               dict={
                  "Andhra-Pradesh":"https://img.theculturetrip.com/1440x807/smart/wp-content/uploads/2016/06/24498998325_f451c67aae_o.jpg",
                  "Karnataka":"https://wallpapercave.com/wp/wp8568701.jpg",
                  "Kerala":"https://wallpapercave.com/dwp1x/wp7877523.jpg",
                  "Tamil-Nadu":"https://wallpapercave.com/wp/wp7626693.jpg",
                  "Telangana":"https://img.theculturetrip.com/1440x807/smart/wp-content/uploads/2016/06/24498998325_f451c67aae_o.jpg",
                 }

               s_image = dict[state]

            else:
                url=f"https://www.jagran.com/state/{state}"    
                r = requests.get(url)
                soup = BeautifulSoup(r.content,'html5lib')
                heading1 = soup.find_all('div',{'class':'h3'})
                News=[]

                for t in heading1:
                    News.append(t.text.strip())

                News=News[1:11]  


                image=soup.find_all('img',{'class':'lazy'})
                Image=[]
                #base_url="https:"
                for img in image:
                    Image.append(img.attrs['data-src'])
                
                Image=Image[0:10] 
                
                dict={
                        "uttar-pradesh":"https://wallpapercave.com/dwp1x/wp6612900.jpg",
                        "delhi-ncr":"https://wallpapercave.com/wp/wp1891549.jpg",
                        "punjab":"https://wallpaperaccess.com/full/1828844.jpg",
                        "bihar":"https://imgnew.outlookindia.com/public/uploads/articles/2021/1/28/BODHGAYA4-1024x686.jpg",
                        "haryana":"https://www.nativeplanet.com/img/2018/03/1-1520417762.jpg",
                        "uttarakhand":"https://wallpapercave.com/wp/wp7372495.jpg",
                        "jharkhand":"https://tourism.jharkhand.gov.in/Application/uploadDocuments/location/1140X320/location20200929_133548.jpg",
                        "himachal-pradesh":"https://wallpapercave.com/wp/wp5165428.jpg",
                        "jammu-and-kashmir":"https://wallpapercave.com/wp/wp2678168.jpg",
                        "west-bengal":"https://static.toiimg.com/photo/67786078.cms",
                        "odisha":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/The_sun_temple_at_konark.jpg/1024px-The_sun_temple_at_konark.jpg",
                    }

                s_image = dict[state]

            url3="https://www.mohfw.gov.in/"
            r3=requests.get(url3)

            soup2 = BeautifulSoup(r3.content, 'html5lib')

            covid=[]

            for miter in soup2.find_all('span', {'class' : 'mob-show'}):
                  for byiter in miter.find_all('strong'):
                     covid.append(byiter.text)
        
            ACases=covid[0]
            DCases=covid[1]
            DeCases=covid[2]

       
            return render(request, 'news/index.html', {'s_image': s_image , 'ACases' : ACases, 'DCases' : DCases, 'DeCases':DeCases, 'state':state, 'Image':Image, 'News': News})


        return render(request, 'news/index.html', {'s_image': s_image , 'ACases' : ACases, 'DCases' : DCases, 'DeCases':DeCases,'Image':Image, 'News': News})


