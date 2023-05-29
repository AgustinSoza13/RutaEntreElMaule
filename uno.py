import streamlit as st
import json
import folium
from streamlit_folium import  st_folium
class Api:
    def __init__(self,rutas,paraderos):
        self.rutas=rutas
        self.paraderos=paraderos
        self.vertice=[]
        self.coordenas=[]
        self.columna = []
        self.mapa = folium.Map(location=[-35.4264000, -71.6554200], zoom_start=10)
    

    def lectura(self):
        with open(self.rutas,encoding='utf-8') as archivo:
            datos_geojson = json.load(archivo)
        for feature in datos_geojson['features']:
            valor = feature['geometry']['coordinates']
            self.columna.append(valor)
    def procesoRutas(self):
        for i in self.columna:
            trail_coordinates=[]
            for j in i:
                latitud=j[1]
                longitud=j[0]
                cambio=latitud,longitud
                trail_coordinates.append(cambio)
            polilinea = folium.PolyLine(locations=trail_coordinates, color='red') 
            self.mapa.add_child(polilinea)#agrgamos un objeto secundario al mapa es un hijo   

    def lecturaDos(self):
        with open(self.paraderos,encoding='utf-8') as archivo:
            datos_geojson = json.load(archivo)
        for feature in datos_geojson['features']:
            valor = feature['geometry']['coordinates']
            if valor[0] != None or valor[1]!=None:
                self.vertice.append(valor)    
            else:
                pass
        #print(self.vertice)
    def markerLinea(self):
        for i in self.vertice:
            latitud=i[1]
            longitud=i[0]
            cambio=latitud,longitud
            self.coordenas.append({'lat':latitud ,'lon':longitud})
        #print(self.coordenas)  
        for i in self.coordenas:
            icono_propio=folium.CustomIcon('parada.png',icon_size=(30,30))
            folium.Marker(location=[i['lat'],i['lon']],popup='paradero',icon=icono_propio).add_to(self.mapa)
    def run(self):
        self.lectura()
        self.procesoRutas()
        self.lecturaDos()
        self.markerLinea()
        st_folium(self.mapa,width=700,height=700)
        #st(self.mapa)#renderizar la pagina
if __name__ == '__main__':
    mapita=Api('maule.geojson','map.geojson')
    mapita.run()



