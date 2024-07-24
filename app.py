import streamlit as st
import requests

key = st.secrets.some_magic_api.key


st.write('Welcome to my app')

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:

date and time
pickup longitude
pickup latitude
dropoff longitude
dropoff latitude
passenger_count
'''

pickup_datetime = st.text_input("Enter pickup_datetime", "2014-07-06 19:18:00")
pickup_longitude = st.text_input("Enter pickup_longitude", "-73.950655")
pickup_latitude = st.text_input("Enter pickup_latitude", "40.783282")
dropoff_longitude = st.text_input("Enter dropoff_longitude", "-73.984365")
dropoff_latitude = st.text_input("Enter dropoff_latitude", "40.769802")
passenger_count = st.number_input("Enter passenger_count", min_value=1, max_value=10, value=2)


'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare.lewagon.ai/predict'#API Endpoint

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...'''
params = {
       'pickup_datetime': [pickup_datetime],
       'pickup_longitude': [pickup_longitude],
       'pickup_latitude': [pickup_latitude],
       'dropoff_longitude': [dropoff_longitude],
       'dropoff_latitude': [dropoff_latitude],
       'passenger_count': [passenger_count]}

'''
3. Let's call our API using the `requests` package...
'''
response = requests.get(url,params=params)

'''
4. Let's retrieve the prediction from the **JSON** returned by the API...
'''
# Parse the response
prediction = response.json()
fare = prediction["fare"]

'''
## Finally, we can display the prediction to the user
'''
st.write(f"Estimated Taxi Fare: ${fare}")
