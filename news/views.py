from unicodedata import name
from urllib import request
from django.shortcuts import render, redirect
from django.shortcuts import render, HttpResponse
import json
import requests
import urllib3
import math
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import lxml
from bs4 import BeautifulSoup
import requests
import pandas as pd 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from selenium.webdriver.common.by import By 
# from selenium.webdriver.support.ui import WebDriverWait 
# from selenium.webdriver.support import expected_conditions as EC
from .forms import CustomUserCreationForm
# Create your views here.

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def chatbotPage(request):
    return render(request, 'bot.html')

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
    options = Options()
    options.headless = True   
    driver = webdriver.Chrome(ChromeDriverManager().install(),options = options)
    

    if "state-name" in request.GET:
            
        state=request.GET.get('state-name')
        dict={
                        "Chhattisgarh":"https://static.toiimg.com/photo/61783642/.jpg",
                        "Madhya-Pradesh":"https://wallpapercave.com/wp/wp10785224.jpg",
                        "Rajasthan":"https://www.mapsofindia.com/maps/rajasthan/images/rajasthan.jpg",
                        "Uttar-Pradesh":"https://wallpapercave.com/dwp1x/wp6612900.jpg",
                        "Delhi-NCR":"https://wallpapercave.com/wp/wp1891549.jpg",
                        "Punjab":"https://wallpaperaccess.com/full/1828844.jpg",
                        "Bihar":"https://imgnew.outlookindia.com/public/uploads/articles/2021/1/28/BODHGAYA4-1024x686.jpg",
                        "Haryana":"https://www.nativeplanet.com/img/2018/03/1-1520417762.jpg",
                        "Uttarakhand":"https://wallpapercave.com/wp/wp7372495.jpg",
                        "Jharkhand":"https://tourism.jharkhand.gov.in/Application/uploadDocuments/location/1140X320/location20200929_133548.jpg",
                        "Himachal-Pradesh":"https://wallpapercave.com/wp/wp5165428.jpg",
                        "Jammu-and-Kashmir":"https://wallpapercave.com/wp/wp2678168.jpg",
                        "West-Bengal":"https://static.toiimg.com/photo/67786078.cms",
                        "Andhra-Pradesh":"https://img.theculturetrip.com/1440x807/smart/wp-content/uploads/2016/06/24498998325_f451c67aae_o.jpg",
                        "Karnataka":"https://wallpapercave.com/wp/wp8568701.jpg",
                        "Kerala":"https://wallpapercave.com/dwp1x/wp7877523.jpg",
                        "Tamil-Nadu":"https://wallpapercave.com/wp/wp7626693.jpg",
                        "Telangana":"https://img.theculturetrip.com/1440x807/smart/wp-content/uploads/2016/06/24498998325_f451c67aae_o.jpg",
                        "Odisha":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/The_sun_temple_at_konark.jpg/1024px-The_sun_temple_at_konark.jpg",
             }
        s_image=dict[state]     
        yt_video={
                  "Chhattisgarh":"https://www.youtube.com/results?search_query=chhattisgarh+news&sp=CAISBggCEAEYAQ%253D%253D",
                  "Madhya-Pradesh":"https://www.youtube.com/results?search_query=madhya+pradesh+news&sp=EgYIARABGAE%253D",
                  "Rajasthan":"https://www.youtube.com/results?search_query=rajasthan+news&sp=EgYIAhABGAE%253D",
                  "Andhra-Pradesh":"https://www.youtube.com/results?search_query=andhrapradesh+news&sp=EgYIARABGAE%253D",
                  "Karnataka":"https://www.youtube.com/results?search_query=karnataka+news&sp=EgQIARgB",
                  "Kerala":"https://www.youtube.com/results?search_query=kerala+news&sp=EgYIARABGAE%253D",
                  "Tamil-Nadu":"https://www.youtube.com/results?search_query=tamil+nadu+news&sp=EgYIARABGAE%253D",
                  "Telangana":"https://www.youtube.com/results?search_query=telangana+news&sp=EgYIARABGAE%253D",
                  "Uttar-Pradesh":"https://www.youtube.com/results?search_query=uttar+pradesh+news&sp=EgYIAhABGAE%253D",
                  "Delhi-NCR":"https://www.youtube.com/results?search_query=delhi+ncr+news&sp=EgYIAhABGAE%253D",
                  "Punjab":"https://www.youtube.com/results?search_query=punjab+news&sp=CAASBggCEAEYAQ%253D%253D",
                  "Bihar":"https://www.youtube.com/results?search_query=bihar+news&sp=EgYIARABGAE%253D",
                  "Haryana":"https://www.youtube.com/results?search_query=haryana+news&sp=EgYIARABGAE%253D",
                  "Uttarakhand":"https://www.youtube.com/results?search_query=uttarakhand+news&sp=EgYIARABGAE%253D",
                  "Jharkhand":"https://www.youtube.com/results?search_query=jharkhand+news&sp=EgYIARABGAE%253D",
                  "Himachal-Pradesh":"https://www.youtube.com/results?search_query=himachal+pradesh+news&sp=EgYIARABGAE%253D",
                  "Jammu-and-Kashmir":"https://www.youtube.com/results?search_query=jammu+kashmir+news&sp=EgYIAhABGAE%253D",
                  "West-Bengal":"https://www.youtube.com/results?search_query=west+bengal+news&sp=EgYIARABGAE%253D",
                  "Odisha":"https://www.youtube.com/results?search_query=odisha+news&sp=EgYIARABGAE%253D",
               }

        yt_state = yt_video[state]

        # driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(yt_state)

        user_data = driver.find_elements(By.XPATH,'//*[@id="thumbnail"]')
        links = []
        for i in user_data:
            links.append(i.get_attribute('href'))

        links=links[1:11]

        lin=[]
        base_url="https://www.youtube.com/embed/"
        for i in links:
          lin.append(base_url + (i.split("=")[1].split("&")[0]))
          #lin.append(base_url + (i.partition("=")[2])) 
        
        driver.close()

        return render(request, 'news/videos.html', {'lin':lin,'state':state,'s_image':s_image})

    yt_state="https://www.youtube.com/results?search_query=india+news&sp=EgYIAhABGAE%253D"
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(yt_state)

    user_data = driver.find_elements(By.XPATH,'//*[@id="thumbnail"]')
    links = []
    for i in user_data:
        links.append(i.get_attribute('href'))

    links=links[1:11]

    lin=[]
    base_url="https://www.youtube.com/embed/"
    for i in links:
        lin.append(base_url + (i.split("=")[1].split("&")[0]))
        #lin.append(base_url + (i.partition("=")[2])) 
  
    s_image="https://wallpaperaccess.com/full/6170275.jpg" 

    return render(request, 'news/videos.html', {'lin':lin, 's_image':s_image})    

