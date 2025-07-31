import streamlit as st
from datetime import timedelta
import numpy as np
import pandas as pd
from sklearn import sklearn
import requests
from datetime import date

params = [ "temperature_2m_max",
        "temperature_2m_min",
        "apparent_temperature_max",
        "apparent_temperature_min",
        "snowfall_sum",
        "precipitation_sum",
        "windspeed_10m_max",
        "windgusts_10m_max",
        "shortwave_radiation_sum"]

def date_data(start, city, lat, lon):
     start_new = start - timedelta(days=2)
     start_str = start_new.strftime("%Y-%m-%d") #vc
     end       = start + timedelta(days=7)
     end_str   = end.strftime("%Y-%m-%d")#vc
     start_open= end - timedelta(days=188)
     end_open   = start - timedelta(days=3)
     start_open_str = start_open.strftime("%Y-%m-%d")#open-meteo
     end_open_str   = end_open.strftime("%Y-%m-%d")#open_meteo
     return start_str,end_str,start_open_str,end_open_str,city,lat,lon

def combined_data(start_vc, end_vc, start_open, end_open, city, lat, lon):
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
        weather_vc = pd.json_normalize(data_vc["days"])
        weather_vc["city"] = city
        return weather_vc
    
    def retrive_open(start_open, end_open):
        url_open = (
            f"https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={lat}&longitude={lon}"
            f"&start_date={start_open}&end_date={end_open}"
            f"&daily={','.join(params)}"
            f"&timezone=Asia%2FKolkata"
        )
        response = requests.get(url_open)
        data_open = response.json()
        weather_open = pd.DataFrame(data_open["daily"])
        weather_open["city"] = city
        return weather_open

    weather_vc = retrive_vc(start_vc, end_vc)
    weather_open = retrive_open(start_open, end_open)
    #chnaging column to match visual crossing api
    weather_open.rename(columns={"time": "datetime",
                  "temperature_2m_max": "tempmax",
                  "temperature_2m_min": "tempmin",
                  "apparent_temperature_max": "feelslikemax",
                   "apparent_temperature_min": "feelslikemin",
                   "snowfall_sum": "snow",
                   "precipitation_sum": "precip",
                   "windspeed_10m_max": "windspeed",
                   "windgusts_10m_max": "windgust",
                   "shortwave_radiation_sum":"solarenergy",},inplace= True)
     # changing some column units to match with visual crossing data
    weather_open["windspeed"]=weather_open["windspeed"]*3.6
    weather_open["windgust"]=weather_open["windgust"]*3.6
    weather_open["solarenergy"]=weather_open["solarenergy"]/3.6
    vc_data = weather_vc.copy()
    vc_data= vc_data[["datetime","tempmax","tempmin","feelslikemax","feelslikemin","snow","precip","windspeed","windgust","solarenergy","city"]]
        # Combine
    weather_data = pd.concat([weather_open,vc_data], ignore_index=True)
    weather = weather_data.copy()
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
    y_pred_df=y_pred_df.tail(9) #selected date range
    y_test_df =y_test.tail(9)   #selected date range
    np.sqrt(metrics.mean_squared_error(y_test_df,y_pred_df)) #error between actual and predicted value
    y_pred_new= y_pred_df.reset_index(drop=True)
    y_pred_new["datetime"] =  weather_vc["datetime"]
    y_pred_new["icon"] = weather_vc["icon"]
    y_pred_new = y_pred_new[["datetime","tempmax","tempmin","icon"]]
    y_pred_new = y_pred_new.tail(8)

    y_pred_new["tempmax"] = pd.to_numeric(y_pred_new["tempmax"], errors='coerce')
    y_pred_new["tempmin"] = pd.to_numeric(y_pred_new["tempmin"], errors='coerce')

    y_pred_new["tempmax_diff"] = y_pred_new["tempmax"].diff().fillna(0).map("{:.2f}".format)
    y_pred_new["tempmin_diff"] = y_pred_new["tempmin"].diff().fillna(0).map("{:.2f}".format)
    y_pred_new[['tempmax_diff',"tempmin_diff"]]=y_pred_new[['tempmax_diff',"tempmin_diff"]].fillna(0)
    y_pred_new

    return y_pred_new





