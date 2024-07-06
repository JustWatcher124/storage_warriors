import streamlit as st
import pandas as pd
import os

def save_df_to_folder(df, folder_path, file_name):
    """Saves dataframe to the provided folder."""
    if not os.path.isdir(folder_path):
        st.error('The provided folder does not exist. Please provide a valid folder path.')
        return

    file_path = os.path.join(folder_path, file_name)
    df.to_csv(file_path, index=False)
    st.success(f'Successfully saved dataframe to {file_path}')

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})  # example dataframe

folder_path = st.text_input('Enter the folder path where you want to save the dataframe:')
file_name = st.text_input('Enter the filename for the dataframe (should end in .csv):')

if st.button('Save Dataframe'):
    save_df_to_folder(df, folder_path, file_name)
