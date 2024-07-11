import streamlit as st
import pandas as pd


pages = {
    'Start Here': [st.Page('homepage.py', title="Homepage")],
    'New Model / Data': [st.Page('load_new_data.py', title="Load Your Own Data"),
                         st.Page('sub_pages/clean_the_data.py', title='Clean your Data')],
    'Existing Model / Data': [st.Page('load_old_data.py', title="Load Model or Data")],
    'Train a Model or Save Data': [st.Page('train_or_save.py', title='Train or Save')],
    'Pediction Engine™': [st.Page('prediction.py', title='Predict your needed Inventory')]
}
pg = st.navigation(pages)

pg.run()
