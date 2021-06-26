from django.shortcuts import render,redirect,reverse
from .models import *
from django.http import HttpResponse
from urllib.request import urlopen,Request,urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import shutil
import requests
import re

# Create your views here.


def index(request):

	movieList=Movie.objects.all()

	context={'movieList':movieList}
	get_src()

	return render(request,'recent_movies/index.html',context)

'''
def movieDetail(request,name):
	movie=Movie.objects.get(name=name)
	castaward=movie.castaward.all()
	context={'movie':movie,'castaward':castaward}

	return render(request,'recent_movies/movie.html',context)
'''
def get_src(url="https://yts.mx/"):

    try:
        req=Request(url,headers={"User-Agent":"Mozilla/5.0"})
        html=urlopen(req)
    except HTTPError as e:
        print(e)
        return None
    try:
        bsobj=BeautifulSoup(html,"html.parser")
        latest=bsobj.find("div",{"class":"content-dark"}).findAll("img",{"src":re.compile("\/assets\/images\/movies\/[a-z_0-9]+\/medium-cover\.jpg")})
        popular=bsobj.find("div",{"class":"container home-content"}).findAll("img",{"src":re.compile("\/assets\/images\/movies\/[a-z_0-9]+\/medium-cover\.jpg")})

        for image in latest:
            name=image['alt'].replace('download','').replace(' ','_')+'.jpg'
            imageurl="https://yts.mx"+image['src']
            response=requests.get(imageurl,stream=True)
            with open(name,'wb') as out_file:
            	shutil.copyfileobj(response.raw,out_file)
            del response
            shutil.move('/home/saurabh/GIT/yts_recent_movies/'+name,'/home/saurabh/GIT/yts_recent_movies/static/image/'+name)
            Movie.objects.get_or_create(name=name[:-5].replace('_',' '),image=name)


        for image in popular:
            name=image['alt'].replace('download','').replace(' ','_')+'.jpg'
            imageurl="https://yts.mx"+image['src']
            response=requests.get(imageurl,stream=True)
            with open(name,'wb') as out_file:
                shutil.copyfileobj(response.raw,out_file)
            del response
            shutil.move('/home/saurabh/GIT/yts_recent_movies/'+name,'/home/saurabh/GIT/yts_recent_movies/static/image/'+name)
            Movie.objects.get_or_create(name=name[:-5].replace('_',' '),image=name)
	            

    except AttributeError as e:
        print(e)
