import streamlit as st
import requests
import datetime
import streamlit.components.v1 as components

#kaggle dataset https://www.kaggle.com/datasets/dhruvildave/new-york-city-taxi-trips-2019/data


key = st.secrets.some_magic_api.key

st.title('Conoce tu precio')

st.markdown('''****Aplicación de demostración para API productiva de estimación de precios****''')
mapbox_api_key = st.secrets.some_magic_api.mapbox_api_key


##################### MAPA #####################
map_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Simple Map</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <script src="https://api.mapbox.com/mapbox-gl-js/v2.3.1/mapbox-gl.js"></script>
    <link href="https://api.mapbox.com/mapbox-gl-js/v2.3.1/mapbox-gl.css" rel="stylesheet" />
    <style>
        body {{ margin: 0; padding: 0; }}
        #map {{ position: absolute; top: 0; bottom: 0; width: 100%; }}
    </style>
</head>
<body>
<div id="map" style="height: 100vh;"></div>
<script>
mapboxgl.accessToken = '{mapbox_api_key}';
var map = new mapboxgl.Map({{
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [-73.950655, 40.783282],
    zoom: 10
}});
</script>
</body>
</html>
"""

components.html(map_html, height=500)

##############################################################


'''
Ingrese datos
'''

with st.form(key='APIparams'):
    #pickup_datetime = st.date_input("Hora requerida servicio", "2014-07-06 19:18:00")
    pickup_date = st.date_input("Fecha requerida servicio", value=datetime.date(2014, 7, 6))
    pickup_time = st.time_input("Hora requerida servicio", value=datetime.time(19, 18, 00))
    pickup_datetime = datetime.datetime.combine(pickup_date, pickup_time)#alternativa f'{pickup_date} {pickup_time}'
    pickup_longitude = st.number_input('longitude recogida', value=-73.950655)
    pickup_latitude = st.number_input("Latitude recogida", value=40.783282)
    dropoff_longitude = st.number_input("Longitud destino", value=-73.984365)
    dropoff_latitude = st.number_input("Latitud destino", value=40.769802)
    passenger_count = st.number_input("Núumero de pasajeros]", min_value=1, max_value=10, value=2)

    estimar = st.form_submit_button('Estimar')
    if estimar:

        #See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

        url = 'https://taxifare.lewagon.ai/predict'#API Endpoint

        params = {
            'pickup_datetime': pickup_datetime,
            'pickup_longitude': [pickup_longitude],
            'pickup_latitude': [pickup_latitude],
            'dropoff_longitude': [dropoff_longitude],
            'dropoff_latitude': [dropoff_latitude],
            'passenger_count': [passenger_count]}

        response = requests.get(url,params=params)


        #4. Let's retrieve the prediction from the **JSON** returned by the API...

        # Parse the response
        prediction = response.json()
        fare = prediction["fare"]

        '''
        ## Tarifa estimada
        '''
        st.write(f"Estimated Taxi Fare: ${round(fare,2)}")
        #st.write(params)

        #####################

        # Coordenadas de inicio y destino
        start_coords = (pickup_longitude, pickup_latitude)
        end_coords = (dropoff_longitude, dropoff_latitude)

        # URL de la API de Mapbox Directions
        url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}?geometries=geojson&access_token={mapbox_api_key}"
        response = requests.get(url)
        directions = response.json()

        # Extrae la ruta (geojson) de la respuesta
        route = directions['routes'][0]['geometry']


        # Muestra la distancia y la duración
        distance = directions['routes'][0]['distance'] / 1000  # en kilómetros
        duration = directions['routes'][0]['duration'] / 60  # en minutos

        st.write(f"Distancia: {distance:.2f} km")
        st.write(f"Duración: {duration:.2f} minutos")
