import streamlit as st
import os
import json
from utils import load_markdown_file_combined, get_first_level_headers, load_markdown_preview

def run(selected_language):
    folder = "experimental"

    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # Build the path to the JSON file
    json_file_path = os.path.join(script_dir, f'docs/{selected_language.lower()}', 'extras.json')
    # Open and load the JSON file
    with open(json_file_path, 'r') as json_file:
        extras = json.load(json_file)

    # Initialize session state for expanded state of sections
    if "expanded_accelerators" not in st.session_state:
        st.session_state["expanded_accelerators"] = False
    if "expanded_detectors" not in st.session_state:
        st.session_state["expanded_detectors"] = False
    if "expanded_atlas" not in st.session_state:
        st.session_state["expanded_atlas"] = False

    # The intro to the module
    general_info = '00_intro.md'
    # Create paths and titles for each section
    tabs_path = ['01_accelerators.md', '02_detectors.md', '03_ATLAS.md']
    tab_titles = get_first_level_headers(selected_language, folder, tabs_path)

    # Print the intro to the module
    load_markdown_file_combined(general_info, folder, selected_language)

    # Create the tabs
    tabs = st.tabs(tab_titles)
    # Get the start/done buttons
    start, done = extras["start_done"][0], extras["start_done"][1]

    # Tab 1: Accelerators
    with tabs[0]:
        # Load preview for accelerators
        accelerators_preview = load_markdown_preview(tabs_path[0], folder, selected_language, lines=3)

        if not st.session_state["expanded_accelerators"]:
            # Show preview
            preview_lines = accelerators_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button(start, key="accelerators_read"):
                st.session_state["expanded_accelerators"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content and video
            load_markdown_file_combined(tabs_path[0], folder, selected_language)
            st.video("https://www.youtube.com/embed/pQhbhpU9Wrg")
            if st.button(done, key="accelerators_done"):
                st.session_state["expanded_accelerators"] = False
                st.rerun()  # Refresh the app to show the preview again

    # Tab 2: Detectors
    with tabs[1]:
        # Load preview for detectors
        detectors_preview = load_markdown_preview(tabs_path[1], folder, selected_language, lines=3)

        if not st.session_state["expanded_detectors"]:
            # Show preview
            preview_lines = detectors_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button(start, key="detectors_read"):
                st.session_state["expanded_detectors"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_combined(tabs_path[1], folder, selected_language)
            if st.button(done, key="detectors_done"):
                st.session_state["expanded_detectors"] = False
                st.rerun()  # Refresh the app to show the preview again

    # Tab 3: ATLAS
    with tabs[2]:
        # Load preview for detectors
        atlas_preview = load_markdown_preview(tabs_path[2], folder, selected_language, lines=3)

        if not st.session_state["expanded_atlas"]:
            # Show preview
            preview_lines = atlas_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button(start, key="atlas_read"):
                st.session_state["expanded_atlas"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_combined(tabs_path[2], folder, selected_language)
            if st.button(done, key="atlas_done"):
                st.session_state["expanded_atlas"] = False
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