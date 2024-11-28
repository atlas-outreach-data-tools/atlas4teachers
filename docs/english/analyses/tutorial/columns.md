Intially, this dataset has {data} rows or events

##### Understanding the Columns
Here’s what the columns in the dataset mean:
- **EventID**: A unique identifier for each event recorded in the detector. Each event corresponds to a snapshot of what happens during a single particle collision in the detector.
- **nParticles**: The total number of particles reconstructed in the event. In this simplified mock dataset, we focus on events with 2, 3, or 4 particles, which is typical for certain analyses. In reality, particle counts can vary significantly depending on the physics process being studied.
- **LeptonType**: Indicates the type of lepton detected in the event—either an electron or a muon. While real events often involve a mix of particle types, this dataset simplifies the scenario by focusing on a single lepton type per event to highlight specific analyses.
- **Energy (GeV)**: The energy of the selected lepton in giga-electronvolts (GeV), ranging from 10 to 200 in this mock dataset. In practice, the energy recorded for an event comes from summing the contributions of all detected particles, and individual lepton energies are just one part of the full energy profile.