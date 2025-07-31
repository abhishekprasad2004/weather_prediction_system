import streamlit as st 
import numpy as np

pages = {
    "Project": [
        st.Page("pages/_forecast.py", title="Forecast",default=True,icon=":material/azm:"),
        st.Page("pages/_historical.py", title="Historical",icon=":material/history:"),
        
    ],
    "Tools": [
        st.Page("pages/_about.py", title="About Project",icon=":material/page_info:"),
        st.Page("pages/_rating.py", title="Rating",icon=":material/add_reaction:"),
    ],
}


st.set_page_config(layout="wide")
pg = st.navigation(pages,position="sidebar")
pg.run()