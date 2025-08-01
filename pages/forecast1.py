import streamlit as st

import numpy as np
import pandas as pd
import requests
from datetime import date,timedelta
import datetime
from  pages.model1 import combined_data,date_data
from pages.model2 import combined_data0
import time
import pydeck as pdk

cities_df = pd.read_csv("cities_df.csv")
tab1,tab2 = st.tabs(["Model 1.1","Model 1.0"])
today  = date.today()




with tab1:
        st.header("Current/Forecast")
        col1, col2 = st.columns([1.3,1.1], gap="small")
        with col1:
           city_model1= st.selectbox("Select city", cities_df["City"], key="city1")
           selected_model1= cities_df[cities_df["City"] == city_model1].iloc[0]
           lat1=selected_model1['Latitude']
           lon1=selected_model1['Longitude']
        with col2:
           model1_start_date=st.date_input( "date (fixed to today)",value=today,min_value=today,max_value=today,key="date1")
           
           start_vc, end_vc, start_open, end_open, city, lat, lon=date_data(model1_start_date,city_model1,lat1,lon1)
           y_Pred1=combined_data(start_vc, end_vc, start_open, end_open, city, lat, lon)


        col_x, col_y= st.columns([1.3,1.1], gap="small")  
        
        with col_x:
           with st.spinner("Wait for it...", show_time=True):
                time.sleep(2)
                st.badge("Success", icon=":material/check:", color="green")
                st.subheader("weather report")
                for index, row in y_Pred1.iterrows():
                            with st.container(border=True):  # Requires Streamlit >= 1.32
                                col1, col2,col3,col4= st.columns([1.5,1,1,1])
                                with col1:
                                    st.metric("Date",row['datetime'])
                                   
                                with col2:
                                    st.metric("tempmax",row['tempmax'],row['tempmax_diff'])
                                    
                                with col3:
                                    st.metric("tempmin",row['tempmin'],row['tempmax_diff'])
                                with col4:
                                    if row["icon"] == "rain":
                                        st.image("image/raining-morning.png",width=50)
                                        st.markdown("Rainy")
                                    elif row["icon"] == "partly-cloudy-day":
                                        st.image("image/partly-cloudy-morning.png",width=50)
                                        st.markdown("Partly-cloudy")
                                    elif row["icon"] == "clear-day":
                                        st.image("image/clear1.png",width=50)
                                        st.markdown("Clear_day")
                                    elif row["icon"] == "cloudy":
                                        st.image("image/cloudy-morning.png",width=50)
                                        st.markdown("Cloudy")
                                    elif row["icon"] == "wind":
                                        st.image("image/windy-day.png",width=50)
                                        st.markdown("Windy")
                                    else: 
                                        st.text("error in data")
                                        st.markdown("inform developer !")

        with col_y:
            st.subheader("Temp. min/max plot")
            st.line_chart(
            y_Pred1,
            x="datetime",
            y=["tempmax", "tempmin"],
            color=["#FF0000", "#0000FF"],)

            st.subheader("Available cities info")
            st.dataframe(cities_df,height=260)

             
            st.subheader("weather of following coordinate")

            # Create a new DataFrame with just the selected city
            selected_city_df = pd.DataFrame({
                "City": [city_model1],
                "lat": [lat1],
                "lon": [lon1]
            })

            # Show pydeck chart focused on selected city
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=lat1,
                    longitude=lon1,
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
            


                    
with tab2:
        st.header("Current/Forecast")
        colA, colB,colC = st.columns([1.3,1,1], gap="small")
        with colA:
            city_model2= st.selectbox("Select city", cities_df["City"], key="city2")
            selected_model2= cities_df[cities_df["City"] == city_model2].iloc[0]
            lat2=selected_model2['Latitude']
            lon2=selected_model2['Longitude']


        with colB:
            model10_start_date=st.date_input( "Date (fixed to today)",value=today,max_value=today,key="date2")
          

        with colC:
            model10_end_date = st.date_input("select end date",min_value=model10_start_date + datetime.timedelta(days=7),max_value=model10_start_date + datetime.timedelta(days=7))
            y_pred2=combined_data0(model10_start_date,model10_end_date, city_model2)

        
        col_x1, col_y2= st.columns([1.3,1.1], gap="small")  
        
        with col_x1:
           with st.spinner("Wait for it...", show_time=True):
                time.sleep(2)
                st.badge("Success", icon=":material/check:", color="green")
                st.subheader("weather report")
                for index, row in y_pred2.iterrows():
                            with st.container(border=True):  # Requires Streamlit >= 1.32
                                col1, col2,col3,col4= st.columns([1.5,1,1,0.5])
                                with col1:
                                    st.metric("Date",row['datetime'])
                                    
                                with col2:
                                    st.metric("tempmax",row['tempmax'],row['tempmax_diff'])
                                    
                                with col3:
                                    st.metric("tempmin",row['tempmin'],row['tempmax_diff'])
                                with col4:
                                    if row["icon"] == "rain":
                                        st.image("image/raining-morning.png",width=50)
                                        st.markdown("Rainy")
                                    elif row["icon"] == "partly-cloudy-day":
                                        st.image("image/partly-cloudy-morning.png",width=50)
                                        st.markdown("Partly-cloudy")
                                    elif row["icon"] == "clear-day":
                                        st.image("image/clear1.png",width=50)
                                        st.markdown("Clear_day")
                                    elif row["icon"] == "cloudy":
                                        st.image("image/cloudy-morning.png",width=50)
                                        st.markdown("Cloudy")
                                    elif row["icon"] == "wind":
                                        st.image("image/windy-day.png",width=50)
                                        st.markdown("Windy")
                                    else: 
                                        st.text("error in data")
                                        st.markdown("inform developer !")

        with col_y2:
            st.subheader("Temp. min/max plot")
            st.line_chart(
            y_pred2,
            x="datetime",
            y=["tempmax", "tempmin"],
            color=["#FF0000", "#0000FF"],)

            st.subheader("Available cities info")
            st.dataframe(cities_df,height=260)

             
            st.subheader("weather of following coordinate")

            # Create a new DataFrame with just the selected city
            selected_city_df = pd.DataFrame({
                "City": [city_model2],
                "lat": [lat2],
                "lon": [lon2]
            })

            # Show pydeck chart focused on selected city
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=lat2,
                    longitude=lon2,
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
                    
                










   
   


