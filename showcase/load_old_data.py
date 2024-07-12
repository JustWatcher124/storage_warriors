# Import necessary modules, Streamlit for rendering, os for directory operations, pickle to load data from filesystem
import streamlit as st
import os
import pickle

# Import the helper_functions script to 'outsource' the backend
import helpers.helper_functions as helper_functions

# Set Page configs
st.set_page_config(page_title='Load Models / Data', page_icon='images/icon.png',
                   layout='wide', initial_sidebar_state='expanded')

# Check if User is on the right page using session_states variables
try:
    # exists only if user visited the homepage (mostly from reloading) -- causes exception caught below
    _ = st.session_state['visited_homepage']
    # load the default markdown from file
    with open('markdowns/load_old_data.md', 'r') as file:
        markdown = file.read().split('[[[[')
    file.close()
    # load the extra markdown from file
    with open('markdowns/load_old_data_alt.md', 'r') as file:
        markdown_alt = file.read().split('[[[[')
    file.close()
    st.markdown(markdown[0])

    # get the current directory for directory and file operations later
    current_directory = os.getcwd()

    # get meta info files from the designated directory
    datasets_directory = os.path.join(current_directory, '../datasets')
    datasets_meta_info_path_list = helper_functions.get_files(datasets_directory)

    # list to store meta information of datasets
    datasets_meta_list = []
    # read all meta information files for datasets from the datasets directory
    for file_path in datasets_meta_info_path_list:
        with open(file_path, 'rb') as file:
            datasets_meta_list.append(pickle.load(file))
        file.close()

    st.markdown(markdown[1])  # write some markdown to the page

    # split meta information into user-generated and system generated to allow for easier distinction
    system_datasets = [datasets_meta for datasets_meta in datasets_meta_list if datasets_meta['system_trained']]
    user_datasets = [datasets_meta for datasets_meta in datasets_meta_list if not datasets_meta['system_trained']]

    if user_datasets:
        # write a pretty markdown table for the datasets
        st.markdown(helper_functions.pretty_markdown_for_datasets(user_datasets))
        with st.form('user datasets choice form', border=False):
            use_this_dataset = st.selectbox(
                'Select a dataset from the list directly above to choose it for training',
                options=[dataset_info['data_name'] + ' - ' + dataset_info['data_file_name']
                         for dataset_info in user_datasets])
            submit_user_dataset = st.form_submit_button('Use this Choice')
            if submit_user_dataset:  # actually load the dataset into memory
                st.write('With the Dataset chosen, you can continue to the Train or Save page in the New Model / Data section')
                st.session_state['clean_dataframe'], st.session_state['cleaning_options'], st.session_state['data_filename'] = helper_functions.get_dataset_from_choice(
                    use_this_dataset, user_datasets)

    else:
        st.markdown(markdown_alt[0])

    if system_datasets:
        st.markdown(markdown_alt[3])
        # write a pretty markdown table for the datasets
        st.markdown(helper_functions.pretty_markdown_for_datasets(system_datasets))
        with st.form('system datasets choice form', border=False):
            use_this_dataset = st.selectbox(
                'Select a dataset from the list directly above to choose it for training',
                options=[dataset_info['data_name'] + ' - ' + dataset_info['data_file_name']
                         for dataset_info in system_datasets])
            submit_system_dataset = st.form_submit_button('Use this Choice')
            if submit_system_dataset:  # actually load the dataset into memory
                st.write('With the Dataset chosen, you can continue to the Train or Save page in the New Model / Data section')
                st.session_state['clean_dataframe'], st.session_state['cleaning_options'], st.session_state['data_filename'] = helper_functions.get_dataset_from_choice(
                    use_this_dataset, system_datasets)
    else:
        st.markdown(markdown_alt[4])

    # get meta info files from the designated directory
    model_directory = os.path.join(current_directory, '../tought_models')
    model_meta_info_path_list = helper_functions.get_files(model_directory)

    # list to store meta information of datasets
    model_meta_list = []
    # read all meta information files for datasets from the datasets directory
    for file_path in model_meta_info_path_list:
        with open(file_path, 'rb') as file:
            model_meta_list.append(pickle.load(file))
        file.close()

    # split meta information into user-generated and system generated to allow for easier distinction
    system_models = [model_meta for model_meta in model_meta_list if model_meta['system_trained']]
    user_models = [model_meta for model_meta in model_meta_list if not model_meta['system_trained']]

    if user_models:
        st.markdown(markdown[3])
        # write a pretty markdown table for the models
        st.markdown(helper_functions.pretty_markdown_for_models(user_models))
        with st.form('user models choice form', border=False):
            use_this_model = st.selectbox(
                'Select a model from the list directly above to choose it for prediction',
                options=[model_info['model_name']+' - '+model_info['user_model_name'] for model_info in user_models])
            submit_user_models = st.form_submit_button('Use this Choice')
            if submit_user_models:  # actually load the model into memory
                st.write('With the Model set, please continue on to the Prediction Page')
                st.session_state['chosen_model'], st.session_state['chosen_models_avail_products'] = helper_functions.get_model_from_choice(
                    use_this_model, user_models)
    else:
        # tell the user that no user model exists
        st.markdown(markdown_alt[2])

    if system_models:
        st.markdown(markdown[2])
        # write a pretty markdown table for the models
        st.markdown(helper_functions.pretty_markdown_for_models(system_models))
        with st.form('system models choice form', border=False):
            use_this_model = st.selectbox(
                'Select a model from the list directly above to choose it for prediction',
                options=[model_info['model_name'] + ' - ' + model_info['user_model_name'] for model_info in system_models])
            submit_system_models = st.form_submit_button('Use this Choice')
            if submit_system_models:  # actually load the model into memory
                st.write('With the Model set, please continue on to the Prediction Page')
                st.session_state['chosen_model'], st.session_state['chosen_models_avail_products'] = helper_functions.get_model_from_choice(
                    use_this_model, system_models)
    else:
        # tell the user that no system models have been found
        st.markdown(markdown_alt[1])


except:  # bare exception because this also makes errors clear to the user
    with open('markdowns/skipped_page.md') as file:
        markdown = file.read()
    file.close()
    st.markdown(markdown)
