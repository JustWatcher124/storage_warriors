import streamlit as st
import os
import helpers.helper_functions as helper_functions
import pickle


try:
    if st.session_state['visited_homepage']:
        print('User visited Homepage')
    with open('markdowns/load_old_data.md', 'r') as file:
        markdown = file.read().split('[[[[')
    st.markdown(markdown[0])


    current_directory = os.getcwd()
    model_directory = os.path.join(current_directory , '../tought_models')
    model_meta_info_path_list = helper_functions.get_files(model_directory)

    
    model_meta_list = []
    for file_path in model_meta_info_path_list:
        with open(file_path, 'rb') as file:
            model_meta_list.append(pickle.load(file))
        file.close()
    model_meta_list
    

    
except KeyError:
    with open('markdowns/skipped_page.md') as file:
        markdown = file.read()
    st.markdown(markdown)
