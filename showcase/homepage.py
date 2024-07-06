import streamlit as st
st.set_page_config(page_title='Homepage', page_icon='images/icon.png', layout='wide', initial_sidebar_state='expanded')

# as we use markdown to write the text and provide the formatting of our pages we store them in seperate files for easier wirting

with open('markdowns/homepage.md', 'r') as file:
    markdown_string = file.read()


st.markdown(markdown_string)
st.session_state['visited_homepage'] = True

