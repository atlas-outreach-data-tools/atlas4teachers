import streamlit as st
import os
import json
import threading
from root_browser import RootFileBrowser
from utils import load_markdown_file_with_images_and_code, get_first_level_headers, load_markdown_preview


# explenation of every type
DESCRIPTIONS = {
    "runNumber": "Type: Int \nNumber uniquely identifying ATLAS data-taking run",
    "eventNumber": "Type: Int \nEvent number and run number combined uniquely identifies event",
    "channelNumber": "Type: Int \nNumber uniquely identifying ATLAS simulated dataset",
    "mcWeight": "Type: Float \nWeight of a simulated event",
    "XSection": "Type: Float \nTotal cross-section, including filter efficiency and higher-order correction factor",
    "SumWeights": "Type: Float \nGenerated sum of weights for MC process",
    "scaleFactor_PILEUP": "Type: Float \nScale-factor for pileup reweighting",
    "scaleFactor_ELE": "Type: Float \nScale-factor for electron efficiency",
    "scaleFactor_MUON": "Type: Float \nScale-factor for muon efficiency",
    "scaleFactor_PHOTON": "Type: Float \nScale-factor for photon efficiency",
    "scaleFactor_TAU": "Type: Float \nScale-factor for tau efficiency",
    "scaleFactor_BTAG": "Type: Float \nScale-factor for b-tagging algorithm @70% efficiency",
    "scaleFactor_LepTRIGGER": "Type: Float \nScale-factor for lepton triggers",
    "scaleFactor_PhotonTRIGGER": "Type: Float \nScale-factor for photon triggers",
    "trigE": "Type: Bool \nIndicates if the event passes a single-electron trigger",
    "trigM": "Type: Bool \nIndicates if the event passes a single-muon trigger",
    "trigP": "Type: Bool \nIndicates if the event passes a diphoton trigger",
    "lep_n": "Type: Int \nNumber of pre-selected leptons",
    "lep_truthMatched": "Type: Vector<Bool> \nIndicates if the lepton is matched to a simulated lepton",
    "lep_trigMatched": "Type: Vector<Bool> \nIndicates if the lepton is the one triggering the event",
    "lep_pt": "Type: Vector<Float> \nTransverse momentum of the lepton",
    "lep_eta": "Type: Vector<Float> \nPseudo-rapidity (η) of the lepton",
    "lep_phi": "Type: Vector<Float> \nAzimuthal angle (φ) of the lepton",
    "lep_E": "Type: Vector<Float> \nEnergy of the lepton",
    "lep_z0": "Type: Vector<Float> \nZ-coordinate of the lepton track wrt. primary vertex",
    "lep_charge": "Type: Vector<Int> \nCharge of the lepton",
    "lep_type": "Type: Vector<Int> \nSignifying the lepton type (e or µ)",
    "lep_isTightID": "Type: Vector<Bool> \nIndicates if the lepton satisfies tight ID reconstruction criteria",
    "lep_ptcone30": "Type: Vector<Float> \nSum of track pT in a cone of R=0.3 around lepton (tracking isolation)",
    "lep_etcone20": "Type: Vector<Float> \nSum of track ET in a cone of R=0.2 around lepton (calorimeter isolation)",
    "lep_trackd0pvunbiased": "Type: Vector<Float> \nd0 of lepton track at point of closest approach",
    "lep_tracksigd0pvunbiased": "Type: Vector<Float> \nd0 significance of lepton track at point of closest approach",
    "met_et": "Type: Float \nTransverse energy of the missing momentum vector",
    "met_phi": "Type: Float \nAzimuthal angle of the missing momentum vector",
    "jet_n": "Type: Int \nNumber of pre-selected jets",
    "jet_pt": "Type: Vector<Float> \nTransverse momentum of the jet",
    "jet_eta": "Type: Vector<Float> \nPseudo-rapidity (η) of the jet",
    "jet_phi": "Type: Vector<Float> \nAzimuthal angle (φ) of the jet",
    "jet_E": "Type: Vector<Float> \nEnergy of the jet",
    "jet_jvt": "Type: Vector<Float> \nJet vertex tagger discriminant",
    "jet_trueflav": "Type: Vector<Int> \nFlavour of the simulated jet",
    "jet_truthMatched": "Type: Vector<Bool> \nIndicates if the jet is matched to a simulated jet",
    "jet_MV2c10": "Type: Vector<Float> \nOutput from the multivariate b-tagging algorithm",
    "photon_n": "Type: Int \nNumber of pre-selected photons",
    "photon_truthMatched": "Type: Vector<Bool> \nIndicates if the photon is matched to a simulated photon",
    "photon_trigMatched": "Type: Vector<Bool> \nIndicates if the photon is the one triggering the event",
    "photon_pt": "Type: Vector<Float> \nTransverse momentum of the photon",
    "photon_eta": "Type: Vector<Float> \nPseudo-rapidity of the photon",
    "photon_phi": "Type: Vector<Float> \nAzimuthal angle of the photon",
    "photon_E": "Type: Vector<Float> \nEnergy of the photon",
    "photon_isTightID": "Type: Vector<Bool> \nIndicates if the photon satisfies tight ID reconstruction criteria",
    "photon_ptcone30": "Type: Vector<Float> \nSum of track pT in a cone of R=0.3 around photon",
    "photon_etcone20": "Type: Vector<Float> \nSum of track ET in a cone of R=0.2 around photon",
    "photon_convType": "Type: Vector<Int> \nInformation about photon conversion",
    "largeRjet_n": "Type: Int \nNumber of pre-selected large-R jets",
    "largeRjet_pt": "Type: Vector<Float> \nTransverse momentum of the large-R jet",
    "largeRjet_eta": "Type: Vector<Float> \nPseudo-rapidity of the large-R jet",
    "largeRjet_phi": "Type: Vector<Float> \nAzimuthal angle of the large-R jet",
    "largeRjet_E": "Type: Vector<Float> \nEnergy of the large-R jet",
    "largeRjet_m": "Type: Vector<Float> \nInvariant mass of the large-R jet",
    "largeRjet_truthMatched": "Type: Vector<Int> \nIndicates if the large-R jet is matched to a simulated jet",
    "largeRjet_D2": "Type: Vector<Float> \nAlgorithm weight for W/Z-boson tagging",
    "largeRjet_tau32": "Type: Vector<Float> \nAlgorithm weight for top-quark tagging",
    "tau_n": "Type: Int \nNumber of pre-selected hadronically decaying τ-leptons",
    "tau_pt": "Type: Vector<Float> \nTransverse momentum of the hadronically decaying τ-lepton",
    "tau_eta": "Type: Vector<Float> \nPseudo-rapidity of the hadronically decaying τ-lepton",
    "tau_phi": "Type: Vector<Float> \nAzimuthal angle of the hadronically decaying τ-lepton",
    "tau_E": "Type: Vector<Float> \nEnergy of the hadronically decaying τ-lepton",
    "tau_charge": "Type: Vector<Int> \nCharge of the hadronically decaying τ-lepton",
    "tau_isTightID": "Type: Vector<Bool> \nIndicates if τ-lepton satisfies tight ID reconstruction criteria",
    "tau_truthMatched": "Type: Vector<Bool> \nIndicates if the τ-lepton is matched to a simulated τ-lepton",
    "tau_trigMatched": "Type: Vector<Bool> \nIndicates if the τ-lepton triggered the event",
    "tau_nTracks": "Type: Vector<Int> \nNumber of tracks in the τ-lepton decay",
    "tau_BDTid": "Type: Vector<Float> \nOutput of multivariate τ-lepton discrimination algorithm",
    "ditau_m": "Type: Float \nDi-τ invariant mass using the missing-mass calculator",
    "lep_pt_syst": "Type: Vector<Float> \nSystematic uncertainty for lepton momentum scale and resolution",
    "met_et_syst": "Type: Float \nSystematic uncertainty for MET scale and resolution",
    "jet_pt_syst": "Type: Vector<Float> \nSystematic uncertainty for jet energy scale",
    "photon_pt_syst": "Type: Vector<Float> \nSystematic uncertainty for photon energy scale and resolution",
    "largeRjet_pt_syst": "Type: Vector<Float> \nSystematic uncertainty for large-R jet energy resolution",
    "tau_pt_syst": "Type: Vector<Float> \nSystematic uncertainty for τ-lepton reconstruction and energy scale",
}

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
    
    # Create the file browser
    browser = RootFileBrowser(descriptions=DESCRIPTIONS)
    
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
            
            browser.browse_root_file(selected_language) # Call the root browser function
            
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