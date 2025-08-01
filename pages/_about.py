import streamlit as st
st.title("🌤️ About the Weather Prediction App")
st.markdown("""
Welcome to the Weather Prediction App! This tool allows users to view **weather forecasts**, analyze **historical trends**, and assess **model predictions** for different cities.
The main goal is to provide accurate, user-friendly, and real-time weather insights using machine learning.
""")
st.subheader("🔧 Key Features")
st.markdown("""
- 🌦️ 7-day weather forecast using real-time APIs (Visual Crossing / Open-Meteo)
- 📈 Historical weather trend
- 🤖 Machine learning-based temperature predictions (XGBoost, LightGBM)
- 📊 Evaluation metrics (RMSE, MAE),obtained best rmse score for model 1.1 -> 2.88
- 📥 Feedback and rating system for continuous improvement
""")
st.subheader("⚙️ How It Works")
st.markdown("""
1. User selects a city and date range
2. App fetches weather data using external APIs
3. ML models predict temperature (tempmax & tempmin)
4. Differences and trends are calculated and displayed
5. Results are shown in a friendly and interactive interface
            
""")

st.subheader("🚀 Future Enhancements")
st.markdown("""
- Add rainfall and wind prediction
- Integrate severe weather alerts
- Mobile-friendly version
- Improved UI 
""")

st.subheader("🛠️ Technologies Used")

tools = ["Python", "Pandas", "Streamlit", "XGBoost", "LightGBM", "Matplotlib", "Visual Crossing API", "Open-Meteo API"]
st.markdown(", ".join(f"`{tool}`" for tool in tools))

st.header("Workflow")
st.image("image/workflow.png",width=600)

st.subheader("👤 Developer")

st.markdown("""
- **Name**: Abhishek Prasad
- **Email**: abhiprasad60036@gmail.com
- **GitHub**: [github.com/abhishek/2004](https://github.com/abhishekprasad2004)
""")

