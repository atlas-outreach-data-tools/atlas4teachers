import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import load_markdown_file_combined
import os
import json

def plot_barplot(data, column, ax, distribution_text, count_text):
    counts = data[column].value_counts(sort=False)
    ax.bar([2, 3, 4], [counts.get(2, 0), counts.get(3, 0), counts.get(4, 0)], alpha=0.7, color='orange')
    ax.set_xlabel(column)
    ax.set_ylabel(f"{count_text}")
    ax.set_title(f"{distribution_text} {column}")
    ax.set_xticks([2, 3, 4])
    ax.set_ylim(0, 500)  # Fixed y-axis

def plot_histogram(data, column, ax, histogram_text, frequency_text,bins=20):
    ax.hist(data[column], bins=np.linspace(0, 700, bins + 1), alpha=0.7)
    ax.set_xlabel(column)
    ax.set_ylabel(f"{frequency_text}")
    ax.set_title(f"{histogram_text} {column}")
    ax.set_xlim(-30, 700)  # Fixed x-axis
    ax.set_ylim(0, 190)  # Fixed y-axis

def run(selected_language):
    # Opening the file with the extras analysis part 
    extras_file_path = os.path.join('docs', selected_language.lower(), 'analyses/tutorial', 'extras.json')

    # Load the extras JSON file
    try:
        with open(extras_file_path, 'r', encoding='utf-8') as cuts_file:
            extras = json.load(cuts_file)
    except FileNotFoundError:
        st.error(f"Higgs file not found for language: {selected_language}. Check the file path.")
        st.stop()  # Stop the app if the file is missing
    except json.JSONDecodeError:
        st.error("Failed to decode the higgs JSON file. Please check its format.")
        st.stop()  # Stop the app if the JSON is malformed

    # Load mock data
    data = pd.read_csv("event_dataset.csv")

    # Streamlit app
    # Introduction to tutorial
    load_markdown_file_combined(filename='intro.md',
                                folder='analyses/tutorial',
                                language=selected_language)
    
    load_markdown_file_combined(filename='cuts.md', 
                                folder='analyses/tutorial', 
                                language=selected_language)
    
    load_markdown_file_combined(filename='dataset.md', 
                                folder='analyses/tutorial', 
                                language=selected_language)

    st.dataframe(data)

    # Column info
    load_markdown_file_combined(filename='columns.md', 
                                folder='analyses/tutorial', 
                                language=selected_language,
                                data = data.shape[0])
    
    # Initial visualization
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        plot_barplot(data, "nLeptons", ax, extras['distribution'], extras['count'])
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots()
        plot_histogram(data, "LeadingLeptonEnergy", ax, extras['histogram'], extras['frequency'])
        st.pyplot(fig)    

    # Selection: Filter by number of particles
    load_markdown_file_combined(filename='selection_cut.md', 
                                folder='analyses/tutorial', 
                                language=selected_language)

    selected_nLeptons = st.multiselect(
        "Choose the number of particles to include:",
        options=[2, 3, 4],
        default=[]
    )

    filtered_data = data[data["nLeptons"].isin(selected_nLeptons)]
    filtered_data.reset_index(inplace=True, drop=True)

    load_markdown_file_combined(filename='visualization.md', 
                                folder='analyses/tutorial', 
                                language=selected_language,
                                filtered_data_size=len(filtered_data),
                                filtered_data=filtered_data)

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        plot_barplot(filtered_data, "nLeptons", ax, extras['distribution'], extras['count'])
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots()
        plot_histogram(filtered_data, "LeadingLeptonEnergy", ax, extras['histogram'], extras['frequency'])
        st.pyplot(fig)   

    # Range: Filter by energy range
    load_markdown_file_combined(filename='range_cut.md', 
                                folder='analyses/tutorial', 
                                language=selected_language,
                                filtered_data_size=len(filtered_data),
                                filtered_data=filtered_data)
    
    min_energy, max_energy = st.slider(
        "Select energy range (GeV):",
        min_value=int(data["LeadingLeptonEnergy"].min()),
        max_value=int(data["LeadingLeptonEnergy"].max()),
        value=(20, 150)
    )
    filtered_data = filtered_data[
        (filtered_data["LeadingLeptonEnergy"] >= min_energy) & (filtered_data["LeadingLeptonEnergy"] <= max_energy)
    ]
    filtered_data.reset_index(inplace=True, drop=True)

    load_markdown_file_combined(filename='visualization_again.md', 
                                folder='analyses/tutorial', 
                                language=selected_language,
                                filtered_data_size=len(filtered_data),
                                filtered_data=filtered_data)

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        plot_barplot(filtered_data, "nLeptons", ax, extras['distribution'], extras['count'])
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots()
        plot_histogram(filtered_data, "LeadingLeptonEnergy", ax, extras['histogram'], extras['frequency'])
        st.pyplot(fig)   

    load_markdown_file_combined(filename='summary.md', 
                                folder='analyses/tutorial', 
                                language=selected_language)