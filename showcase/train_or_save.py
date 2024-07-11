import streamlit as st
from helpers.train_models import main_st, MODELS
from helpers.helper_functions import save_model_to_system, only_selected_models, only_selected_model_infos, save_dataset_to_system


try:
    df = st.session_state['clean_dataframe']
    try:
        _ = st.session_state['trained_models']
        models_are_trained = True
    except:
        models_are_trained = False
        chosen_models = None
    options = st.session_state['cleaning_options']
    with open('markdowns/train_or_save.md', 'r') as file:
        markdown = file.read().split('[[[[')
    file.close()

    st.markdown(markdown[0])
    st.markdown(markdown[1])
    with open('markdowns/train_the_model.md', 'r') as file:
        train_model_markdown = file.read().split('[[[[')
    file.close()
    st.markdown(train_model_markdown[0])
    selected_models = {model['name']: st.checkbox(model['name']) for model in MODELS}
    test_split = st.number_input('In a percentage of the Test/Train Split (defaults: 20% Test, 80% Train)', value=20)
    train_them = st.button('Train These models')
    st.session_state['selected_models'] = selected_models

    if train_them:
        st.markdown(train_model_markdown[1])
        options['test_split'] = test_split
        trained_models, results_markdown = main_st(df, options, selected_models)
        st.session_state['trained_models'] = trained_models
        st.session_state['results_markdown'] = results_markdown
    if models_are_trained or train_them:
        try:
            st.markdown(results_markdown)
        except:
            st.markdown(st.session_state['results_markdown'])
        save_models = {model[1]: (st.checkbox(model[1], key=hash(model[1])), model)
                       for model in st.session_state['trained_models']}
        choose_one_to_save = any([v[0] for k, v in save_models.items()])
        available_products = list(df[options['product_id']].unique())
        user_model_name = st.text_input('### Put a Name for your trained models here')
        safe_them = st.button('Save these models in the system')
        unallowed_characters = '#\'\"[]{}:();,./?!@%$'
        user_input_is_disallowed = any([i in user_model_name for i in unallowed_characters])
        if user_input_is_disallowed:
            st.error('This name is not valid! It can\'t contain any of the following characters: '+" ,".join(list(unallowed_characters)))
        elif not user_model_name and user_input_is_disallowed:
            st.error('You did not write a model(s) name, you won\'t find it later!')
        if safe_them and not user_input_is_disallowed and user_model_name:
            additional_info = [available_products, user_model_name]
            st.markdown(train_model_markdown[2])
            for model_info in only_selected_model_infos(save_models):
                save_model_to_system(list(model_info)+additional_info, st.session_state['data_filename'])
        elif safe_them and not user_model_name and choose_one_to_save:
            st.error('You did not write a model(s) name, you won\'t find it later!')
        elif safe_them and not user_model_name and not choose_one_to_save:
            st.error('You did not write down a name or chose any to save. You will loose them if you reload the system!!')
######
    st.markdown(markdown[2])
    with open('markdowns/save_data.md', 'r') as file:
        save_data_markdown = file.read().split('[[[[')
    file.close()
    st.markdown(save_data_markdown[0])
    user_data_name = st.text_input('### Put a Name for your cleaned data here (empty name is OK)')
    save_the_data = st.button('Save the Data in the System')
    unallowed_characters = '#\'\"[]{}:();,./?!@%$'
    dataset_name_is_disallowed = any([i in user_data_name for i in unallowed_characters])
    if dataset_name_is_disallowed:
        st.error('This name is not valid! It can\'t contain any of the following characters: '+" ,".join(list(unallowed_characters)))
    if save_the_data and not dataset_name_is_disallowed:
        save_dataset_to_system(
            df, st.session_state['data_filename'],
            user_data_name, st.session_state['cleaning_options'])

except:
    with open('markdowns/skipped_page.md') as file:
        markdown = file.read()
    st.markdown(markdown)