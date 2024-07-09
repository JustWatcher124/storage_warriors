import streamlit as st
from helpers.train_models import main_st, MODELS
from helpers.helper_functions import only_selected_models


try:
    df = st.session_state['clean_dataframe']
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
    # st.write(only_selected_models(selected_models))
    train_them = st.button('Train These models')
    st.session_state['cleaning_options']['test_split'] = st.session_state['options']=20
    if train_them:
        # st.write(selected_models)
        # st.write(st.session_state['cleaning_options'])
        main_st(df, st.session_state['cleaning_options'], selected_models)
    st.markdown(markdown[2])
    with open('markdowns/save_data.md', 'r') as file:
        save_data_markdown = file.read().split('[[[[')
    file.close()
    st.markdown(save_data_markdown[0])
except:
    with open('markdowns/skipped_page.md') as file:
        markdown = file.read()
    st.markdown(markdown)

