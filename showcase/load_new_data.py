import streamlit as st
import pandas as pd
import os
import helpers.helper_functions as helper_functions 
from io import StringIO
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title='Load New Data', page_icon='images/icon.png')
try:
    if st.session_state['visited_homepage']:
        print('User visited Homepage')
    with open('markdowns/load_new_data.md', 'r') as file:
        markdown = file.read().split('[[[[')

    st.markdown(markdown[0])

    uploaded_files = st.file_uploader("Upload the file(s) that contain the data", type=['csv', 'parquet', 'xlsx', 'xls', 'odt'], accept_multiple_files=True)
    #st.write(uploaded_file)

    start_process_btn = st.button('That\' all of them')

    if start_process_btn and uploaded_files:  # check if the list if not an empty list
        io_list = []

        # To read file(s) as bytes:
        for file in uploaded_files:
            bytes_data = file.getvalue()
            #st.write(bytes_data)
            stringio = StringIO(file.getvalue().decode("utf-8"))
            #st.write(stringio)
        # To read file as string:
            #st.write(string_data)
            io_list.append(stringio) 
            #st.write(io_list)
        
        df = helper_functions.load_data_path_or_stringio(io_list)

        st.session_state['data_dataframe'] = df

        st.markdown(markdown[1])
    #    st.markdown('### Here are the first ten lines of your data')
        st.dataframe(df.head(10))
        st.markdown(markdown[3])        

    elif start_process_btn and not uploaded_files:
        st.markdown(markdowns[2])
except KeyError:
    with open('markdowns/skipped_page.md') as file:
        markdown = file.read()
    st.markdown(markdown)
