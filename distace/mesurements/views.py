from django.shortcuts import render , get_object_or_404
from .models import mesurementsofdistance
from .forms import MeasurementsForm
import folium
import requests
import re
from bs4 import BeautifulSoup
headers = {
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

# Create your views here.
def calculate(request):
     alert = False
     tell_dis = ''
     obj = get_object_or_404(mesurementsofdistance,  id=1)
     form = MeasurementsForm(request.POST or None)
     
     res = requests.get('https://ipinfo.io/')
     data = res.json()
     location = data['city']
     print(location)
     loc = data['loc']
     loc = loc.split(',')
     lat = float(loc[0])
     lon = float(loc[1])
     point=(float(loc[0]),float(loc[1]))
     
     m = folium.Map(
     location=point,
     width='80%',
     height='50%',
    )
     tooltip = 'Click me!'
     folium.Marker([lat, lon], popup=str(location), tooltip=tooltip,icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
      
     if form.is_valid():
         
        alert = True
        instance = form.save(commit=False)
        instance.destination = form.cleaned_data.get('destination')
        instance.location = location
        #######################LAN LON########################
        base = 'https://www.google.com/search?safe=active&rlz=1C1YQLS_enIN897IN897&sxsrf=ALeKk03dT5fURtWH9yNfIqP8pPmGuRbNOA%3A1608629982485&ei=3r7hX96XHc3QrQGs7ZTwAQ&q=latitude+and+longitude+of+'
        url1 = (base+form.cleaned_data.get('destination'))
        page = requests.get(url1, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        latlon = soup.find('div', attrs={'class':'Z0LcW XcVN5d'}).get_text()
        latlon = latlon.split(',')
        lat_des = re.findall("\d+\.\d+", latlon[0])
        lon_des = re.findall("\d+\.\d+", latlon[1])
        lat_des = float(''.join(lat_des))
        lon_des = float(''.join(lon_des))
        pointb = (lat_des,lon_des)
        ####################Get Distance#####################
        base = 'https://www.google.com/search?safe=active&rlz=1C1YQLS_enIN897IN897&biw=1366&bih=657&sxsrf=ALeKk02Y8GEcD4XWh64yCvecTCetld-HZQ%3A1608364202503&ei=qrDdX5WVHtSprtoPmu6HiA0&q=distance+between+'
        url = (base+location+'+and+'+str(form.cleaned_data.get('destination')))	
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        price = soup.find('span', attrs={'class':'UdvAnf'}).get_text() 
        
        temp = re.sub('^.*\((.*?)\)[^\(]*$', '\g<1>', price)
        temp = temp.replace(',', '')
        temp1 = re.findall("\d+\.\d+", temp)
        distance = round(float(''.join(temp1)))
        ###################################
        
        m = folium.Map(
        location=point,
        width='80%',
        height='50%',
        )
       
        tooltip = 'Click me!'
        folium.Marker([lat, lon], popup=str(location), tooltip=tooltip,icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
       
        folium.Marker([lat_des, lon_des], popup=str(form.cleaned_data.get('destination')), tooltip=tooltip,icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)
       
        line = folium.PolyLine(locations=[point,pointb],weight=5,color='blue')
        m.add_child(line)
        
        ###################################
        instance.distance = distance 
        instance.save()
        tell_dis = mesurementsofdistance.objects.filter().order_by('-id')[0]
        print(tell_dis)

     
     m = m._repr_html_()
     
     context = {
         
         'form':form,
         'map':m,
         'alert':alert,
         'actual_dis':tell_dis
     }    
     
     return render(request,'mesurements/main.html',context)