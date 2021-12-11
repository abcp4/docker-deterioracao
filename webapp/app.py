import requests
import streamlit as st

API_URL = "http://api-predict:8000"

x = st.slider("Select a value", max_value=10)

r = requests.get(f"{API_URL}/factorial", params={"number": x})

if r.status_code == 200:
    data = r.json()
    st.write(x, "factorial is", data["answer"])
