# import modules, Streamlit for rendering, datetime for date operations on this page
import streamlit as st

# import needed functions and variable from the train_models module
from helpers.train_models import main_st, MODELS

# Import the helper_functions script to 'outsource' the backend
import helpers.helper_functions as helper_functions


# Check if User is on the right page using session_states variables
try:
    # exists only if user has uploaded and cleaned a dataset beforehand -- causes exception caught below
    df = st.session_state['clean_dataframe']
    # check if the models have been trained before (handles user or automatic refreshes of the page)
    try:
        _ = st.session_state['trained_models']
        models_are_trained = True
    except:
        models_are_trained = False
        chosen_models = None

    # load the default markdown from file
    with open('markdowns/train_or_save.md', 'r') as file:
        markdown = file.read().split('[[[[')
    file.close()

    st.markdown(markdown[0])
    st.markdown(markdown[1])

    # load training specific markdown from file
    with open('markdowns/train_the_model.md', 'r') as file:
        train_model_markdown = file.read().split('[[[[')
    file.close()
    st.markdown(train_model_markdown[0])

    # give a choice in form of checkboxes to the user what type of model to use
    selected_models = {model['name']: st.checkbox(model['name']) for model in MODELS}
    # save user choice through reloads
    st.session_state['selected_models'] = selected_models

    # let user set the test/train split used in training -- this is basically only for people who know what they do
    test_split = st.number_input(
        'In a percentage of the Test/Train Split (defaults: 20% Test, 80% Train)', value=20, max_value=50)
    train_them = st.button('Train These models')

    # cleaning_options also contains some information needed in training
    options = st.session_state['cleaning_options']

    if train_them:  # user chose to train the selected or all models
        st.markdown(train_model_markdown[1])
        # save the test split through reloads
        options['test_split'] = test_split
        # actually train the models
        trained_models, results_markdown = main_st(df, options, selected_models)
        st.session_state['trained_models'] = trained_models
        st.session_state['results_markdown'] = results_markdown

    if models_are_trained or train_them:  # show the results regardless how many reloads
        # somehow breaks without this try except block -- i don't know why though
        try:
            st.markdown(results_markdown)
        except:
            st.markdown(st.session_state['results_markdown'])
        # choice for the user to save trained models
        save_models = {model[1]: (st.checkbox(model[1], key=hash(model[1])), model)
                       for model in st.session_state['trained_models']}
        choose_one_to_save = any([v[0] for k, v in save_models.items()])
        available_products = list(df[options['product_id']].unique())

        # user given name for the models
        user_model_name = st.text_input('### Put a Name for your trained models here')
        safe_them = st.button('Save these models in the system')
        # some user input sanitation is a must (this should allow simple 'python code injection')
        unallowed_characters = '#\'\"[]{}:();,./?!@%$'
        user_input_is_disallowed = any([i in user_model_name for i in unallowed_characters])

        # show errors dependent on the user error
        if user_input_is_disallowed:
            st.error('This name is not valid! It can\'t contain any of the following characters: '+" ,".join(list(unallowed_characters)))
        elif not user_model_name and user_input_is_disallowed:
            st.error('You did not write a model(s) name, you won\'t find it later!')

        # check for cases where a name (needed) or input error occur when pressing the button
        if safe_them and not user_input_is_disallowed and user_model_name:
            # format the data for the saving function correctly
            additional_info = [available_products, user_model_name]
            st.markdown(train_model_markdown[2])
            # save models and there meta information into their respective files
            for model_info in helper_functions.only_selected_model_infos(save_models):
                helper_functions.save_model_to_system(
                    list(model_info)+additional_info, st.session_state['data_filename'])
        # following 2 elifs:
        # handle user mis-input
        elif safe_them and not user_model_name and choose_one_to_save:
            st.error('You did not write a model(s) name, you won\'t find it later!')
        elif safe_them and not user_model_name and not choose_one_to_save:
            st.error('You did not write down a name or chose any to save. You will loose them if you reload the system!!')
# code break to show where dataset saving code begins
    st.markdown(markdown[2])
    # load saving specific markdown
    with open('markdowns/save_data.md', 'r') as file:
        save_data_markdown = file.read().split('[[[[')
    file.close()
    st.markdown(save_data_markdown[0])
    user_data_name = st.text_input('### Put a Name for your cleaned data here (empty name is OK)')
    save_the_data = st.button('Save the Data in the System')
    # user input sanitation / checking
    unallowed_characters = '#\'\"[]{}:();,./?!@%$'
    dataset_name_is_disallowed = any([i in user_data_name for i in unallowed_characters])
    if dataset_name_is_disallowed:
        st.error('This name is not valid! It can\'t contain any of the following characters: '+" ,".join(list(unallowed_characters)))
    # save the dataset to the system files
    if save_the_data and not dataset_name_is_disallowed:
        helper_functions.save_dataset_to_system(
            df, st.session_state['data_filename'],
            user_data_name, st.session_state['cleaning_options'])

except:  # bare exception because this also makes errors clear to the user
    with open('markdowns/skipped_page.md') as file:
        markdown = file.read()
    st.markdown(markdown)
