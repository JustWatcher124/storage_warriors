import streamlit as st
import pandas as pd


pages = {
    'Start Here': [st.Page('homepage.py', title="Homepage")],
    'Upload Data': [st.Page('load_new_data.py', title="Load new Data"),
                    st.Page('sub_pages/clean_the_data.py', title='Clean your Data')],
    'Load Models / Data': [st.Page('load_old_data.py', title="Load some Data")],
    'Train Models - Save Data': [st.Page('train_or_save.py', title="Train or Save")],
    'Predict needed Inventory': [st.Page('prediction.py', title="Prediction Engine")]
}
pg = st.navigation(pages)

pg.run()
