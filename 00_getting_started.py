import streamlit as st
from utils import load_markdown_file_with_images_and_code

def run(selected_language):
    folder = "getting_started"

    # Initialize session state for expanded state of sections
    if "expanded_intro" not in st.session_state:
        st.session_state["expanded_intro"] = False
    if "expanded_standard_model" not in st.session_state:
        st.session_state["expanded_standard_model"] = False

    tabs_path = ['00_intro.md']

    # Show full content
    load_markdown_file_with_images_and_code(tabs_path[0], folder, {}, selected_language)

    