import streamlit as st
import os
import helpers.helper_functions as helper_functions
import pickle


try:
    _ = st.session_state['visited_homepage']
    with open('markdowns/load_old_data.md', 'r') as file:
        markdown = file.read().split('[[[[')
    st.markdown(markdown[0])

    current_directory = os.getcwd()
    model_directory = os.path.join(current_directory, '../tought_models')
    model_meta_info_path_list = helper_functions.get_files(model_directory)

    datasets_directory = os.path.join(current_directory, '../datasets')
    datasets_meta_info_path_list = helper_functions.get_files(datasets_directory)
    datasets_meta_list = []
    for file_path in datasets_meta_info_path_list:
        with open(file_path, 'rb') as file:
            datasets_meta_list.append(pickle.load(file))
        file.close()
    st.markdown(markdown[1])
    datasets_meta_list

    model_meta_list = []
    for file_path in model_meta_info_path_list:
        with open(file_path, 'rb') as file:
            model_meta_list.append(pickle.load(file))
        file.close()
    system_models = [model_meta for model_meta in model_meta_list if model_meta['system_trained']]
    user_models = [model_meta for model_meta in model_meta_list if not model_meta['system_trained']]

    st.markdown(markdown[2])

    system_models
    st.markdown(markdown[3])
    user_models
    model_meta_list


except KeyError:
    with open('markdowns/skipped_page.md') as file:
        markdown = file.read()
    st.markdown(markdown)
