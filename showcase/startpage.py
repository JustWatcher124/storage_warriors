import streamlit as st
import pandas as pd


pages = {
    'Start Here': [st.Page('homepage.py', title="Homepage")],
    'New Model / Data': [st.Page('load_new_data.py', title="Load Your Own Data"),
                         st.Page('sub_pages/clean_the_data.py', title='Clean your Data'),
                         st.Page('sub_pages/train_or_save.py', title='Train or Save')],
    'Existing Model / Data': [st.Page('load_old_data.py', title="Load some Data")]
}
pg = st.navigation(pages)

pg.run()
