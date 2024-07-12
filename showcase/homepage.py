# Import Streamlit to allow for rendering by Streamlit
import streamlit as st

# Set Page configs
st.set_page_config(page_title='Homepage', page_icon='images/icon.png', layout='wide', initial_sidebar_state='expanded')

# as this page is only showing markdown and not doing anything: no try, except block. it is always allowed to buy us coffee

# load the page's markdown from the file (this makes changing the text easier)
with open('markdowns/homepage.md', 'r') as file:
    markdown = file.read()


st.markdown(markdown)
# allow user to go to some of the other pages through the navigation pane
st.session_state['visited_homepage'] = True
