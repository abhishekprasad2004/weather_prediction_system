import streamlit as st
import streamlit.components.v1 as components
import time
 
st.title("Share your experience")
sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")


st.text("any suggestion?")
st.text("Give your valuable Feedback IN Google Form below")
if st.button("Open"):
        with st.spinner("Wait for it...", show_time=True):
            time.sleep(1)
            google_form_url = "https://forms.gle/rWfBhSteMmEFpHPbA"
            components.iframe(google_form_url, height=800, scrolling=True)
            if st.button("Submitted form?"):
                st.success('Google form opened', icon="✅")
            else:
                st.warning("Please fill the form")     
else:
    st.warning("Open form by clicking open button")
    
