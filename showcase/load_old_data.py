import streamlit as st
import os
import helpers.helper_functions as helper_functions
import pickle


def reset_choices():
    st.session_state['reset_choices_loading'] = True


def lock_in_choice():
    st.session_state['reset_choices_loading'] = False


try:
    _ = st.session_state['visited_homepage']
    try:
        _ = st.session_state['reset_choices_loading']
    except:
        st.session_state['reset_choices_loading'] = False
    with open('markdowns/load_old_data.md', 'r') as file:
        markdown = file.read().split('[[[[')
    file.close()
    with open('markdowns/load_old_data_alt.md', 'r') as file:
        markdown_alt = file.read().split('[[[[')
    file.close()
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
    system_datasets = [datasets_meta for datasets_meta in datasets_meta_list if datasets_meta['system_trained']]
    user_datasets = [datasets_meta for datasets_meta in datasets_meta_list if not datasets_meta['system_trained']]
    if user_datasets:
        st.markdown(helper_functions.pretty_markdown_for_datasets(user_datasets))
        with st.form('user datasets choice form', border=False):
            use_this_dataset = st.selectbox(
                'Select a dataset from the list directly above to choose it for training',
                options=[dataset_info['data_name']+' - '+dataset_info['data_file_name'] for dataset_info in user_datasets], on_change=lock_in_choice())
            submit_user_dataset = st.form_submit_button('Use this Choice')
            if submit_user_dataset:
                st.write('With the Dataset chosen, you can continue to the Train or Save page in the New Model / Data section')
                st.session_state['clean_dataframe'], st.session_state['cleaning_options'] = get_dataset_from_choice(use_this_dataset, user_datasets)
    else:
        st.markdown(markdown_alt[0])

    if system_datasets:
        st.markdown(markdown_alt[3])
        st.markdown(helper_functions.pretty_markdown_for_datasets(system_datasets))
        with st.form('system datasets choice form', border=False):
            use_this_dataset = st.selectbox(
                'Select a dataset from the list directly above to choose it for training',
                options=[dataset_info['data_name']+' - '+dataset_info['data_file_name'] for dataset_info in system_datasets], on_change=lock_in_choice())
            print('h')
            submit_system_dataset = st.form_submit_button('Use this Choice')
            if submit_system_dataset:
                st.write('With the Dataset chosen, you can continue to the Train or Save page in the New Model / Data section')
                st.session_state['clean_dataframe'], st.session_state['cleaning_options'] = helper_functions.get_dataset_from_choice(use_this_dataset, system_datasets)
    else:
        st.markdown(markdown_alt[4])

    model_meta_list = []

    for file_path in model_meta_info_path_list:
        with open(file_path, 'rb') as file:
            model_meta_list.append(pickle.load(file))
        file.close()
    system_models = [model_meta for model_meta in model_meta_list if model_meta['system_trained']]
    user_models = [model_meta for model_meta in model_meta_list if not model_meta['system_trained']]

    if user_models:
        st.markdown(markdown[3])
        st.markdown(helper_functions.pretty_markdown_for_models(user_models))
        with st.form('user models choice form', border=False):
            use_this_model = st.selectbox(
                'Select a model from the list directly above to choose it for prediction',
                options=[model_info['model_name']+' - '+model_info['user_model_name'] for model_info in user_models], on_change=lock_in_choice())
            submit_user_models = st.form_submit_button('Use this Choice')
            if submit_user_models:
                st.write('With the Model set, please continue on to the Prediction Page')
                st.session_state['chosen_model'] = use_this_model 
    else:
        st.markdown(markdown_alt[2])

    if system_models:
        st.markdown(markdown[2])
        st.markdown(helper_functions.pretty_markdown_for_models(system_models))
        with st.form('system models choice form', border=False):
            use_this_model = st.selectbox(
                'Select a model from the list directly above to choose it for prediction',
                options=[model_info['model_name'] + ' - ' + 'System Trained' for model_info in system_models], on_change=lock_in_choice())
            submit_system_models = st.form_submit_button('Use this Choice')
            if submit_system_models:
                st.write('With the Model set, please continue on to the Prediction Page')
                st.session_state['chosen_model'] = use_this_model 
    else:
        st.markdown(markdown_alt[1])


except KeyError:
    with open('markdowns/skipped_page.md') as file:
        markdown = file.read()
    file.close()
    st.markdown(markdown)
