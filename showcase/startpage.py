# This script sets up a Streamlit application with multiple pages for data analysis and machine learning tasks.

# Import necessary libraries: Streamlit (interactive python library)
import streamlit as st
import pandas as pd

# Define a dictionary 'pages' which maps page titles to the corresponding Python files and titles for each page.
pages = {
 'Start Here': [st.Page('homepage.py', title="Homepage")],  # User is directed to homepage.py.
 'Upload Data': [st.Page('load_new_data.py', title="Load new Data"),   # User is directed to load_new_data.py, where data can be uploaded.
                 st.Page('sub_pages/clean_the_data.py', title='Clean your Data')],  # After loading data, user is redirected to clean_the_data.py for data cleaning.
 'Load Models / Data': [st.Page('load_old_data.py', title="Load some Data")],   # User is directed to load_old_data.py where previous data or models are loaded.
 'Train Models - Save Data': [st.Page('train_or_save.py', title="Train or Save")],  # User is directed to train_or_save.py, for training or saving machine learning models.
 'Predict needed Inventory': [st.Page('prediction.py', title="Prediction Engine")]   # Lastly, user is directed to prediction.py which is a prediction wrapper using the trained model.
}
pg = st.navigation(pages)

pg.run()
