import streamlit as st 
import numpy as np

pages = {
    "Project": [
        st.Page("pages/forecast1.py", title="Forecast",default=True,icon=":material/azm:"),
        st.Page("pages/historical1.py", title="Historical",icon=":material/history:"),
        
    ],
    "Tools": [
        st.Page("pages/about1.py", title="About Project",icon=":material/page_info:"),
        st.Page("pages/rating1.py", title="Rating",icon=":material/add_reaction:"),
    ],
}


st.set_page_config(layout="wide")
pg = st.navigation(pages,position="sidebar")
pg.run()