import streamlit as st

import numpy as np
import pandas as pd
import sklearn
import requests
from datetime import date,timedelta
import datetime
from  pages._historical_data import combined_data
import time
import pydeck as pdk

cities_df = pd.read_csv("cities_df.csv")


col=st.columns([1.5,1])
today  = date.today()

st.header("Past/Historical")
colA, colB,colC = st.columns([1.5,1,1], gap="small", vertical_alignment="center")
with colA:
        city= st.selectbox("Select city", cities_df["City"], key="city1")
        
        selected= cities_df[cities_df["City"] == city].iloc[0]
        lat=selected['Latitude']
        lon=selected['Longitude']
with colB:
           start_date=st.date_input("select start date",value=today - datetime.timedelta(days=10),max_value=today - datetime.timedelta(days=3))
           
                    
with colC:
           end_date = st.date_input("select end date",max_value=today - datetime.timedelta(days=3))
           y_Pred1=combined_data(start_date, end_date, city, lat, lon)

st.warning("Don't select long date range((it may dificult to display) ")

col_x, col_y= st.columns([1.3,1.1], gap="small")  




with col_x:
           with st.spinner("Wait for it...", show_time=True):
                time.sleep(2)
                st.badge("Success", icon=":material/check:", color="green")
                st.subheader("weather report")
                
                for index, row in y_Pred1.iterrows():
                            with st.container(border=True):  # Requires Streamlit >= 1.32
                                col1, col2,col3= st.columns([1.5,1,1])
                                with col1:
                                    st.metric("Date",row['datetime'])
                                    st.markdown(f"Date : {row['datetime']}")
                                with col2:
                                    st.metric("tempmax",row['tempmax'],row['tempmax_diff'])
                                    
                                with col3:

                                    st.metric("tempmin",row['tempmin'],row['tempmax_diff'])

with col_y:
            st.subheader("Temp. min/max plot")
            st.line_chart(
            y_Pred1,
            x="datetime",
            y=["tempmax", "tempmin"],
            color=["#FF0000", "#0000FF"],)

            st.subheader("Available cities info")
            st.dataframe(cities_df)
             
            st.subheader("weather of following coordinate")
      

            # Create a new DataFrame with just the selected city
            selected_city_df = pd.DataFrame({
                "City": [city],
                "lat": [lat],
                "lon": [lon]
            })

            # Show pydeck chart focused on selected city
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=lat,
                    longitude=lon,
                    zoom=8,
                    pitch=50,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=selected_city_df,
                        get_position='[lon, lat]',
                        get_color='[255, 0, 0, 180]',  # red
                        get_radius=30000,
                        pickable=True
                    )
                ],
                tooltip={"text": "📍 {City}"}
            ),height=370)