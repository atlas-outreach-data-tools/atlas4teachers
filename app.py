import streamlit as st
from streamlit_option_menu import option_menu
from st_social_media_links import SocialMediaIcons

import importlib
import json
import importlib.util
import os

st.set_page_config(
    page_title="ATLAS for Teachers",
    page_icon="💥",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://opendata.atlas.cern/contact-us',
        'About': "# ATLAS Open Data in the Classroom"
    }
)

# Initialize session state for language selection
if "language_selected" not in st.session_state:
    st.session_state["language_selected"] = False

if "language" not in st.session_state:
    st.session_state["language"] = None

# Initialize session state for selected tab
if "selected_tab" not in st.session_state:
    st.session_state["selected_tab"] = None

# Initialize password protection state for analysis
if "analysis_unlocked" not in st.session_state:
    st.session_state["analyses_unlocked"] = False

# Define a callback function to set session state when "Proceed" button is clicked
def proceed(language):
    st.session_state["language_selected"] = True
    st.session_state["language"] = language

# Define a callback function to reset the language selection (for the "Change Language" button)
def reset_language():
    st.session_state["language_selected"] = False
    st.session_state["language"] = None

# Main page (landing page with language selection)
if not st.session_state["language_selected"]:
    st.title("Welcome to ATLAS Open Data in the Classroom")
    st.image('https://atlas.cern/sites/default/files/2024-07/ATLAS-open-data.jpg', width=630)
    st.write("Please select your language to continue:")
    
    # Dropdown for language selection
    language = st.selectbox("Select Language", ["English", "Spanish", "Italian"])
    
    # Proceed button with a callback function
    st.button("Proceed", on_click=proceed, args=(language,))

    social_media_links = [
    "https://x.com/ATLASexperiment",
    "https://www.facebook.com/ATLASexperiment",
    "https://www.instagram.com/atlasexperiment/",
    "https://www.tiktok.com/@atlasexperiment",
    "https://www.linkedin.com/company/atlas-collaboration",
    "https://www.youtube.com/c/ATLASExperiment",
    "https://www.threads.net/@atlasexperiment",
    ]

    social_media_icons = SocialMediaIcons(social_media_links)
    social_media_icons.render()

# # Check if English is selected
# elif st.session_state["language"] == "English":
else:
    # Get selected language
    selected_language = st.session_state['language']
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # Build the path to the JSON file
    json_file_path = os.path.join(script_dir, f'docs/{selected_language.lower()}', 'extras.json')
    # Open and load the JSON file
    with open(json_file_path, 'r') as json_file:
        extras = json.load(json_file)

    st.sidebar.title(extras['side_bar_title'])
    sidebar_top = st.sidebar.container()  # Create a container for the top part of the sidebar
    sidebar_bottom = st.sidebar.container()  # Create a container for the bottom part of the sidebar
    # Use the top container for the main menu
    with sidebar_top:
        tabs = extras['side_bar']
        selected_tab = option_menu(
            "",
            tabs,
            menu_icon="code",  # Customize menu icon (optional)
            default_index=0,
        )

    # Check if the selected tab has changed
    if st.session_state["selected_tab"] != selected_tab:
        st.session_state["selected_tab"] = selected_tab

    # Dynamically import and display the content of the selected tab
    if selected_tab == tabs[0]:
        module = importlib.import_module("00_getting_started")
        module.run(selected_language)

    elif selected_tab == tabs[1]:
        module = importlib.import_module("01_foundations")
        module.run(selected_language)

    elif selected_tab == tabs[2]:
        module = importlib.import_module("02_experimental")
        module.run(selected_language)

    elif selected_tab == tabs[3]:
        # Check if the tutorial has been completed
        if "tutorial_completed" not in st.session_state:
            st.session_state["tutorial_completed"] = False

        if not st.session_state["tutorial_completed"]:
            # Load the tutorial module
            if st.button(extras['tutorial']['already_done']):
                st.session_state["tutorial_completed"] = True
                st.rerun()
            module = importlib.import_module("03_analyses_tutorial")
            module.run(selected_language)

            # Add a "Finish Tutorial" button
            if st.button(extras['tutorial']['finish'], type='primary'):
                st.session_state["tutorial_completed"] = True
                st.rerun()
        else:
            # Add a "Finish Tutorial" button
            if st.button(extras['tutorial']['back']):
                st.session_state["tutorial_completed"] = False
                st.rerun()
            # Load the actual analyses module after completing the tutorial
            module = importlib.import_module("03_analyses")
            module.run(selected_language)
        

    elif selected_tab == tabs[4]:
        module = importlib.import_module("04_extrapython")
        module.run(selected_language)

    elif selected_tab == tabs[5]:
        module = importlib.import_module("05_class_toolkit")
        module.run(selected_language)


    # Use the bottom container to place the language section at the bottom
    with sidebar_bottom:
        st.sidebar.markdown("<br><br><br><br><br>", unsafe_allow_html=True)  
        st.sidebar.text(f"Language: {selected_language}")
        st.sidebar.button("Change Language", on_click=reset_language)