def defencePage(request):
    r = requests.get("https://idrw.org/",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    
    for a in soup.find_all('h2',{'class':'art-postheader entry-title'}):
        for b in a.find_all('a'):
            heading.append(b.getText())

    heading=heading[0:10]

    Url=[]
    for link in soup.find_all('h2',{'class':'art-postheader entry-title'}):
        for l in link.find_all('a'):
            Url.append( l.get('href'))       

    Url=Url[0:10]

    Image=[]

    for j in soup.find_all('div',{'class':'art-postcontent clearfix'}):
        for k in j.find_all('img'):
            Image.append(k.get('src'))

    Image=Image[0:10]

    employees = zip(Image,Url,heading)

    return render(request, 'news/defence.html', {'employees':employees})  

def techPage(request):
    r = requests.get("https://www.gadgets360.com/news",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('span',{'class':'news_listing'}):
            heading.append(a.getText())

    heading=heading[0:10]

    Url=[]
    for link in soup.find_all('div',{'class':'caption_box'}):
        for l in link.find_all('a'):
            Url.append( l.get('href'))       

    Url=Url[0:10]

    Image=[]

    for j in soup.find_all('div',{'class':'thumb'}):
       for k in j.find_all('img'):
        Image.append(k.get('src'))

    Image=Image[0:10] 

    employees = zip(Image,Url,heading)

    return render(request, 'news/tech.html', {'employees':employees})   


def buisPage(request):
    r=requests.get("https://www.business-standard.com/",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('div',{'class':'article'}):
        for b in a.find_all('h2'):
            heading.append(b.getText())
    
    heading=heading[0:9]

    Url=[]
    for link in soup.find_all('div',{'class':'article'}):
        for l in link.find_all('a'):
            Url.append("https://www.business-standard.com" + l.get('href'))
    
    Url = Url[0:9]

    Image=[]
    for j in soup.find_all('div',{'class':'article'}):
        for k in j.find_all('img'):
            Image.append(k.get('src'))

    Image = Image[0:10] 
    Image = Image[:5] + Image[6:]  

    employees=zip(Image, Url, heading)
    return render(request, 'news/buis.html', {'employees':employees})

def automobilePage(request):
    r=requests.get("https://www.livemint.com/auto-news",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('div',{'class':'headlineSec'}):
       for p in a.find_all('h2',{'class':'headline'}):
         for b in p.find_all('a'):
            heading.append(b.getText())
    
    heading=heading[0:10]

    Url=[]
    for link in soup.find_all('div',{'class':'headlineSec'}):
        for l in link.find_all('a'):
            Url.append(l.get('href'))
    
    Url = Url[0:10]

    Image=[]

    for j in soup.find_all('div',{'class':'listtostory clearfix'}):
        for g in j.find_all('a',{'class':'imgSec'}): 
          for k in g.find_all('img',{'class':'lozad fade'}):
            Image.append(k.get('data-src'))

    Image = Image[0:10]   

    employees=zip(Image, Url, heading)
    return render(request, 'news/automobile.html', {'employees':employees})

def astronomyPage(request):
    r=requests.get("https://astronomy.com/news",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('div',{'class':'latestNews'}):
        for b in a.find_all('h2'):
            heading.append(b.getText())
    
    heading=heading[0:12]

    Content=[]
    for a in soup.find_all('div',{'class':'latestNews'}):
        for b in a.find_all('div',{'class':'snippet'}):
            Content.append(b.getText())

    Content=Content[0:12]

    Url=[]
    for link in soup.find_all('div',{'class':'content withImage'}):
        for l in link.find_all('a'):
            Url.append("https://astronomy.com"+l.get('href'))
    
    Url = Url[0:12]

    Image=[]
    for j in soup.find_all('div',{'class':'dataItem'}):
        for k in j.find_all('img'):
            Image.append("https://astronomy.com" + k.get('src'))

    Image = Image[3:15]   

    employees=zip(Image, Url, Content, heading)
    return render(request, 'news/astronomy.html', {'employees':employees})     


def internationalPage(request):
    r=requests.get("https://news-decoder.com/category/world/",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('h2',{'class':'entry-title'}):  
        for b in a.find_all('a'):
            heading.append(b.getText())
    
    heading=heading[0:10]
    
    Content=[]
    for y in soup.find_all('p',{'class':'xcrpt'}):
        Content.append(y.getText())

    Content=Content[0:10]

    Url=[]
    for link in soup.find_all('h2',{'class':'entry-title'}):
         for l in link.find_all('a'):
            Url.append(l.get('href'))
    
    Url = Url[0:10]

    Image=[]
    for j in soup.find_all('a',{'class':'entry-featured-image-url'}):
        for k in j.find_all('img'):
            Image.append(k.get('src'))

    Image = Image[0:10]   

    employees=zip(Image, Url,Content, heading)
    return render(request, 'news/international.html', {'employees':employees})       

def entertainmentPage(request):
    r=requests.get("https://indianexpress.com/section/entertainment/",verify=False)
    soup=BeautifulSoup(r.content,'lxml')
    
    News=[]
    
    for inew in soup.find_all('div',{'class':'title'}):
            for jnew in inew.find_all('a'):
              News.append(jnew.get('title'))

    News= News[0:10]        
    
    Content=[]
    for a in soup.find_all('div',{'class':'articles'}):
        for b in a.find_all('div',{'class':'title'}):
            for c in b.find_all('p'):
              Content.append(c.getText())

    Content=Content[0:10]  

    Url=[]
    for link in soup.find_all('div',{'class':'articles'}):
        for li in link.find_all('div',{'class':'snaps'}):
            for ji in li.find_all('a'):
              Url.append(ji.get('href'))
    
    Url = Url[0:10]

    Image=[]
    for k in soup.find_all('div',{'class':'articles'}):
      for l in k.find_all('div',{'class':'snaps'}):
        for m in l.find_all('img'):
            Image.append(m.get('src'))
          
     
    Image=Image[0:10]   
    
    employees=zip(Image, Url, Content, News)
    return render(request, 'news/entertainment.html', {'employees':employees})

def southindiaPage(request):
    r=requests.get("https://www.koimoi.com/category/south-indian-cinema/",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('div',{'class':'td-block-span6'}):
        for b in a.find_all('h3',{'class':'entry-title td-module-title'}):
            for c in b.find_all('a'):
             heading.append(c.getText())
    
    heading=heading[0:10]

    Url=[]
    for link in soup.find_all('div',{'class':'td-block-span6'}):
      for lin in link.find_all('h3',{'class':'entry-title td-module-title'}):
        for l in lin.find_all('a'):
            Url.append(l.get('href'))
    
    Url = Url[0:10]

    Image=[]
    for j in soup.find_all('div',{'class':'td-block-span6'}):
       for s in j.find_all('div',{'class':'td-module-image'}): 
         for k in s.find_all('div',{'class':'td-module-thumb'}):
           for m in k.find_all('a'):
             for l in m.find_all('img',{'class':'entry-thumb'}):
                Image.append(l.get('src'))

    Image = Image[0:10]   
    

    employees=zip(Image, Url, heading)
    return render(request, 'news/southindia.html', {'employees':employees})     


def marathicinemaPage(request):
    r=requests.get("https://www.loksatta.com/manoranjan/marathi-cinema/",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('div',{'class':'entry-title'}):
            for b in a.find_all('a'):
             heading.append(b.getText())
    
    heading=heading[0:10]

    Url=[]
    for link in soup.find_all('div',{'class':'entry-title'}):
        for l in link.find_all('a'):
            Url.append(l.get('href'))
    
    Url = Url[0:10]

    Image=[]
    for j in soup.find_all('figure',{'class':'post-thumbnail'}):
           for m in j.find_all('a'):
             for l in m.find_all('img'):
                Image.append(l.get('src'))

    Image = Image[0:10]   

    employees=zip(Image, Url, heading)
    return render(request, 'news/marathicinema.html', {'employees':employees})     

def hollywoodPage(request):
    r=requests.get("https://www.firstpost.com/entertainment/hollywood",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    
    for c in soup.find_all('div',{'class':'main-content'}):
         for d in c.find_all('div',{'class':'big-thumb'}):   
            for b in d.find_all('a'):
                 for a in b.find_all('img'):
                  heading.append(a.get('title'))
    
    heading=heading[0:10]

    Url=[]
    for link in soup.find_all('div',{'class':'main-content'}):
        for lin in link.find_all('div',{'class':'big-thumb'}):
         for l in lin.find_all('a'):
            Url.append(l.get('href'))
    
    Url = Url[0:10]

    Image=[]
    
    for j in soup.find_all('div',{'class':'main-content'}):
           for n in j.find_all('div',{'class':'big-thumb'}):
            for m in n.find_all('a',{'class':'thumb-img'}):
             for l in m.find_all('img'):
                Image.append(l.get('data-src'))

    Image = Image[0:10]   

    employees=zip(Image, Url, heading)
    return render(request, 'news/hollywood.html', {'employees':employees})

def economicsPage(request):
    r=requests.get("https://www.businesstoday.in/latest/economy",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('div',{'class':'section-listing-LHS'}):
     for b in a.find_all('div',{'class':'widget-listing'}):
      for c in b.find_all('div',{'class':'widget-listing-body'}):
        for d in c.find_all('div',{'class':'widget-listing-thumb'}):
          for e in d.find_all('a'): 
            for f in e.find_all('img'):
                heading.append(f.get('alt'))
    
    heading=heading[0:10]

    Url=[]
    for link in soup.find_all('div',{'class':'section-listing-LHS'}):
        for lin in link.find_all('div',{'class':'widget-listing'}):
         for li in lin.find_all('div',{'class':'widget-listing-body'}):
          for lis in li.find_all('div',{'class':'widget-listing-thumb'}):
            for l in lis.find_all('a'):
              Url.append(l.get('href'))
    
    Url = Url[0:10]

    Image=[]
    for n in soup.find_all('div',{'class':'section-listing-LHS'}):
     for j in n.find_all('div',{'class':'widget-listing'}):
      for i in j.find_all('div',{'class':'widget-listing-body'}):
        for m in i.find_all('div',{'class':'widget-listing-thumb'}):
          for k in m.find_all('a'):
            for l in k.find_all('img'):
              Image.append(l.get('data-src'))

    Image = Image[0:10]   

    employees=zip(Image, Url, heading)
    return render(request, 'news/economics.html', {'employees':employees})     

def inteconomicPage(request):
    r=requests.get("https://www.business-standard.com/category/international-news-economy-1160102.htm",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('div',{'class':'listing-panel'}):
     for b in a.find_all('ul'):
      for c in b.find_all('li'):
        for d in c.find_all('h2'):
          for e in d.find_all('a'): 
            heading.append(e.getText())
    
    heading=heading[0:10]

    Url=[]
    for link in soup.find_all('div',{'class':'listing-panel'}):
        for lin in link.find_all('ul'):
         for li in lin.find_all('li'):
          for lis in li.find_all('h2'):
            for l in lis.find_all('a'):
              Url.append(l.get('href'))
    
    Url = Url[0:10]

    Image=[]
    for n in soup.find_all('div',{'class':'listing-panel'}):
     for j in n.find_all('ul'):
      for i in j.find_all('li'):
          for k in i.find_all('a'):
            for l in k.find_all('img'):
              Image.append(l.get('src'))

    Image = Image[0:10]   

    employees=zip(Image, Url, heading)
    return render(request, 'news/inteconomic.html', {'employees':employees})     

def cricketPage(request):
    r=requests.get("https://www.cricbuzz.com/cricket-news/latest-news",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('div',{'class':'cb-bg-white'}):
     for b in a.find_all('div',{'class':'cb-col cb-col-100 cb-lst-itm cb-pos-rel cb-lst-itm-lg'}):
      for c in b.find_all('div',{'class':'cb-col cb-col-33 cb-pos-rel'}):
        for d in c.find_all('a'):
          for e in d.find_all('img'): 
            heading.append(e.get('title'))
    
    heading=heading[0:10]

    Url=[]
    for link in soup.find_all('div',{'class':'cb-bg-white'}):
        for lin in link.find_all('div',{'class':'cb-col cb-col-100 cb-lst-itm cb-pos-rel cb-lst-itm-lg'}):
         for li in lin.find_all('div',{'class':'cb-col cb-col-33 cb-pos-rel'}):
            for l in li.find_all('a'):
              Url.append("https://www.cricbuzz.com"+l.get('href'))
    
    Url = Url[0:10]

    Image=[]
    for n in soup.find_all('div',{'class':'cb-bg-white'}):
     for j in n.find_all('div',{'class':'cb-col cb-col-100 cb-lst-itm cb-pos-rel cb-lst-itm-lg'}):
      for i in j.find_all('div',{'class':'cb-col cb-col-33 cb-pos-rel'}):
          for k in i.find_all('a'):
            for l in k.find_all('img'):
              Image.append(l.get('src'))

    Image = Image[0:10]   

    employees=zip(Image, Url, heading)
    return render(request, 'news/cricket.html', {'employees':employees})     


def wplPage(request):
    r=requests.get("https://www.cricbuzz.com/cricket-series/5938/womens-premier-league-2023",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('div',{'class':'cb-col-100 cb-col'}):
     for b in a.find_all('div',{'class':'cb-col cb-col-100 cb-lst-itm cb-pos-rel cb-lst-itm-lg'}):
      for c in b.find_all('div',{'class':'cb-col cb-col-33 cb-pos-rel'}):
        for d in c.find_all('a'):
          for e in d.find_all('img'): 
            heading.append(e.get('title'))
    
    heading=heading[0:10]

    Url=[]
    for link in soup.find_all('div',{'class':'cb-col-100 cb-col'}):
        for lin in link.find_all('div',{'class':'cb-col cb-col-100 cb-lst-itm cb-pos-rel cb-lst-itm-lg'}):
         for li in lin.find_all('div',{'class':'cb-col cb-col-33 cb-pos-rel'}):
            for l in li.find_all('a'):
              Url.append("https://www.cricbuzz.com"+l.get('href'))
    
    Url = Url[0:10]

    Image=[]
    for n in soup.find_all('div',{'class':'cb-col-100 cb-col'}):
     for j in n.find_all('div',{'class':'cb-col cb-col-100 cb-lst-itm cb-pos-rel cb-lst-itm-lg'}):
      for i in j.find_all('div',{'class':'cb-col cb-col-33 cb-pos-rel'}):
          for k in i.find_all('a'):
            for l in k.find_all('img'):
              Image.append(l.get('src'))

    Image = Image[0:10]   

    employees=zip(Image, Url, heading)
    return render(request, 'news/wpl.html', {'employees':employees})    

def iplPage(request):
    r=requests.get("https://www.cricbuzz.com/cricket-series/5945/indian-premier-league-2023",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('div',{'class':'cb-col-100 cb-col'}):
     for b in a.find_all('div',{'class':'cb-col cb-col-100 cb-lst-itm cb-pos-rel cb-lst-itm-lg'}):
      for c in b.find_all('div',{'class':'cb-col cb-col-33 cb-pos-rel'}):
        for d in c.find_all('a'):
          for e in d.find_all('img'): 
            heading.append(e.get('title'))
    
    heading=heading[0:10]

    Url=[]
    for link in soup.find_all('div',{'class':'cb-col-100 cb-col'}):
        for lin in link.find_all('div',{'class':'cb-col cb-col-100 cb-lst-itm cb-pos-rel cb-lst-itm-lg'}):
         for li in lin.find_all('div',{'class':'cb-col cb-col-33 cb-pos-rel'}):
            for l in li.find_all('a'):
              Url.append("https://www.cricbuzz.com"+l.get('href'))
    
    Url = Url[0:10]

    Image=[]
    for n in soup.find_all('div',{'class':'cb-col-100 cb-col'}):
     for j in n.find_all('div',{'class':'cb-col cb-col-100 cb-lst-itm cb-pos-rel cb-lst-itm-lg'}):
      for i in j.find_all('div',{'class':'cb-col cb-col-33 cb-pos-rel'}):
          for k in i.find_all('a'):
            for l in k.find_all('img'):
              Image.append(l.get('src'))

    Image = Image[0:10]   

    employees=zip(Image, Url, heading)
    return render(request, 'news/ipl.html', {'employees':employees})    

def footballPage(request):
    r=requests.get("https://timesofindia.indiatimes.com/sports/football",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('ul',{'class':'cvs_wdt clearfix'}):
      for c in a.find_all('li'):
       for d in c.find_all('a',{'class':'w_img'}):
         heading.append(d.get('title'))
    
    heading=heading[0:10]

    Url=[]
    for links in soup.find_all('ul',{'class':'cvs_wdt clearfix'}):
     for link in links.find_all('li'):
        for lin in link.find_all('a',{'class':'w_img'}):
              Url.append("https://timesofindia.indiatimes.com/" + lin.get('href'))
    
    Url = Url[0:10]

    Image=[]
    for k in soup.find_all('ul',{'class':'cvs_wdt clearfix'}):
     for i in k.find_all('li'):
      for j in i.find_all('a',{'class':'w_img'}):
            for m in j.find_all('img'):
              Image.append(m.get('src'))

    Image = Image[0:10]   

    employees=zip(Image, Url, heading)
    return render(request, 'news/football.html', {'employees':employees})     

def tennisPage(request):
    r=requests.get("https://timesofindia.indiatimes.com/sports/tennis",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('ul',{'class':'cvs_wdt clearfix'}):
      for c in a.find_all('li'):
       for d in c.find_all('a',{'class':'w_img'}):
         heading.append(d.get('title'))
    
    heading=heading[0:10]

    Url=[]
    for links in soup.find_all('ul',{'class':'cvs_wdt clearfix'}):
     for link in links.find_all('li'):
        for lin in link.find_all('a',{'class':'w_img'}):
              Url.append("https://timesofindia.indiatimes.com/" + lin.get('href'))
    
    Url = Url[0:10]

    Image=[]
    for k in soup.find_all('ul',{'class':'cvs_wdt clearfix'}):
     for i in k.find_all('li'):
      for j in i.find_all('a',{'class':'w_img'}):
            for m in j.find_all('img'):
              Image.append(m.get('src'))

    Image = Image[0:10]   

    employees=zip(Image, Url, heading)
    return render(request, 'news/tennis.html', {'employees':employees})    

def NBAPage(request):
    r=requests.get("https://timesofindia.indiatimes.com/sports/nba",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('ul',{'class':'cvs_wdt clearfix'}):
      for c in a.find_all('li'):
       for d in c.find_all('a',{'class':'w_img'}):
         heading.append(d.get('title'))
    
    heading=heading[0:10]

    Url=[]
    for links in soup.find_all('ul',{'class':'cvs_wdt clearfix'}):
     for link in links.find_all('li'):
        for lin in link.find_all('a',{'class':'w_img'}):
              Url.append("https://timesofindia.indiatimes.com/" + lin.get('href'))
    
    Url = Url[0:10]

    Image=[]
    for k in soup.find_all('ul',{'class':'cvs_wdt clearfix'}):
     for i in k.find_all('li'):
      for j in i.find_all('a',{'class':'w_img'}):
            for m in j.find_all('img'):
              Image.append(m.get('src'))

    Image = Image[0:10]   

    employees=zip(Image, Url, heading)
    return render(request, 'news/NBA.html', {'employees':employees})     

def othsportsPage(request):
    r=requests.get("https://www.deccanherald.com/sports/other-sports",verify=False)
    soup=BeautifulSoup(r.content,'lxml')

    heading=[]
    for a in soup.find_all('div',{'class':'group'}):
      for c in a.find_all('div',{'class':' mtop-d-20 mtop-tl-20 inline w100'}):
       for d in c.find_all('div',{'class':'grid-col-half'}):
         for e in d.find_all('ul',{'class':'sm-hr-card-list '}):
            for f in e.find_all('li',{'class':'sm-hr-card-list__items mtop-m-20'}):
               for g in f.find_all('div',{'class':'sm-hr-card sm-hr-card--m-top'}):
                 for h in g.find_all('a'):
                    heading.append(h.get('data-vr-contentbox'))
    
    heading=heading[0:10]

    Url=[]
    for links in soup.find_all('div',{'class':'group'}):
     for link in links.find_all('div',{'class':' mtop-d-20 mtop-tl-20 inline w100'}):
        for lin in link.find_all('div',{'class':'grid-col-half'}):
            for li in lin.find_all('ul',{'class':'sm-hr-card-list '}):
                for l in li.find_all('li',{'class':'sm-hr-card-list__items mtop-m-20'}):
                  for lis in l.find_all('div',{'class':'sm-hr-card sm-hr-card--m-top'}):
                   for ls in lis.find_all('a'):
                     Url.append("https://www.deccanherald.com/" + ls.get('href'))
    
    Url = Url[0:10]

    Image=[]
    for k in soup.find_all('ul',{'class':'cvs_wdt clearfix'}):
     for i in k.find_all('li'):
      for j in i.find_all('a',{'class':'w_img'}):
            for m in j.find_all('img'):
              Image.append(m.get('src'))

    Image = Image[0:10]   

    employees=zip(Image, Url, heading)
    return render(request, 'news/othsports.html', {'employees':employees})     

@login_required(login_url='login')
def homePage(request):
        r=requests.get("https://indianexpress.com/section/india/",verify=False)
        soup=BeautifulSoup(r.content,'lxml')
        heading=soup.find_all('h2',{'class':'title'})
    
        heading=heading[0:10]
    
        Url=[]
        for link in soup.find_all('h2',{'class':'title'}):
           for l in link.find_all('a'):
             Url.append(l.get('href'))
    
        Url = Url[0:10]

        News=[]
        for news in heading:
            News.append(news.getText().strip())

        Image=[]
        for j in soup.find_all('div',{'class':'snaps'}):
            for k in j.find_all('img'):
                Image.append(k.get('src'))

         
        Image=Image[0:10]      
        
        employees=zip(Image,Url,News)

        s_image="https://wallpaperaccess.com/full/6170275.jpg"
        
        url3="https://www.mohfw.gov.in/"
        r3=requests.get(url3,verify=False)

        soup2 = BeautifulSoup(r3.content, 'html5lib')

        covid=[]

        for miter in soup2.find_all('span', {'class' : 'mob-show'}):
            for byiter in miter.find_all('strong'):
                covid.append(byiter.text)
        
        ACases=covid[0]
        DCases=covid[1]
        DeCases=covid[2]
        logo = "https://expressgroup.indianexpress.com/images/tie-logo.png"
        if "state-name" in request.GET:
            
            state=request.GET.get('state-name')
            var = request.GET.get('state-name')
            city= request.GET.get('state-name').replace('-',' ')
            url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=8257c3245fe46476bbb73f8920f1418e"
            x= requests.get(url,verify=False)
            y=x.json()
            City = f"{y['name']}"
            Temp = f"{math.trunc(y['main']['temp']-273.15)}°C"
            icon =  f"{y['weather'][0]['icon']}"
            Pressure = f"Pressure: {y['main']['pressure']} mb"
            Humidity = f"Humidity: {y['main']['humidity']}%"
            weather_condition = f"{y['weather'][0]['description']}".capitalize()

            if (state=="chhattisgarh" or state=="madhya-pradesh" or state=="rajasthan"):
                url=f"https://www.amarujala.com/{state}"
                r=requests.get(url,verify=False)
                soup = BeautifulSoup(r.content,'html5lib')

                News=[]
                for h in soup.find_all('div',{'class':'image_description'}):
                   for x in h.find_all('a'):
                      News.append(x.get('title'))

                News=News[0:10]
                Url=[]
                for link in soup.find_all('div',{'class':'image_description'}):
                  for l in link.find_all('a'):
                    Url.append("https://www.amarujala.com/" + l.get('href'))
    
                Url = Url[0:10]
                
                
                Image=[]
                # for main in soup.find_all('figure',{'class':'auw-lazy-load'}):
                for main in soup.find_all('div',{'class':'image'}):
                   for by in main.find_all('img'):
                       Image.append(by.get('src'))


                Image=Image[2:12]

                employees = zip(Image,Url,News)

                dict={
                  "chhattisgarh":"https://static.toiimg.com/photo/61783642/.jpg",
                  "madhya-pradesh":"https://wallpapercave.com/wp/wp10785224.jpg",
                  "rajasthan":"https://www.mapsofindia.com/maps/rajasthan/images/rajasthan.jpg",
                   }

                s_image = dict[state] 
                logo = "https://spiderimg.amarujala.com/assets/images/2018/01/19/750x506/amar-ujala-logo_1516333530.jpeg"

            elif (state=="andhra-pradesh" or state=="karnataka" or state=="kerala" or state=="tamil-nadu" or state=="telangana"):
               url2=f"https://www.thenewsminute.com/section/{state}"  
               r=requests.get(url2,verify=False)
               soup=BeautifulSoup(r.content, 'html5lib')
                
               News=[]
               for h in soup.find_all('h3',{'class':'article-title'}):
                    News.append(h.text.strip()) 
                
               News=News[4:14]

               Url=[]
               for link in soup.find_all('h3',{'class':'article-title'}):
                for t in link.find_all('a'):
                    Url.append(t.get('href'))
    
               Url = Url[4:14] 

               

               Image=[]
               for i in soup.find_all('div',{'class':'col-lg-6 col-3'}):
                for j in i.find_all('img'):
                   Image.append(j.get('src'))

               Image=Image[0:10] 

               employees = zip(Image,Url,News)

               dict={
                  "andhra-pradesh":"https://img.theculturetrip.com/1440x807/smart/wp-content/uploads/2016/06/24498998325_f451c67aae_o.jpg",
                  "karnataka":"https://wallpapercave.com/wp/wp8568701.jpg",
                  "kerala":"https://wallpapercave.com/dwp1x/wp7877523.jpg",
                  "tamil-nadu":"https://wallpapercave.com/wp/wp7626693.jpg",
                  "telangana":"https://img.theculturetrip.com/1440x807/smart/wp-content/uploads/2016/06/24498998325_f451c67aae_o.jpg",
                 }

               s_image = dict[state]
               logo = "https://www.thenewsminute.com/sites/default/files/branding-page/BrandStudioLogo.svg"
            elif (state=="assam" or state=="meghalaya" or state=="tripura" or state=="mizoram" or state=="manipur" or state=="nagaland" or state=="arunachal-pradesh" or state=="sikkim"):
                url=f"https://nenow.in/category/north-east-news/{state}"
                r=requests.get(url,verify=False)
                soup = BeautifulSoup(r.content,'html5lib')

                News=[]
                for h in soup.find_all('h2',{'class':'entry-title'}):
                   for x in h.find_all('a'):
                      News.append(x.getText())

                News=News[0:10]
                Url=[]
                for link in soup.find_all('h2',{'class':'entry-title'}):
                    for l in link.find_all('a'):
                      Url.append(l.get('href'))
    
                Url = Url[0:10]
                
                
                Image=[]
                for main in soup.find_all('a',{'class':'post-thumbnail-inner'}):
                   for by in main.find_all('img'):
                       Image.append(by.get('src'))


                Image=Image[0:10]

                employees = zip(Image,Url,News)

                dict={
                  "assam":"https://static.toiimg.com/photo/61783642/.jpg",
                  "meghalaya":"https://wallpapercave.com/wp/wp10785224.jpg",
                  "tripura":"https://images.travelandleisureasia.com/wp-content/uploads/sites/2/2023/02/17131051/Ujjayanta-Palace.jpg",
                  "mizoram":"https://wallpapercave.com/wp/wp10785224.jpg",
                  "manipur":"https://wallpapercave.com/wp/wp10785224.jpg",
                  "nagaland":"https://wallpapercave.com/wp/wp10785224.jpg",
                  "arunachal-pradesh":"https://wallpapercave.com/wp/wp10785224.jpg",
                  "sikkim":"https://wallpapercave.com/wp/wp10785224.jpg",
                   }

                s_image = dict[state]
                logo = "https://nenow.in/wp-content/uploads/2017/12/Logo_squre-1-80x80.png"
            else:
                url=f"https://www.jagran.com/state/{state}/"    
                r = requests.get(url,verify=False)
                soup = BeautifulSoup(r.content,'html5lib')
                heading1 = soup.find_all('div',{'class':'summary'})
                News=[]

                for t in heading1:
                    for u in t.find_all('p'):
                     News.append(u.text.strip())

                News=News[0:8]  
                
                Url=[]
                for link in soup.find_all('div',{'class':'summary'}):
                  for li in link.find_all('p'):
                    for l in li.find_all('a'):
                      Url.append(l.get('href'))
    
                Url = Url[0:8]
                
                

                #image=soup.find_all('img',{'class':'lazy'})
                Image=[]
                #base_url="https:"
                for image in soup.find_all('ul',{'class':'list'}):
                      for ima in image.find_all('li',{'class':'article'}):
                        for im in ima.find_all('figure'):
                          for i in im.find_all('a'):
                            for io in i.find_all('img',{'data-nimg':'intrinsic'}):
                              Image.append(io.get('alt'))
                
                Image=Image[0:16:2] 

                employees = zip(Image,Url,News)
                
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
                logo="https://www.freelogovectors.net/wp-content/uploads/2022/06/jagran-logo-freelogovectors.net_.png"

            url3="https://www.mohfw.gov.in/"
            r3=requests.get(url3,verify=False)

            soup2 = BeautifulSoup(r3.content, 'html5lib')

            covid=[]

            for miter in soup2.find_all('span', {'class' : 'mob-show'}):
                  for byiter in miter.find_all('strong'):
                     covid.append(byiter.text)
        
            ACases=covid[0]
            DCases=covid[1]
            DeCases=covid[2]

       
            return render(request, 'news/index.html', {'logo':logo,'employees':employees,'City': City,'Temp':Temp,'icon':icon,'Pressure':Pressure,'Humidity':Humidity,'weather_condition':weather_condition, 's_image': s_image , 'ACases' : ACases, 'DCases' : DCases, 'DeCases':DeCases, 'state':state})


        return render(request, 'news/index.html', {'logo':logo,'employees':employees, 's_image': s_image , 'ACases' : ACases, 'DCases' : DCases, 'DeCases':DeCases})


