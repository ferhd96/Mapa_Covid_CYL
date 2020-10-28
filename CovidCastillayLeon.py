
# coding: utf-8

# ### Autores:
# #### Francisco Alonso Fernández. Data Scientist en Future Space.
# #### Fernando Hernandez de Vega. Técnico Gis en Cirosip.

# In[1]:


from IPython.display import HTML

HTML('''
<script>code_show=true; 

function code_toggle() {
    if (code_show){
    $('div.input').hide();
    } else {
    $('div.input').show();
    }
    code_show = !code_show
} 

$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="Haz click para ver el código."></form>
''')


# In[2]:


## Importamos las librerías necesarias

import requests
import pandas as pd

from datetime import date
import datetime
import json
import folium

## Obtenemos la fecha actual

today = date.today()

days = datetime.timedelta(1)


# In[3]:


## Usando una url formada con la fecha actual obtenemos los datos de hoy mediante una petición a la api

url_basic = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/search/?dataset=situacion-epidemiologica-coronavirus-en-castilla-y-leon&q=&facet=fecha&facet=provincia&refine.fecha="
url = url_basic+str(today.year)+'%2F'+str(today.month)+'%2F'+str(today.day)

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)
my_data = response.json()


# In[4]:


## Tenemos dos condiciones: que hoy hayan actualizado datos o no
## esto es así porque los días festivos puede que no haya actualizaciones en los mismos
## en el caso de que no haya actualizaciones se toman los datos del día anterior

## Para comprobar los campos simplemente vemos que uno de los campos del json que devuelve la petición tiene el valor
## que debería 

