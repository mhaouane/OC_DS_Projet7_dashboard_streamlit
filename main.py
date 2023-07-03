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

   ##################################
    # LIST OF API REQUEST FUNCTIONS

    # Get list of SK_IDS (cached)
    @st.cache
    def get_sk_id_list():
        # URL of the sk_id API
        SK_IDS_API_URL = API_URL + "sk_ids/"
        # Requesting the API and saving the response
        response = requests.get(SK_IDS_API_URL)
        # Convert from JSON format to Python dict
        content = json.loads(response.content)
        # Getting the values of SK_IDS from the content
        SK_IDS = pd.Series(content['data']).values
        return SK_IDS
 

   


if __name__ == '__main__':
    main()
