import streamlit as st
from helpers.train_models import main_st, MODELS
from helpers.helper_functions import save_model_to_system, only_selected_models, only_selected_model_infos


try:
    df = st.session_state['clean_dataframe']
    try:
        _ = st.session_state['trained_models']
        models_are_trained = True
    except:
        models_are_trained = False
        chosen_models = None
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
    train_them = st.button('Train These models')
    st.session_state['selected_models'] = selected_models
    st.session_state['cleaning_options']['test_split'] = st.session_state['options'] = 20
    if train_them or models_are_trained:
        st.markdown(train_model_markdown[1])
        trained_models = main_st(df, st.session_state['cleaning_options'], selected_models)
        st.session_state['trained_models'] = trained_models
        save_models = {model[1]: (st.checkbox(model[1], key=hash(model[1])), model)
                       for model in st.session_state['trained_models']}
        safe_them = st.button('Safe these models in the system')
        choose_one_to_save = any([v[0] for k, v in save_models.items()])
        available_products = list(df[st.session_state['cleaning_options']['product_id']].unique())
        user_model_name = st.text_input('### Put a Name for your trained models here')
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
                save_model_to_system(list(model_info)+additional_info)
        elif safe_them and not user_model_name and choose_one_to_save:
            st.error('You did not write a model(s) name, you won\'t find it later!')
        elif safe_them and not user_model_name and not choose_one_to_save:
            st.error('You did not write down a name or chose any to save. You will loose them if you reload the system!!')
#        selected_models2 = {model[1]: (st.checkbox(model[1]), model) for model in st.session_state['trained_models']}
#        selected_models2
        # selected_models = {model['name']: st.checkbox(model['name']) for model in MODELS}
    st.markdown(markdown[2])
    with open('markdowns/save_data.md', 'r') as file:
        save_data_markdown = file.read().split('[[[[')
    file.close()
    st.markdown(save_data_markdown[0])
except:
    with open('markdowns/skipped_page.md') as file:
        markdown = file.read()
    st.markdown(markdown)