if my_data['nhits']>0:
    
    ## Formamos un dataframe con la información contenida en el Json
    
    provincias = [my_data['records'][x]['fields']['provincia'] for x in range(len(my_data['records']))]
    nuevos_positivos = [my_data['records'][x]['fields']['nuevos_positivos'] for x in range(len(my_data['records']))]
    altas = [my_data['records'][x]['fields']['altas'] for x in range(len(my_data['records']))]
    fallecimientos = [my_data['records'][x]['fields']['fallecimientos'] for x in range(len(my_data['records']))]
    casos_confirmados = [my_data['records'][x]['fields']['casos_confirmados'] for x in range(len(my_data['records']))]
    fecha = [my_data['records'][x]['fields']['fecha'] for x in range(len(my_data['records']))]
    my_dict = {'provincias' : provincias, 'nuevos_positivos' : nuevos_positivos, 'altas' : altas, 'fallecimientos' : fallecimientos, 'casos_confirmados' : casos_confirmados, 'fecha' : fecha}
    df = pd.DataFrame(my_dict)
    
    ## Leemos el geojson, que contiene la información necesaria para pintar las coropletas
    
    geo = 'https://raw.githubusercontent.com/ferhd96/Mapa_Covid_CYL/main/GEOJSON.geojson'
    
    m = folium.Map(location=[42, -4], zoom_start=7)
    
    ## Mediante folium realizamos el mapa

    folium.Choropleth(
        geo_data=geo,
        name='choropleth',
        data=df,
        columns=['provincias', 'nuevos_positivos'],
        key_on='feature.properties.texto_alt',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name ='Created by: Francisco Alonso y Fernando Hernadez.').add_to(m)
    
    ## Una vez tenemos el mapa añadimos los marcadores en las coordenadas de cada provincia
    ## con la información dinámica obtenida del dataframe
    ## además, como marcador usamos una imagen de la que pasamos la url
    
    ## ÁVILA. Nota: La salida del mapa da problemas con las tildes
    
    folium.LayerControl().add_to(m)
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([40.55, -4.9], popup='<h3> Avila: </h3>'+'<p>'+str(today)+'</p>'+'<p>-'+str(df[df.provincias=='Ávila']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Ávila']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Ávila']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Ávila']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    
    ## SALAMANCA
    
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([40.9, -5.6], popup='<h3> Salamanca: </h3>'+'<p>'+str(today)+'</p>'+'<p>-'+str(df[df.provincias=='Salamanca']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Salamanca']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Salamanca']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Salamanca']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    
    ## ZAMORA
    
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([41.5, -5.74], popup='<h3> Zamora: </h3>'+'<p>'+str(today)+'</p>'+'<p>-'+str(df[df.provincias=='Zamora']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Zamora']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Zamora']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Zamora']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    
    ## LEÓN. Nota: La salida del mapa da problemas con las tildes
    
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([42.59, -5.56], popup='<h3> Leon: </h3>'+'<p>'+str(today)+'</p>'+'<p>-'+str(df[df.provincias=='León']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='León']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='León']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='León']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    
    ## PALENCIA
    
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([42.15, -4.53], popup='<h3> Palencia: </h3>'+'<p>'+str(today)+'</p>'+'<p>-'+str(df[df.provincias=='Palencia']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Palencia']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Palencia']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Palencia']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    
    ## BURGOS
    
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([42.34, -3.69], popup='<h3> Burgos: </h3>'+'<p>'+str(today)+'</p>'+'<p>-'+str(df[df.provincias=='Burgos']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Burgos']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Burgos']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Burgos']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    
    ## SORIA
    
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([41.76, -2.46], popup='<h3> Soria: </h3>'+'<p>'+str(today)+'</p>'+'<p>-'+str(df[df.provincias=='Soria']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Soria']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Soria']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Soria']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    
    ## SEGOVIA
    
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([40.94, -4.11], popup='<h3> Segovia: </h3>'+'<p>'+str(today)+'</p>'+'<p>-'+str(df[df.provincias=='Segovia']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Segovia']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Segovia']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Segovia']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    
    ## VALLADOLID
    
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([41.63, -4.71], popup='<h3> Valladolid: </h3>'+'<p>'+str(today)+'</p>'+'<p>-'+str(df[df.provincias=='Valladolid']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Valladolid']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Valladolid']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Valladolid']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    
    ## Repetimos un proceso totalmente análogo pero con los datos de la fecha de ayer
    ## por si los de hoy no estuvieran disponibles
    
    
else:
    
    ## Repetimos un proceso totalmente análogo pero con los datos de la fecha de ayer
    ## por si los de hoy no estuvieran disponibles
    
    yesterday = today-days
    url_basic = "https://analisis.datosabiertos.jcyl.es/api/records/1.0/search/?dataset=situacion-epidemiologica-coronavirus-en-castilla-y-leon&q=&facet=fecha&facet=provincia&refine.fecha="
    url = url_basic+str(yesterday.year)+'%2F'+str(yesterday.month)+'%2F'+str(yesterday.day)

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)
    my_data = response.json()
    provincias = [my_data['records'][x]['fields']['provincia'] for x in range(len(my_data['records']))]
    nuevos_positivos = [my_data['records'][x]['fields']['nuevos_positivos'] for x in range(len(my_data['records']))]
    altas = [my_data['records'][x]['fields']['altas'] for x in range(len(my_data['records']))]
    fallecimientos = [my_data['records'][x]['fields']['fallecimientos'] for x in range(len(my_data['records']))]
    casos_confirmados = [my_data['records'][x]['fields']['casos_confirmados'] for x in range(len(my_data['records']))]
    fecha = [my_data['records'][x]['fields']['fecha'] for x in range(len(my_data['records']))]
    my_dict = {'provincias' : provincias, 'nuevos_positivos' : nuevos_positivos, 'altas' : altas, 'fallecimientos' : fallecimientos, 'casos_confirmados' : casos_confirmados, 'fecha' : fecha}
    df = pd.DataFrame(my_dict)
    
    geo = 'https://raw.githubusercontent.com/ferhd96/Mapa_Covid_CYL/main/GEOJSON.geojson'
    
    m = folium.Map(location=[42, -4], zoom_start=7)

    folium.Choropleth(
        geo_data=geo,
        name='choropleth',
        data=df,
        columns=['provincias', 'nuevos_positivos'],
        key_on='feature.properties.texto_alt',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name ='Created by: Francisco Alonso y Fernando Hernadez.').add_to(m)
    
    folium.LayerControl().add_to(m)
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([40.55, -4.9], popup='<h3> Avila: </h3>'+'<p>'+str(yesterday)+'</p>'+'<p>-'+str(df[df.provincias=='Ávila']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Ávila']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Ávila']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Ávila']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([40.9, -5.6], popup='<h3> Salamanca: </h3>'+'<p>'+str(yesterday)+'</p>'+'<p>-'+str(df[df.provincias=='Salamanca']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Salamanca']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Salamanca']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Salamanca']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([41.5, -5.74], popup='<h3> Zamora: </h3>'+'<p>'+str(yesterday)+'</p>'+'<p>-'+str(df[df.provincias=='Zamora']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Zamora']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Zamora']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Zamora']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([42.59, -5.56], popup='<h3> Leon: </h3>'+'<p>'+str(yesterday)+'</p>'+'<p>-'+str(df[df.provincias=='León']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='León']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='León']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='León']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([42.15, -4.53], popup='<h3> Palencia: </h3>'+'<p>'+str(yesterday)+'</p>'+'<p>-'+str(df[df.provincias=='Palencia']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Palencia']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Palencia']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Palencia']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([42.34, -3.69], popup='<h3> Burgos: </h3>'+'<p>'+str(yesterday)+'</p>'+'<p>-'+str(df[df.provincias=='Burgos']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Burgos']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Burgos']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Burgos']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([41.76, -2.46], popup='<h3> Soria: </h3>'+'<p>'+str(yesterday)+'</p>'+'<p>-'+str(df[df.provincias=='Soria']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Soria']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Soria']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Soria']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([40.94, -4.11], popup='<h3> Segovia: </h3>'+'<p>'+str(yesterday)+'</p>'+'<p>-'+str(df[df.provincias=='Segovia']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Segovia']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Segovia']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Segovia']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)
    icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(30, 30),
    icon_anchor=(15, 15),
    popup_anchor=(0.1, -0.1))
    folium.Marker([41.63, -4.71], popup='<h3> Valladolid: </h3>'+'<p>'+str(yesterday)+'</p>'+'<p>-'+str(df[df.provincias=='Valladolid']['nuevos_positivos'].tolist()[0])+                  ' nuevos positivos.</p>'+'<p>-'+str(df[df.provincias=='Valladolid']['altas'].tolist()[0])+' altas.</p>'+                  '<p>-'+str(df[df.provincias=='Valladolid']['fallecimientos'].tolist()[0])+' fallecimientos.</p>'+                  '<p>-'+str(df[df.provincias=='Valladolid']['casos_confirmados'].tolist()[0])+' casos confirmados.</p>',  
               icon=icon).add_to(m)


# In[5]:


m

