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
    API_URL = "https://oc-ds-projet7-api-flask-mh.streamlit.app/"

    ##################################
    # LIST OF API REQUEST FUNCTIONS

    # Get list of SK_IDS (cached)
    @st.cache_data
    def get_sk_id_list():
        # URL of the sk_id API
        SK_IDS_API_URL = API_URL + "list_id/"
        # Requesting the API and saving the response
        response = requests.get(SK_IDS_API_URL)
        # Convert from JSON format to Python dict
        content = json.loads(response.content)
        # Getting the values of SK_IDS from the content
        SK_IDS = pd.Series(content['data']).values
        return SK_IDS

    # Get Personal data (cached)
    @st.cache_data
    def get_data_cust(select_sk_id):
        # URL of the scoring API (ex: SK_ID_CURR = 100028)
        PERSONAL_DATA_API_URL = API_URL + "get_data_cust/?SK_ID_CURR=" + str(select_sk_id)
        # save the response to API request
        response = requests.get(PERSONAL_DATA_API_URL)
        # convert from JSON format to Python dict
        content = json.loads(response.content.decode('utf-8'))
        # convert data to pd.Series
        data_cust = pd.Series(content['data']).rename(select_sk_id)
        return data_cust

    # Get data from 10 nearest neighbors in train set (cached)
    @st.cache_data
    def get_data_neigh(select_sk_id):
        # URL of the scoring API (ex: SK_ID_CURR = 100028)
        NEIGH_DATA_API_URL = API_URL + "neigh_cust/?SK_ID_CURR=" + str(select_sk_id)
        # save the response of API request
        response = requests.get(NEIGH_DATA_API_URL)
        # convert from JSON format to Python dict
        content = json.loads(response.content.decode('utf-8'))
        # convert data to pd.DataFrame and pd.Series
        X_neigh = pd.DataFrame(content['X_neigh'])
        y_neigh = pd.Series(content['y_neigh']['TARGET']).rename('TARGET')
        return X_neigh, y_neigh

    # Get scoring of one applicant customer (cached)
    @st.cache_data
    def get_cust_scoring(select_sk_id):
        # URL of the scoring API
        SCORING_API_URL = API_URL + "scoring_cust/?SK_ID_CURR=" + str(select_sk_id)
        # Requesting the API and save the response
        response = requests.get(SCORING_API_URL)
        # convert from JSON format to Python dict
        content = json.loads(response.content.decode('utf-8'))
        # getting the values from the content
        score = content['score']
        thresh = content['thresh']
        return score, thresh

    # Get the list of features and description
    @st.cache_data
    def get_features_descriptions():
        # URL of the aggregations API
        FEAT_DESC_API_URL = API_URL + "feat_desc"
        # Requesting the API and save the response
        response = requests.get(FEAT_DESC_API_URL)
        # convert from JSON format to Python dict
        content = json.loads(response.content.decode('utf-8'))
        # convert back to pd.Series
        features_desc = pd.Series(content['data']['Description']).rename("Description")
        return features_desc
    
    # Get the list of feature importances (according to lgbm classification model)
    @st.cache_data
    def get_features_importances():
        # URL of the aggregations API
        FEAT_IMP_API_URL = API_URL + "feat_imp"
        # Requesting the API and save the response
        response = requests.get(FEAT_IMP_API_URL)
        # convert from JSON format to Python dict
        content = json.loads(response.content.decode('utf-8'))
        # convert back to pd.Series
        feat_imp = pd.Series(content['data']).sort_values(ascending=False)
        return feat_imp

    
    #################################
    #################################
    #################################
    # Configuration of the streamlit page
    st.set_page_config(page_title='Loan application scoring dashboard',
                       page_icon='random',
                       layout='centered',
                       initial_sidebar_state='auto')

    # Display the title
    st.title('Loan application scoring dashboard')
    st.header("Mohamed HAOUANE - Data Science project 7")
    path = "logo.png"
    image = Image.open(path)
    st.sidebar.image(image, width=180)

   

    #################################
    #################################
    #################################

    # ------------------------------------------------
    # Select the customer's ID
    # ------------------------------------------------

    SK_IDS = get_sk_id_list()
    select_sk_id = st.sidebar.selectbox('Select SK_ID_CURR from list :', SK_IDS, key=18)
    st.write('SK_ID_CURR selected : ', select_sk_id)


    # ------------------------------------------------
    # Get All Data relative to customer 
    # ------------------------------------------------

    # Get personal data 
    X_cust= get_data_cust(select_sk_id)  

    # Get 10 neighbors personal data (preprocessed)
    X_neigh, y_neigh = get_data_neigh(select_sk_id)
    y_neigh = y_neigh.replace({0: 'repaid (neighbors)',
                               1: 'not repaid (neighbors)'})

    # ------------------------------------------------
    # Default value for main columns
    # ------------------------------------------------
    feat_imp = get_features_importances()
    main_cols = list(feat_imp.sort_values(ascending=False).iloc[:12].index)

    # #############################
    
    def get_list_display_features(shap_val_trans, def_n, key):
    
        all_feat = X_tr_all.columns.to_list()
        
        n = st.slider("Nb of features to display",
                      min_value=2, max_value=42,
                      value=def_n, step=None, format=None, key=key)
        
        if st.checkbox('Choose main features according to SHAP local interpretation for the applicant customer', key=key):
            disp_cols = list(shap_val_trans.abs()
                                .sort_values(ascending=False)
                                .iloc[:n].index)
        else:
            disp_cols = list(get_features_importances().sort_values(ascending=False)\
                                            .iloc[:n].index)
            
        disp_box_cols = st.multiselect('Choose the features to display (default: order of general importance for lgbm calssifier):',
                                        sorted(all_feat),
                                        default=disp_cols, key=key)
        return disp_box_cols

     # #############################
    
    def get_list_display_features(shap_val_trans, def_n, key):
    
        all_feat = X_tr_all.columns.to_list()
        
        n = st.slider("Nb of features to display",
                      min_value=2, max_value=42,
                      value=def_n, step=None, format=None, key=key)
        
        disp_cols = list(get_features_importances().sort_values(ascending=False)\
                                            .iloc[:n].index)
            
        disp_box_cols = st.multiselect('Choose the features to display (default: order of general importance for lgbm calssifier):',
                                        sorted(all_feat),
                                        default=disp_cols, key=key)
        return disp_box_cols
    # ##########################

    # ##################################################
    # CUSTOMER'S DATA
    # ##################################################

    if st.sidebar.checkbox("Customer's data"):

        st.header("Customer's data")

        format_dict = {'cust prepro': '{:.2f}',
                       '10 neigh (mean)': '{:.2f}',
                       '10k samp (mean)': '{:.2f}'}
        all_feat = list(set(X_cust.index.to_list() ))
        disp_cols = st.multiselect('Choose the features to display :',
                                   sorted(all_feat),#.sort(),
                                   default=sorted(main_cols))
        
        if st.checkbox('Show comparison with 10 neighbors customers', key=31):
            # Concatenation of the information to display
            df_display = pd.concat([X_cust.loc[disp_cols].rename('Customer'),                                  
                                    X_neigh[disp_cols].mean().rename('10 neigh (mean)'),                                    
                                    ], axis=1)  # all pd.Series
        else:
            # Display only personal_data
            df_display = pd.concat([X_cust.loc[disp_cols].rename('Customer')], axis=1)  # all pd.Series

        # Display at last 
        st.dataframe(df_display.style.format(format_dict)
                                     .background_gradient(cmap='seismic',
                                                          axis=0, subset=None,
                                                          text_color_threshold=0.2,
                                                          vmin=-1, vmax=1)
                                     .highlight_null('lightgrey'))
            
    
    ##################################################
    # SCORING
    ##################################################

    if st.sidebar.checkbox("Scoring and model's decision", key=38):

        st.header("Scoring and model's decision")

        #  Get score
        score, thresh = get_cust_scoring(select_sk_id)

        # Display score (default probability)
        st.write('Loan default probability : {:.0f}%'.format(score*100))
        # Display default threshold
        st.write('Default model threshold : {:.0f}%'.format(thresh*100))
        
        # Compute decision according to the best threshold (True: loan refused)
        bool_cust = (score >= thresh)

        if bool_cust is False:
            decision = "Loan accepted"             
        else:
            decision = "Loan refused"
        
        st.write('Decision :', decision)
     
     
    # #################################################
    # FEATURES' IMPORTANCE
    # ##############################################

    if st.sidebar.checkbox("Features importance", key=29):

        st.header("Global features importances")
        
        plot_choice = []
        if st.checkbox('Add global feature importance', value=True, key=25):
            plot_choice.append(0)
            
            #  Get feature imporance
            feat_imp = get_features_importances()
            st.write('Features importance : ',feat_imp.rename('Feat. Importance'))
                  
        

    # #################################################
    # FEATURES DESCRIPTIONS
    # #################################################

    features_desc = get_features_descriptions()

    if st.sidebar.checkbox('Features descriptions', key=22):

        st.header("Features descriptions")

        list_features = features_desc.index.to_list()

        feature = st.selectbox('List of the features :', list_features, key=15)
        #st.write("Feature's name: ", feature)
        # st.write('Description: ', str(features_desc.loc[feature]))
        st.table(features_desc.loc[feature:feature])

        if st.checkbox('show all features', key=20):
            # Display features' descriptions
            st.table(features_desc)
    
    ################################################


if __name__ == '__main__':
    main()
