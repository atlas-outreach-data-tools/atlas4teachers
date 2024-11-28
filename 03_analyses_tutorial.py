import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import load_markdown_file_with_dynamic_content_and_alerts

# Generate mock dataset
def generate_mock_data():
    np.random.seed(42)
    data = {
        "EventID": np.arange(1, 501),
        "nParticles": np.random.choice([2, 3, 4], size=500),
        "LeptonType": np.random.choice(["Electron", "Muon"], size=500),
        "Energy": np.random.uniform(10, 200, size=500),  # Energy in GeV
    }
    return pd.DataFrame(data)

def run(selected_language):
    # Load mock data
    data = generate_mock_data()

    # Streamlit app
    # Introduction to tutorial
    load_markdown_file_with_dynamic_content_and_alerts(filename='intro.md', 
                                                       folder='analyses/tutorial', 
                                                       language=selected_language)
    
    st.dataframe(data)

    # Column info
    load_markdown_file_with_dynamic_content_and_alerts(filename='columns.md', 
                                                       folder='analyses/tutorial', 
                                                       language=selected_language,
                                                       data = data.shape[0])

    # A simple example of a cut
    load_markdown_file_with_dynamic_content_and_alerts(filename='cuts.md', 
                                                       folder='analyses/tutorial', 
                                                       language='english')

    # Apply the cut for next section example
    cut_data = data[data["Energy"] > 50]
    load_markdown_file_with_dynamic_content_and_alerts(filename='cut_example.md', 
                                                       folder='analyses/tutorial', 
                                                       language='english',
                                                       data = data.shape[0],
                                                       cut_data = cut_data,
                                                       cut_data_size = cut_data.shape[0])

    # Step 1: Filter by number of particles
    load_markdown_file_with_dynamic_content_and_alerts(filename='step_1.md', 
                                                       folder='analyses/tutorial', 
                                                       language='english')

    selected_nParticles = st.multiselect(
        "Choose the number of particles to include:",
        options=[2, 3, 4],
        default=[]
    )

    filtered_data = data[data["nParticles"].isin(selected_nParticles)]


    # Step 2: Filter by lepton type
    load_markdown_file_with_dynamic_content_and_alerts(filename='step_2.md', 
                                                       folder='analyses/tutorial', 
                                                       language='english',
                                                       filtered_data_size=len(filtered_data),
                                                       filtered_data=filtered_data)


    selected_lepton_types = st.multiselect(
        "Choose the lepton types to include:",
        options=["Electron", "Muon"],
        default=[]
    )

    filtered_data = filtered_data[filtered_data["LeptonType"].isin(selected_lepton_types)]

    # Step 3: Filter by energy range
    load_markdown_file_with_dynamic_content_and_alerts(filename='step_3.md', 
                                                       folder='analyses/tutorial', 
                                                       language='english',
                                                       filtered_data_size=len(filtered_data),
                                                       filtered_data=filtered_data)

    min_energy, max_energy = st.slider(
        "Select energy range (GeV):",
        min_value=float(data["Energy"].min()),
        max_value=float(data["Energy"].max()),
        value=(20.0, 150.0)
    )
    filtered_data = filtered_data[
        (filtered_data["Energy"] >= min_energy) & (filtered_data["Energy"] <= max_energy)
    ]

    st.write(f"Filtered dataset contains {len(filtered_data)} events.")
    st.dataframe(filtered_data.head(10))

    # Visualization
    load_markdown_file_with_dynamic_content_and_alerts(filename='visualization.md', 
                                                       folder='analyses/tutorial', 
                                                       language=selected_language)

    fig, ax = plt.subplots()
    ax.hist(filtered_data["Energy"], bins=20, alpha=0.7)
    ax.set_xlabel("Energy (GeV)")
    ax.set_ylabel("Number of Events")
    ax.set_title("Energy Distribution After Cuts")
    st.pyplot(fig)

    load_markdown_file_with_dynamic_content_and_alerts(filename='summary.md', 
                                                       folder='analyses/tutorial', 
                                                       language=selected_language)