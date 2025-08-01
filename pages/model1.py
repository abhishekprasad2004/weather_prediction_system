import streamlit as st
from datetime import timedelta
import numpy as np
import pandas as pd
import requests
import sklearn
from datetime import date


def combined_data0(start_date, end_date, city):
    # Unpack all needed dates from the function
    
    def retrive_vc(start_vc, end_vc):
        api_key = "4VTKTZNKFQQKWGRRMAYD64JNV"
        url_vc = (
            f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/"
            f"timeline/{city}/{start_vc}/{end_vc}?unitGroup=metric&include=days"
            f"&key={api_key}&contentType=json"
        )
        response = requests.get(url_vc)
        data_vc = response.json()
        weather_data = pd.json_normalize(data_vc["days"])
        weather_data["city"] = city
        return weather_data
    
    weather_data = retrive_vc(start_date, end_date)
 
    weather_data.rename(columns={"time": "datetime",
                  "temperature_2m_max": "tempmax",
                  "temperature_2m_min": "tempmin",
                  "apparent_temperature_max": "feelslikemax",
                   "apparent_temperature_min": "feelslikemin",
                   "snowfall_sum": "snow",
                   "precipitation_sum": "precip",
                   "windspeed_10m_max": "windspeed",
                   "windgusts_10m_max": "windgust",
                   "shortwave_radiation_sum":"solarenergy",},inplace= True)
    
    weather = weather_data.copy()
    weather= weather[["datetime","tempmax","tempmin","feelslikemax","feelslikemin","snow","precip","windspeed","windgust","solarenergy","city"]]
    
   # 3-day rolling average of feelslike max and feelslike min temperature
    weather['feelslikemax_roll3'] = weather['feelslikemax'].rolling(window=3).mean()
    weather['feelslikemin_roll3'] = weather['feelslikemin'].rolling(window=3).mean()

    # 3-day rolling precipitation sum
    weather['precip_roll3'] = weather['precip'].rolling(window=3).sum()

    #fill nan value of starting 2 column as they donot have previous 3 days value
    weather['feelslikemax_roll3'] = weather['feelslikemax_roll3'].fillna(weather['feelslikemax'])
    weather['feelslikemin_roll3'] = weather['feelslikemin_roll3'].fillna(weather['feelslikemin'])

    weather['precip_roll3'] = weather['precip_roll3'].fillna(weather['precip'])


    weather['datetime'] = pd.to_datetime(weather['datetime'])
    weather["day"] =weather["datetime"].dt.day
    weather["months"] = weather["datetime"].dt.month
    weather["year"] = weather["datetime"].dt.year

    bins = [0,1,3,6,9,11,12]
    labels =["winter","spring","summer","monsoon","autumn","winter"]
    weather["seasons"] = pd.cut(weather["months"],bins =bins,labels=labels,ordered=False)

    from sklearn.preprocessing import LabelEncoder
    weather_col =["city","day","months","year","seasons"]

    for col in weather_col:
        le = LabelEncoder()
        weather[col] = le.fit_transform(weather[col])
    weather = weather[["feelslikemax","feelslikemin","snow","precip","windspeed","windgust","solarenergy","city",'feelslikemax_roll3','feelslikemin_roll3','precip_roll3',"day","months","year","seasons"]]

    from sklearn.preprocessing import StandardScaler
    scaler =StandardScaler()
    weather = scaler.fit_transform(weather)

    import pickle
    predictor = pickle.load(open("model3.pkl","rb"))
    y_pred=predictor.predict(weather)
    y_test= weather_data[["tempmax","tempmin"]]

    from sklearn import metrics
    np.sqrt(metrics.mean_squared_error(y_test,y_pred))

    y_pred_df = pd.DataFrame(y_pred)
    y_pred_df.columns=["tempmax","tempmin"]
    y_pred_df["tempmax"] = y_pred_df["tempmax"].map("{:.2f}".format)
    y_pred_df["tempmin"] = y_pred_df["tempmin"].map("{:.2f}".format)
    
    y_pred_df = y_pred_df.round(2)
    np.sqrt(metrics.mean_squared_error(y_test,y_pred_df)) #error between actual and predicted value
    
    y_pred_df["datetime"] =  weather_data["datetime"]
    
    y_pred_df["icon"] = weather_data["icon"]
    y_pred_new1 = y_pred_df[["datetime","tempmax","tempmin","icon"]]

    y_pred_new1["tempmax"] = pd.to_numeric(y_pred_new1["tempmax"], errors='coerce')
    y_pred_new1["tempmin"] = pd.to_numeric(y_pred_new1["tempmin"], errors='coerce')

    y_pred_new1["tempmax_diff"] = y_pred_new1["tempmax"].diff().fillna(0).map("{:.2f}".format)
    y_pred_new1["tempmin_diff"] = y_pred_new1["tempmin"].diff().fillna(0).map("{:.2f}".format)
    y_pred_new1[['tempmax_diff',"tempmin_diff"]]=y_pred_new1[['tempmax_diff',"tempmin_diff"]].fillna(0)
    y_pred_new1.head(2)

    return y_pred_new1