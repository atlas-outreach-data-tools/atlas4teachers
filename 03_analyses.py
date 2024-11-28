import streamlit as st
from streamlit_theme import st_theme
import numpy as np
import uproot # for reading .root files
import awkward as ak # for handling complex and nested data structures efficiently
import pandas as pd
from utils_analysis import *
from PIL import Image
import base64
import os
import json
import random
import time
from utils import load_markdown_file_with_dynamic_content_and_alerts

def run(selected_language):
    # Initialize everything needed
    # Initialize flags to keep track of each step
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False

    if 'nlepton_cut_applied' not in st.session_state:
        st.session_state.nlepton_cut_applied = False

    if 'leptontype_cut_applied' not in st.session_state:
        st.session_state.leptontype_cut_applied = False

    if 'leptoncharge_cut_applied' not in st.session_state:
        st.session_state.leptoncharge_cut_applied = False

    if 'leptonpt_cut_applied' not in st.session_state:
        st.session_state.leptonpt_cut_applied = False

    if 'invariant_mass_calculated' not in st.session_state:
        st.session_state.invariant_mass_calculated = False
    
    if 'mc_loaded' not in st.session_state:
        st.session_state.mc_loaded = False

    # Initialize a special session state variable for the selectbox
    # This is so that the first cut option resets when using the reset analysis button
    if 'n_leptons_selection' not in st.session_state:
        st.session_state['n_leptons_selection'] = "--"

    # Initilize the expanders for the quizzes
    # First time they are expanded, when reseting they are not
    if 'expand_all' not in st.session_state:
        st.session_state['expand_all'] = True

    # Initialize session state for hint on lepton cut
    if 'show_hint' not in st.session_state:
        st.session_state['show_hint'] = False

    # Define a function to toggle the hint
    def toggle_hint():
        st.session_state['show_hint'] = not st.session_state['show_hint']

    if 'is_z' not in st.session_state:
        st.session_state['is_z'] = False

    if 'is_higgs' not in st.session_state:
        st.session_state['is_higgs'] = False

    # Get the current theme using st_theme
    theme = st_theme()

    # This is the json with all the info for all analyses
    # Build the path to the JSON file
    json_file_path = os.path.join('analyses', 'event_counts.json')
    # Open and load the JSON file
    with open(json_file_path, 'r') as json_file:
        analyses = json.load(json_file)

    # Opening the file with the quizzes
    quizzes_file_path = os.path.join('docs', selected_language.lower(), 'analyses', 'quizzes.json')

    # Load the quizzes JSON file
    try:
        with open(quizzes_file_path, 'r', encoding='utf-8') as quizzes_file:
            quizzes = json.load(quizzes_file)
    except FileNotFoundError:
        st.error(f"Quizzes file not found for language: {selected_language}. Check the file path.")
        st.stop()  # Stop the app if the file is missing
    except json.JSONDecodeError:
        st.error("Failed to decode the quizzes JSON file. Please check its format.")
        st.stop()  # Stop the app if the JSON is malformed
    
    # Opening the file with the cuts
    cuts_file_path = os.path.join('docs', selected_language.lower(), 'analyses', 'cuts.json')

    # Load the selections JSON file
    try:
        with open(cuts_file_path, 'r', encoding='utf-8') as cuts_file:
            cuts = json.load(cuts_file)
    except FileNotFoundError:
        st.error(f"Cuts file not found for language: {selected_language}. Check the file path.")
        st.stop()  # Stop the app if the file is missing
    except json.JSONDecodeError:
        st.error("Failed to decode the cuts JSON file. Please check its format.")
        st.stop()  # Stop the app if the JSON is malformed

    ###################################### HERE IS WERE THE APP STARTS #################################################

    # Introduction
    load_markdown_file_with_dynamic_content_and_alerts("introduction.md", "analyses", "english")

    # Luminosity
    load_markdown_file_with_dynamic_content_and_alerts("luminosity.md", "analyses", "english")

    # Create a dropdown for luminosity
    lumi = st.selectbox(
        'Select luminosity (fb$^{-1}$):',
        options=[12, 24, 36],
        index=0  # Default value (12 fb^-1)
    )

    if st.button("Open the data"):
        # Reset the steps, so that people cannot break it clicking again
        # Reset info for the events
        if st.session_state.nlepton_cut_applied:
            # Reset flags
            st.session_state.nlepton_cut_applied = False
            st.session_state.leptontype_cut_applied = False
            st.session_state.leptoncharge_cut_applied = False
            st.session_state.invariant_mass_calculated = False
            st.session_state.mc_loaded = False
            st.session_state.is_higgs = False
            st.session_state.is_z = False

            # Delete the widget keys from session_state
            for key in ['n_leptons_selection', 'flavor_selection', 'charge_pair_selection']:
                if key in st.session_state:
                    del st.session_state[key]
        
        # Reading the data
        random_sleep = random.randint(1,int(round(lumi/3)))
        # Display a spinner with the loading message
        with st.spinner("Loading data... Please wait."):
            # Simulate a time-consuming process with a random sleep
            time.sleep(random_sleep)

        st.session_state.data_loaded = True
        st.toast('Data loaded successfully!', icon='📈')
        
    if st.session_state.data_loaded:
        st.info(f" Initial number of events: {analyses[f'{lumi}']['nEvents']:,}")

        with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
            # Retrieve the quiz data from the JSON
            luminosity_quiz = quizzes["luminosity_quiz"]

            # Display the quiz title and question
            st.markdown(f"##### ⁉️ {luminosity_quiz['title']}")
            st.markdown(luminosity_quiz["question"].format(lumi=lumi))  # Format question with dynamic values like lumi

            # Display the options dynamically
            options = luminosity_quiz["options"]
            answer = st.radio("Choose your answer:", options, index=None, key="luminosity_quiz")

            # Check the selected answer and provide feedback
            if answer:
                # Get the correct option index
                correct_option_index = luminosity_quiz["correct_option_index"]
                
                # Compare the answer to the correct option
                if answer == options[correct_option_index]:
                    st.success(luminosity_quiz["feedback"]["0"])
                else:
                    st.error(luminosity_quiz["feedback"]["1"])

        # Using a selectbox to let users choose between amounts of leptons
        load_markdown_file_with_dynamic_content_and_alerts(
            filename="n_leptons.md",
            folder="analyses",
            language="english",
            theme=theme["base"],
            lumi=lumi)
        
        # Define the options
        n_leptons_options = cuts["n_leptons"]["selectbox_options"]

        # Create the selectbox
        n_leptons = st.selectbox(
            cuts["n_leptons"]["selectbox_label"],
            n_leptons_options,
            index=0,  # Default index for "--"
            key='n_leptons_selection'
        )

        # Access the selected value from session_state
        n_leptons = st.session_state['n_leptons_selection']

        if n_leptons == 2:
            st.success(cuts["n_leptons"]["messages"]["2"])
        elif n_leptons == 4:
            st.success(cuts["n_leptons"]["messages"]["4"])
        elif n_leptons != '--':
            st.warning(cuts["n_leptons"]["messages"]["3"])

        # Number of leptons button
        # We define a variable to avoid the page breaking when clicked more than once
        if st.button(cuts["n_leptons"]["apply_button"]):
            if st.session_state.nlepton_cut_applied:
                st.toast("You already applied a selection. To reset the analysis go to the end of the page.", icon='❌')
            elif n_leptons != '--':
                random_sleep = random.randint(1, round(lumi/6))
                # Display a spinner with the loading message
                with st.spinner("Making selection... Please wait."):
                    # Simulate a time-consuming process with a random sleep
                    time.sleep(random_sleep)
                st.session_state.nlepton_cut_applied = True
                st.toast("Selection applied successfully.", icon='✂️')
            else:
                st.error(cuts["n_leptons"]["error"])

    # Step 2: Dynamically generate selection for lepton flavors
    if st.session_state.nlepton_cut_applied:
        st.info(f"Events after the selection: {analyses[f'{lumi}'][f'{n_leptons}leptons']['nEvents']:,}")

        with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
            # Retrieve the quiz data from the JSON
            lepton_selection_quiz = quizzes["lepton_selection_quiz"]

            # Display the quiz title and question
            st.markdown(f"##### ⁉️ {lepton_selection_quiz['title']}")
            st.markdown(lepton_selection_quiz["question"])

            # Display the options dynamically
            options = lepton_selection_quiz["options"]
            answer_lepton = st.radio("Choose your answer:", options, index=None, key="lepton_selection_quiz")

            # Check the selected answer and provide feedback
            if answer_lepton:
                # Get the correct option index
                correct_option_index = lepton_selection_quiz["correct_option_index"]
                
                # Compare the answer to the correct option
                if answer_lepton == options[correct_option_index]:
                    st.success(lepton_selection_quiz["feedback"]["0"])
                else:
                    st.error(lepton_selection_quiz["feedback"]["1"])

        load_markdown_file_with_dynamic_content_and_alerts(
            filename="conservation.md",
            folder="analyses",
            language="english",
            theme=theme["base"],
            lumi=lumi)
        
        flavor_options = cuts['flavor']['selectbox_options']
        flavor = st.selectbox(cuts['flavor']['selectbox_label'], 
                              flavor_options, 
                              key="flavor_selection")

        if flavor == flavor_options[1]:
            st.success(cuts['flavor']['messages']['same'])
            
        elif flavor!= flavor_options[0]:
            st.warning(cuts['flavor']['messages']['different'])
            
        # Apply lepton type cut based on flavor selection
        if st.button(cuts['flavor']['apply_button']):
            if st.session_state.leptontype_cut_applied:
                st.toast("You already applied a selection. To reset the analysis go to the end of the page.", icon='❌')
            elif flavor != flavor_options[0]:    
                # Display a spinner with the loading message
                random_sleep = random.randint(1, round(lumi/6))
                with st.spinner("Making selection... Please wait."):
                    # Simulate a time-consuming process with a random sleep
                    time.sleep(random_sleep)

                # Display the cut result
                st.session_state.leptontype_cut_applied = True
                st.toast("Selection applied successfully.", icon='✂️')

            else:
                st.error(cuts['flavor']['error'])

    # Step 3: Dynamically generate selection for lepton charges
    if st.session_state.leptontype_cut_applied:
        st.info(f"Events after the selection: {analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}']['nEvents']:,}")

        # Offer options for charge pairing: Same charge or Opposite charge
        charge_pair_options = cuts['charge']['selectbox_options']
        charge = st.selectbox(cuts['charge']['selectbox_label'], 
                              charge_pair_options)

        # Define the condition for the charge mask based on the selection
        if charge == charge_pair_options[1]:
            st.warning(cuts['charge']['messages']['same'])
        elif charge != '--':
            st.success(cuts['flavor']['messages']['opposite'])

            # Apply lepton type cut based on flavor selection
        if st.button(cuts['charge']['apply_button']):
            if st.session_state.leptoncharge_cut_applied:
                st.toast("You already applied a selection. To reset the analysis go to the end of the page.", icon='❌')
            elif charge != '--':
                # Display a spinner with the loading message
                random_sleep = random.randint(1, round(lumi/6))
                with st.spinner("Making selection... Please wait."):
                    # Simulate a time-consuming process with a random sleep
                    time.sleep(random_sleep)
                    st.session_state.leptoncharge_cut_applied = True

                    # Provide feedback to the user
                    st.toast("Selection applied successfully.", icon='✂️')
            else:
                st.error(cuts['charge']['error'])

        if st.session_state.leptoncharge_cut_applied:
            st.info(f"Events after the selection: {analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['nEvents']:,}")

        
            with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
                # Retrieve the quiz data from the JSON
                charge_selection_quiz = quizzes["charge_selection_quiz"]

                # Display the quiz title and question
                st.markdown(f"##### ⁉️ {charge_selection_quiz['title']}")
                st.markdown(charge_selection_quiz["question"].format(charge=charge))

                # Display the options dynamically
                options = charge_selection_quiz["options"]
                answer_charge = st.radio("Choose your answer:", options, index=None, key="charge_selection_quiz")

                # Check the selected answer and provide feedback
                if answer_charge:
                    # Get the correct option index
                    correct_option_index = charge_selection_quiz["correct_option_index"]
                    
                    # Compare the answer to the correct option
                    if answer_charge == options[correct_option_index]:
                        st.success(charge_selection_quiz["feedback"]["0"])
                    else:
                        st.error(charge_selection_quiz["feedback"]["1"])
                
                if n_leptons==2 and flavor=='Same' and charge=='Opposite':
                    st.session_state.is_z = True
                if n_leptons==4 and flavor=='Same' and charge=='Opposite':
                    st.session_state.is_higgs = True

    # Step 4: Cuts on leptons pT only for Higgs
    if st.session_state.leptoncharge_cut_applied and st.session_state.is_higgs:
        load_markdown_file_with_dynamic_content_and_alerts(
            filename="pt_cut.md",
            folder="analyses",
            language="english")

        # Display initial image
        if not st.session_state['show_hint']:
            st.image(f"images/lepton_pt_{theme['base']}.png", caption="pT distribution of the three most energetic leptons in each event.")
        else:
            st.image(f"images/lepton_pt_{theme['base']}_lines.png", caption="pT distribution of the three most energetic leptons in each event with possible cuts.")

        st.markdown("With this in mind, let's consider the best lower bound cuts on p$_T$ that would help in filtering out background events while retaining those that are likely Higgs candidates.")
        with st.expander("🔍 Quiz", expanded=True):
            # Retrieve the quiz data from the JSON
            pt_cut_quiz = quizzes["pt_cut_quiz"]

            # Display the quiz title and question
            st.markdown(f"##### ⁉️ {pt_cut_quiz['title']}")
            st.markdown(pt_cut_quiz["question"])

            # Display the options dynamically
            options = pt_cut_quiz["options"]
            answer_cut = st.radio("Select the best option for p$_T$ cuts:", options, index=None, key="pt_cut_quiz")

            # Display the hint toggle button
            st.button(
                "Want a hint? Click here and check the image above" if not st.session_state['show_hint'] else "Hide Hint", 
                on_click=toggle_hint
            )

            # Check the selected answer and provide feedback
            if answer_cut:
                # Get the correct option index
                correct_option_index = pt_cut_quiz["correct_option_index"]
                
                # Compare the answer to the correct option
                if answer_cut == options[correct_option_index]:
                    st.success(pt_cut_quiz["feedback"]["0"])
                else:
                    st.error(pt_cut_quiz["feedback"]["1"])
            

        st.markdown("Now, let's make the cut:")

        if st.button("Cut on leptons p$_T$"):
            if st.session_state.leptonpt_cut_applied:
                st.toast("You already applied a cut. To reset the analysis go to the end of the page.", icon='❌')
            else:
                st.session_state.leptonpt_cut_applied = True
                # Display a spinner with the loading message
                random_sleep = random.randint(1, round(lumi/3))
                with st.spinner("Making cut... Please wait."):
                    # Simulate a time-consuming process with a random sleep
                    time.sleep(random_sleep)
                    st.session_state.leptoncharge_cut_applied = True

                    # Provide feedback to the user
                    st.toast("Cut applied successfully.", icon='✂️')
    
    if st.session_state.leptonpt_cut_applied:
        st.info(f"Events after the cut: {analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['ptLeptons']['nEvents']}")

    # Steep 5: invariant mass plot
    if (st.session_state.leptoncharge_cut_applied and not st.session_state.is_higgs) or (st.session_state.is_higgs and st.session_state.leptonpt_cut_applied):
        load_markdown_file_with_dynamic_content_and_alerts(
            filename="invariant_mass.md",
            folder="analyses",
            language="english")
        
        with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
            # Retrieve the quiz data from the JSON
            invariant_mass_quiz = quizzes["invariant_mass_selection_quiz"]

            # Display the quiz title and question
            st.markdown(f"##### ⁉️ {invariant_mass_quiz['title']}")
            st.markdown(invariant_mass_quiz["question"])

            # Display the options dynamically
            options = invariant_mass_quiz["options"]
            answer_mass = st.radio("Choose your answer:", options, index=None, key="invariant_mass_selection_quiz")

            # Check the selected answer and provide feedback
            if answer_mass:
                # Get the correct option index
                correct_option_index = invariant_mass_quiz["correct_option_index"]
                
                # Compare the answer to the correct option
                if answer_mass == options[correct_option_index]:
                    st.success(invariant_mass_quiz["feedback"]["0"])
                else:
                    st.error(invariant_mass_quiz["feedback"]["1"])

        if st.button("Get invariant mass"):
            st.session_state.invariant_mass_calculated = True
    # Step 6: Discussion
    if st.session_state.invariant_mass_calculated:
        if st.session_state.is_higgs:
                #st.info(f"Events after the cut: {analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['ptLeptons']['nEvents']}")
                st.image('analyses/'+analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['ptLeptons'][f"plot_data_only_{theme['base']}"])
        else:
            st.image('analyses/'+analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}'][f"plot_data_only_{theme['base']}"])
        
        if not st.session_state.is_higgs:
            with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
                # Retrieve the quiz data from the JSON
                invariant_mass_Z_quiz = quizzes["invariant_mass_Z"]

                # Display the quiz title and question
                st.markdown(f"##### ⁉️ {invariant_mass_Z_quiz['title']}")
                st.markdown(invariant_mass_Z_quiz["question"])

                # Display the options dynamically
                options = invariant_mass_Z_quiz["options"]
                answer_final = st.radio("Choose your answer:", options, index=None, key="invariant_mass_quiz")

                # Check the selected answer and provide feedback
                if answer_final:
                    # Get the correct option index
                    correct_option_index = invariant_mass_Z_quiz["correct_option_index"]
                    
                    # Compare the answer to the correct option
                    if answer_final == options[correct_option_index]:
                        st.success(invariant_mass_Z_quiz["feedback"]["0"])
                    else:
                        st.error(invariant_mass_Z_quiz["feedback"]["1"])
        
            if answer_final == options[correct_option_index]:
                if st.session_state.is_z:
                    st.balloons()
                load_markdown_file_with_dynamic_content_and_alerts(
                filename="discussion.md",
                folder="analyses",
                language="english")
        else:
            st.markdown("## How do we know we found the Higgs?")

            st.markdown("""
            To determine if we've observed the Higgs boson, we compare our real data with simulations of known background processes and simulated signals. This approach helps us see if a peak stands out in our data where we expect the Higgs boson to appear.
            """)

            # Step 1: Show data only
            st.markdown("### Step 1: Observing the Data")
            st.markdown("Let's start by looking at the data alone. Look carefully: do you notice any specific features? Without additional information, it can be challenging to tell whether any peaks are due to background processes or signal events.")
            higgs_data_only = 'analyses/'+analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['ptLeptons'][f"plot_data_only_{theme['base']}"]
            st.image(higgs_data_only, caption="Observed data alone")

            # Retrieve the quiz data from the JSON
            data_only_plot_quiz = quizzes["data_only_plot_quiz"]

            # Quiz question for the data-only plot
            quiz_data = st.radio(
                data_only_plot_quiz["question"],
                options=data_only_plot_quiz["options"],
                index=None,
                key="data_only_plot_quiz"
            )

            # Provide feedback based on the selected answer
            if quiz_data == data_only_plot_quiz["options"][1]:  # "Some fluctuations, but it's hard to tell"
                st.success(data_only_plot_quiz["feedback"]["1"])
            if quiz_data == data_only_plot_quiz["options"][0]:  # "A clear peak"
                st.warning(data_only_plot_quiz["feedback"]["0"])
            if quiz_data == data_only_plot_quiz["options"][2]:  # "No specific features"
                st.info(data_only_plot_quiz["feedback"]["2"])
            
            if quiz_data:
                # Step 2: Show data with background simulation
                st.markdown("### Step 2: Adding Background Simulation")
                st.markdown("Now, we add a simulation of the background processes (without any signal). This shows us what we’d expect to see from other particles and interactions in the absence of the Higgs boson. Look closely: do any peaks in the data appear in addition to the background?")
                higgs_data_bkg = 'analyses/'+analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['ptLeptons'][f"plot_data_backgrounds_{theme['base']}"]
                st.image(higgs_data_bkg, caption="Data with background simulation")

                # Quiz question for data with background
                # Retrieve the quiz data from the JSON
                background_simulation_quiz = quizzes["background_simulation_quiz"]

                # Quiz question for the background simulation plot
                quiz_background = st.radio(
                    background_simulation_quiz["question"],
                    options=background_simulation_quiz["options"],
                    index=None,
                    key="background_simulation_quiz"
                )

                # Provide feedback based on the selected answer
                if quiz_background == background_simulation_quiz["options"][0]:  # "Yes, there seems to be an extra peak"
                    st.success(background_simulation_quiz["feedback"]["0"])

            
                if quiz_background:
                    # Step 3: Show data with background and simulated Higgs signal
                    st.markdown("### Step 3: Adding the Simulated Higgs Signal")
                    st.markdown("""
                    Finally, we add the simulation of the Higgs signal to see how well it matches with the data. If the data aligns with the background plus the Higgs signal simulation, we have strong evidence of the Higgs boson. Can you spot a clear peak where we expect the Higgs?
                    """)
                    higgs_data_bkg_sig = 'analyses/'+analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['ptLeptons'][f"plot_data_backgrounds_signal_{theme['base']}"]
                    st.image(higgs_data_bkg_sig, caption="Data with background and simulated Higgs signal")

                    # Final quiz question
                    # Retrieve the quiz data from the JSON
                    simulated_higgs_signal_quiz = quizzes["simulated_higgs_signal_quiz"]

                    # Quiz question for the simulated Higgs signal plot
                    quiz_signal = st.radio(
                        simulated_higgs_signal_quiz["question"],
                        options=simulated_higgs_signal_quiz["options"],
                        index=None,
                        key="simulated_higgs_signal_quiz"
                    )

                    # Provide feedback based on the selected answer
                    if quiz_signal == simulated_higgs_signal_quiz["options"][0]:  # "There’s a peak matching the Higgs signal"
                        st.success(simulated_higgs_signal_quiz["feedback"]["0"])

                    if quiz_signal == "There’s a peak matching the Higgs signal":
                        st.balloons()
                        st.markdown("---")
                        st.markdown("### Discussion")
                        st.markdown("You reached the end of the analysis, once you are happy with the result wait for the discussion or reset the analysis to try a new one.")
    

    # Reset button to start the analysis again
    if st.session_state.data_loaded:
        st.markdown('---')
        st.write("""If you want to reaply cuts click the `Restart Analysis` button.""")
        if st.button("Restart Analysis"):
                # Reset flags
                st.session_state.data_loaded = False
                st.session_state.nlepton_cut_applied = False
                st.session_state.leptontype_cut_applied = False
                st.session_state.leptoncharge_cut_applied = False
                st.session_state.leptonpt_cut_applied = False
                st.session_state.invariant_mass_calculated = False
                st.session_state.mc_loaded = False
                st.session_state.expand_all = False
                st.session_state.is_z = False
                st.session_state.is_higgs = False

                # Delete the widget keys from session_state
                for key in ['n_leptons_selection', 'flavor_selection', 'charge_pair_selection']:
                    if key in st.session_state:
                        del st.session_state[key]

                st.rerun()
                st.toast("The analysis has been restarted.")