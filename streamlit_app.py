import streamlit as st
import utils
import os
import uuid
import json

# Set the page title and icon
st.set_page_config(
    page_title="Jarvis",  # Set the tab name here
    page_icon=":sparkles:",  # Optional: Add an icon emoji
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

# with st.sidebar:
#     st.header("Admin Panel",divider=True)
#     st.subheader("Welcome&nbsp;&nbsp;&nbsp;Jhon")


# -- Page Setup --

add_context_page=st.Page(
    page="views/add_context.py",
    title="Add Context",
    # icon=":file_folder:",  # Optional: Add an icon emoji
    # description="Add Context to the Vector DB",
)

update_agent_configuration_page=st.Page(
    page="views/update_agent_configuration.py",
    title="Update Agent Configuration",
    # icon=":gear:",  # Optional: Add an icon emoji
    # description="Update Agent Configuration",
)

user_chat=st.Page(
    page="views/user_chat.py",
    title="User Chat",
    # icon=":gear:",  # Optional: Add an icon emoji
    # description="Update Agent Configuration",
)

# -- Page Navigation --
pg = st.navigation(
    pages=[add_context_page, update_agent_configuration_page, user_chat],
    )

#-- Run the selected page --
pg.run()