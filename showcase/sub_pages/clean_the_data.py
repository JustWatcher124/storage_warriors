# Import necessary modules, Streamlit for rendering, pandas for data handling and cleaning
import streamlit as st
import pandas as pd
# Import the clean_dataframe function to 'outsource' the cleaning
from helpers.clean_data import clean_dataframe

# Set Page configs
st.set_page_config(page_title='Load New Data', page_icon='images/icon.png',
                   layout='wide', initial_sidebar_state='expanded')

# Check if User is on the right page using session_states variables
try:
    # exists only if user uploaded a dataset -- causes exception caught below
    df = st.session_state['data_dataframe']
    # load the default markdown from file
    with open('markdowns/clean_data.md', 'r') as file:
        markdown = file.read().split('[[[[')
    file.close()

    st.markdown(markdown[0])

    options = {}  # to capture user choices for cleaning options

    # allow user to drop some columns (is not necessary)
    st.markdown(markdown[1])
    options['drop_columns'] = st.multiselect(
        'Select the columns that are unnecessary (speeds up training)', df.columns, default=None)

    # make user choose the target variable
    st.markdown(markdown[2])
    options['wanted_value'] = st.selectbox(
        'Select the column that contains the values that the model should predict', options=set(df.columns) -
        set(options['drop_columns']))

    # allow user to maybe fill na, None, np.nan and other null values in the target variable set
    # Comment by dev on this issue: Should not be need tbh, if you have Nulls, either fill them yourself or be happy with the not-Nulls
    st.markdown(markdown[3])
    options['fillna_with'] = st.number_input(
        'Here you can put a number to replace nan values with in the column you chose in Step 3 (0 means no replacement and instead dropping)')

    # allow user to set winsoring percentiles (also handles differing upper and lower bounds)
    st.markdown(markdown[4])
    differing_bounds = st.checkbox('Differing Lower and Upper Percentiles')
    if differing_bounds:  # this handles differing upper and lower bounds
        winsor_percentile_upper = st.number_input(
            'Input an Upper percentile (between 50 and 100)', value=95, min_value=50, max_value=100)
        winsor_percentile_lower = st.number_input(
            'Input an Lower percentile (between 0 and 50)', value=5, min_value=0, max_value=50)
        options['winsor_percentile'] = (winsor_percentile_upper, winsor_percentile_lower)
    else:
        options['winsor_percentile'] = st.number_input(
            'Input a percentile (between 0 and 100) -- 0 or 100 do not make sense though', value=5, min_value=0, max_value=100)

    # make user choose the column where the ID they want to predict for is located
    st.markdown(markdown[5])
    options['product_id'] = st.selectbox(
        'Select the column that contains an identifier for your products (id, name, etc.)', options=set(df.columns) -
        set(options['drop_columns']) - set(options['wanted_value']))
    # make user choose the column where the date information about the data ist
    st.markdown(markdown[6])
    options['date_column'] = st.selectbox(
        'Select the column that contains your timestamp or date', options=set(df.columns) -
        set(options['drop_columns']) - set(options['wanted_value']))

    submitted = st.button('Submit these Options')
    if submitted:
        # this allows the user to go to Train or Save page
        # save the cleaned dataframe to memory
        st.session_state['clean_dataframe'] = clean_dataframe(
            df, winsorize_this_value=options['wanted_value'],
            winsor_percentile=options['winsor_percentile'],
            fillna_value=options['fillna_with'],
            drop_columns=options['drop_columns'])
        # save the options to session
        st.session_state['cleaning_options'] = options
        st.markdown(markdown[7])


except:  # bare exception because this also makes errors clear to the user
    with open('markdowns/skipped_page.md') as file:
        markdown = file.read()
    st.markdown(markdown)
