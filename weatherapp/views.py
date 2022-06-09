from decouple import config
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
import requests
from pprint import pprint

from weatherapp.models import City #-json veriyi güzel gösterme için
#+js axios or fetch = python requests

def home(request):
    city = request.GET.get('city')
    API_key=config("API_KEY")
    print(city)
    if city:
        url =f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric'
        response = requests.get(url)
        if response.ok:
            content = response.json()
            my_city = content['name']
            if City.objects.filter(name=my_city):
                messages.info(request,f'{my_city} şehrinin hava durumu bilgilerine sahipsiniz.Lütfe başka bir şehir arayın😉":"You already know the weather for {my_city}, Please search for another city 😉')
            else:
                City.objects.create(name=my_city)
                messages.success(request,f'{my_city} added to the database')
            
        else :
            messages.warning(request,f'{city} is not a valid city')
        return redirect('home')
    
    city_list = []
    cities = City.objects.all()
    for city in cities:
        url =f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric'
        response = requests.get(url)
        content = response.json()
        data = {
                    "city":content['name'],
                    "id":city.id,
                    "temp":int(content['main']['temp']),
                    "desc":content['weather'][0]['description'],
                    "icon":content['weather'][0]['icon'],
         } 
        city_list.append(data)
    context = {
        "city_list":city_list,
    }

    
    return render(request, 'weatherapp/home.html',context)

def delete_city(request, id):
    city = get_object_or_404(City,id=id)
    city.delete()
    messages.success(request, 'City successfully deleted!')
    return redirect('home')