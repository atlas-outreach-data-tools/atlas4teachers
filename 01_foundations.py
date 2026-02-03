import streamlit as st
import os
import json
from utils import load_markdown_file_combined, get_first_level_headers, load_markdown_preview

def run(selected_language):
    folder = "foundations"

    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # Build the path to the JSON file
    json_file_path = os.path.join(script_dir, f'docs/{selected_language.lower()}', 'extras.json')
    # Open and load the JSON file
    with open(json_file_path, 'r') as json_file:
        extras = json.load(json_file)

    # Initialize session state for expanded state of sections
    if "expanded_intro_01" not in st.session_state:
        st.session_state["expanded_intro_01"] = False
    if "expanded_sm_01" not in st.session_state:
        st.session_state["expanded_sm_01"] = False
    if "expanded_higgs_01" not in st.session_state:
        st.session_state["expanded_higgs_01"] = False
    if "expanded_unknown_01" not in st.session_state:
        st.session_state["expanded_unknown_01"] = False

    # Get the intro to the module
    general_info = '00_intro.md'
    # Create paths and titles for each section
    tabs_path = ['01_particles.md', '02_standard_model.md', '03_higgs.md', '04_unknown.md']
    tab_titles = get_first_level_headers(selected_language, folder, tabs_path)

    # Print the intro to the module
    load_markdown_file_combined(general_info, folder, selected_language)


    # Create the tabs
    tabs = st.tabs(tab_titles)
    # Get the start/done buttons
    start, done = extras["start_done"][0], extras["start_done"][1]

    # Tab 1: What are particles
    with tabs[0]:
        # Load preview
        intro_preview = load_markdown_preview(tabs_path[0], folder, selected_language, lines=3)

        if not st.session_state["expanded_intro_01"]:
            # Show preview
            preview_lines = intro_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button(start, key="intro_read_01", type='primary'):
                st.session_state["expanded_intro_01"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_combined(tabs_path[0], folder, selected_language)
            if st.button(done, key="intro_done_01", type='primary'):
                st.session_state["expanded_intro_01"] = False
                st.rerun()  # Refresh the app to show the preview again

    # Tab 2: The standard model
    with tabs[1]:
        standard_model_preview = load_markdown_preview(tabs_path[1], folder, selected_language, lines=3)
        if not st.session_state["expanded_sm_01"]:
            # Show preview
            preview_lines = standard_model_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button(start, key="standard_model_read_01", type='primary'):
                st.session_state["expanded_sm_01"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_combined(tabs_path[1], folder, selected_language)
            if st.button(done, key="standard_model_done_01", type='primary'):
                st.session_state["expanded_sm_01"] = False
                st.rerun()  # Refresh the app to show the preview again

    # Tab 3: The Higgs boson
    with tabs[2]:
        higgs_preview = load_markdown_preview(tabs_path[2], folder, selected_language, lines=3)
        if not st.session_state["expanded_higgs_01"]:
            # Show preview
            preview_lines = higgs_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button(start, key="higgs_read_01", type='primary'):
                st.session_state["expanded_higgs_01"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_combined(tabs_path[2], folder, selected_language)
            if st.button(done, key="higgs_done_01", type='primary'):
                st.session_state["expanded_higgs_01"] = False
                st.rerun()  # Refresh the app to show the preview again


    # Tab 4: The Unknown
    with tabs[3]:
        uknown_preview = load_markdown_preview(tabs_path[3], folder, selected_language, lines=3)
        if not st.session_state["expanded_unknown_01"]:
            # Show preview
            preview_lines = uknown_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button(start, key="unknown_read_01", type='primary'):
                st.session_state["expanded_unknown_01"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_combined(tabs_path[3], folder, selected_language)
            if st.button(done, key="unknown_done_01", type='primary'):
                st.session_state["expanded_unknown_01"] = False
                st.rerun()  # Refresh the app to show the preview again

    # Making the tabs font bigger
    css = '''
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:1.08rem;
        }
    </style>
    '''

    css_key = f"{selected_language.lower()}::foundations::tabs_css_loaded"
    if css_key not in st.session_state:
        st.markdown(css, unsafe_allow_html=True)
        st.session_state[css_key] = True