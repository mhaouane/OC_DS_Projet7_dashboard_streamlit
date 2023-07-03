# TO RUN: streamlit run c:/Users/ADSL/Documents/Projet7/frontend/main.py
# Local URL: http://localhost:8501
# Network URL: http://192.168.0.50:8501
# Online URL: http://15.188.179.79

import streamlit as st
from PIL import Image
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import shap
import time

from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def main():
    # local API (à remplacer par l'adresse de l'application déployée)
    #API_URL = "http://127.0.0.1:5000/api/"
    API_URL = "https://oc-api-flask-mh.onrender.com/api/"
    #"https://oc-ds-projet7-api-flask-mh.streamlit.app/"
    

    ##################################
    # LIST OF API REQUEST FUNCTIONS

    

    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Streamlit! by Mohamed👋")

    st.sidebar.success("Select a demo above.")

   


if __name__ == '__main__':
    main()
