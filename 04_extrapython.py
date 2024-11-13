import streamlit as st
import os
import json
import threading
from rootbrowser import root_browser
from utils import load_markdown_file_with_images_and_code, get_first_level_headers, load_markdown_preview

def run(selected_language):
    # Shared global namespace across all cells
    global_namespace = {}

    # Folder where markdown files are stored
    folder = "python"

    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # Build the path to the JSON file
    json_file_path = os.path.join(script_dir, f'docs/{selected_language.lower()}', 'extras.json')
    # Open and load the JSON file
    with open(json_file_path, 'r') as json_file:
        extras = json.load(json_file)

    # Initialize session state for expanded state of sections
    if "expanded_intro" not in st.session_state:
        st.session_state["expanded_intro"] = False
    if "expanded_histograms" not in st.session_state:
        st.session_state["expanded_histograms"] = False

    # Create paths and titles for each section
    general_info = '00_before_class.md'
    tabs_path = ['01_intro.md', '02_histograms.md', '03_histograms.md']
    tab_titles = get_first_level_headers(selected_language, folder, tabs_path)

    load_markdown_file_with_images_and_code(general_info, folder, {}, selected_language)
     
    # Create the tabs
    tabs = st.tabs(tab_titles)
    # Get the start/done buttons
    start, done = extras["start_done"][0], extras["start_done"][1]
    
    # Tab 1: Introduction
    with tabs[0]:
        # Load preview for intro
        intro_preview = load_markdown_preview(tabs_path[0], folder, selected_language, lines=3)

        if not st.session_state["expanded_intro"]:
            # Show preview
            preview_lines = intro_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button(start, key="intro_read"):
                st.session_state["expanded_intro"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_with_images_and_code(tabs_path[0], folder, global_namespace, selected_language)
            if st.button(done, key="intro_done"):
                st.session_state["expanded_intro"] = False
                st.rerun()  # Refresh the app to show the preview again

    # Tab 2: Histograms
    with tabs[1]:
        # Load preview for histograms
        histograms_preview = load_markdown_preview(tabs_path[1], folder, selected_language, lines=3)
        
        histograms_preview2 = load_markdown_preview(tabs_path[2], folder, selected_language, lines=3)
        
        
        if not st.session_state["expanded_histograms"]:
            # Show preview
            preview_lines = histograms_preview.splitlines()
            preview_lines2 = histograms_preview2.splitlines()
            
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            
            st.write("\n".join(preview_lines2[0:]))  # Remaining lines as preview text
            
            if st.button(start, key="histograms_read"):
                st.session_state["expanded_histograms"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_with_images_and_code(tabs_path[1], folder, global_namespace, selected_language)
            
            root_browser() # Call the root browser function
            
            load_markdown_file_with_images_and_code(tabs_path[2], folder, global_namespace, selected_language)
            if st.button(done, key="histograms_done"):
                st.session_state["expanded_histograms"] = False
                st.rerun()  # Refresh the app to show the preview again

    # Making the tabs font bigger
    css = '''
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:1.08rem;
        }
    </style>
    '''

    st.markdown(css, unsafe_allow_html=True)