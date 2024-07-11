import streamlit as st
import pandas as pd
import os
from helpers.clean_data import clean_dataframe


try:
    st.session_state['cleaned_data'] = False
    df = st.session_state['data_dataframe']
    with open('markdowns/clean_data.md', 'r') as file:
        markdown = file.read().split('[[[[')
    file.close()
    options = {}
    st.markdown(markdown[0])
    st.markdown(markdown[1])
    options['drop_columns'] = st.multiselect(
        'Select the columns that are unnecessary (speeds up training)', df.columns, default=None)
    st.markdown(markdown[2])
    options['wanted_value'] = st.selectbox(
        'Select the column that contains the values that the model should predict', options=set(df.columns) -
        set(options['drop_columns']))

    st.markdown(markdown[3])
    options['fillna_with'] = st.number_input(
        'Here you can put a number to replace nan values with in the column you chose in Step 3 (0 means no replacement and instead dropping)')
    st.markdown(markdown[4])
    differing_bounds = st.checkbox('Differing Lower and Upper Percentiles')
    if differing_bounds:
        winsor_percentile_upper = st.number_input(
            'Input an Upper percentile (between 50 and 100)', value=95, min_value=50, max_value=100)
        winsor_percentile_lower = st.number_input(
            'Input an Lower percentile (between 0 and 50)', value=5, min_value=0, max_value=50)
        options['winsor_percentile'] = (winsor_percentile_lower, winsor_percentile_upper)
    else:
        options['winsor_percentile'] = st.number_input(
            'Input a percentile (between 0 and 100) -- 0 or 100 do not make sense though', value=5, min_value=0, max_value=100)
    st.markdown(markdown[5])
    options['product_id'] = st.selectbox(
        'Select the column that contains an identifier for your products (id, name, etc.)', options=set(df.columns) -
        set(options['drop_columns']) - set(options['wanted_value']))
    st.markdown(markdown[6])
    options['date_column'] = st.selectbox(
        'Select the column that contains your timestamp or date', options=set(df.columns) -
        set(options['drop_columns']) - set(options['wanted_value']))
    submitted = st.button('Submit these Options')
    if submitted:
        st.session_state['cleaned_data'] = True
        # st.write(options)
        st.session_state['clean_dataframe'] = clean_dataframe(
            df, winsorize_this_value=options['wanted_value'],
            winsor_percentile=options['winsor_percentile'],
            fillna_value=options['fillna_with'],
            drop_columns=options['drop_columns'])
        st.session_state['cleaning_options'] = options
        st.markdown(markdown[7])


except KeyError:
    with open('markdowns/skipped_page.md') as file:
        markdown = file.read()
    st.markdown(markdown)
    st.session_state['cleaned_data'] = False
