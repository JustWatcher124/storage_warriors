# Import necessary modules, Streamlit for rendering, stringio for fileupload
import streamlit as st
from io import StringIO

# Import the helper_functions script to 'outsource' the backend
import helpers.helper_functions as helper_functions

# Set Page configs
st.set_page_config(page_title='Load New Data', page_icon='images/icon.png',
                   layout='wide', initial_sidebar_state='expanded')

# Check if User is on the right page using session_states variables
try:
    # exists only if user visited the homepage (mostly from reloading) -- causes exception caught below
    _ = st.session_state['visited_homepage']
    # load the default markdown from file
    with open('markdowns/load_new_data.md', 'r') as file:
        markdown = file.read().split('[[[[')

    st.markdown(markdown[0])

    # allow user to upload files to the system
    uploaded_files = st.file_uploader("Upload the file(s) that contain the data",
                                      type=['csv', 'parquet', 'xlsx', 'xls', 'odt'],
                                      accept_multiple_files=True)

    # handle the data_filename necessity of the system for single file and multi file uploads
    if len(uploaded_files) > 1:
        st.session_state['data_filename'] = st.selectbox(
            'Select a file name to store with the model or dataset later',
            options=[file.name for file in uploaded_files])
    elif uploaded_files:
        st.session_state['data_filename'] = uploaded_files[0].name
    start_process_btn = st.button('That\' all of them')
    if start_process_btn and uploaded_files:  # check if the list if not an empty list and start the loading process
        io_list = []
        # To read file(s) as bytes:
        for file in uploaded_files:
            bytes_data = file.getvalue()
            stringio = StringIO(file.getvalue().decode("utf-8"))
            io_list.append((stringio, file.name))

        # loads the stringio file(s) into pandas dataframes
        df = helper_functions.load_data_stringio(io_list)

        st.session_state['data_dataframe'] = df

        # I did not write the markdown in order and am not gonna change it. You can, just fork the repo
        st.markdown(markdown[3])
        st.markdown(markdown[1])
        st.dataframe(df.head(10))

    # show an error / missing files message to the user
    elif start_process_btn and not uploaded_files:
        st.markdown(markdown[2])
except:  # bare exception because this also makes errors clear to the user
    with open('markdowns/skipped_page.md') as file:
        markdown = file.read()
    st.markdown(markdown)
