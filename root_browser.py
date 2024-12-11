import streamlit as st
import uproot
import streamlit_antd_components as sac
import matplotlib.pyplot as plt

# explenation of every type
DESCRIPTIONS = {
    "runNumber": {
        "English": "Type: Int \nNumber uniquely identifying ATLAS data-taking run",
        "Spanish": "Tipo: Int \nNúmero que identifica de manera única el run de adquisición de datos ATLAS",
    },
    "eventNumber": {
        "English": "Type: Int \nEvent number and run number combined uniquely identifies event",
        "Spanish": "Tipo: Int \nEl número de evento y el número de run combinados identifican de manera única el evento",
    },
    "channelNumber": {
        "English": "Type: Int \nNumber uniquely identifying ATLAS simulated dataset",
        "Spanish": "Tipo: Int \nNúmero que identifica de manera única el conjunto de datos simulado de ATLAS",
    },
    "mcWeight": {
        "English": "Type: Float \nWeight of a simulated event",
        "Spanish": "Tipo: Float \nPeso de un evento simulado",
    },
    "XSection": {
        "English": "Type: Float \nTotal cross-section, including filter efficiency and higher-order correction factor",
        "Spanish": "Tipo: Float \nSección transversal total, incluyendo la eficiencia del filtro y el factor de corrección de orden superior",
    },
    "SumWeights": {
        "English": "Type: Float \nGenerated sum of weights for MC process",
        "Spanish": "Tipo: Float \nSuma generada de los pesos para el proceso MC",
    },
    "scaleFactor_PILEUP": {
        "English": "Type: Float \nScale-factor for pileup reweighting",
        "Spanish": "Tipo: Float \nFactor de escala para el reajuste de pileup",
    },
    "scaleFactor_ELE": {
        "English": "Type: Float \nScale-factor for electron efficiency",
        "Spanish": "Tipo: Float \nFactor de escala para la eficiencia del electrón",
    },
    "scaleFactor_MUON": {
        "English": "Type: Float \nScale-factor for muon efficiency",
        "Spanish": "Tipo: Float \nFactor de escala para la eficiencia del muón",
    },
    "scaleFactor_PHOTON": {
        "English": "Type: Float \nScale-factor for photon efficiency",
        "Spanish": "Tipo: Float \nFactor de escala para la eficiencia del fotón",
    },
    "scaleFactor_TAU": {
        "English": "Type: Float \nScale-factor for tau efficiency",
        "Spanish": "Tipo: Float \nFactor de escala para la eficiencia del tau",
    },
    "scaleFactor_BTAG": {
        "English": "Type: Float \nScale-factor for b-tagging algorithm @70% efficiency",
        "Spanish": "Tipo: Float \nFactor de escala para el algoritmo de b-tagging a una eficiencia del 70%",
    },
    "scaleFactor_LepTRIGGER": {
        "English": "Type: Float \nScale-factor for lepton triggers",
        "Spanish": "Tipo: Float \nFactor de escala para los triggers de leptones",
    },
    "scaleFactor_PhotonTRIGGER": {
        "English": "Type: Float \nScale-factor for photon triggers",
        "Spanish": "Tipo: Float \nFactor de escala para los triggers de fotones",
    },
    "trigE": {
        "English": "Type: Bool \nIndicates if the event passes a single-electron trigger",
        "Spanish": "Tipo: Bool \nIndica si el evento pasa un trigger de electrón único",
    },
    "trigM": {
        "English": "Type: Bool \nIndicates if the event passes a single-muon trigger",
        "Spanish": "Tipo: Bool \nIndica si el evento pasa un trigger de muón único",
    },
    "trigP": {
        "English": "Type: Bool \nIndicates if the event passes a diphoton trigger",
        "Spanish": "Tipo: Bool \nIndica si el evento pasa un trigger de diphotones",
    },
    "lep_n": {
        "English": "Type: Int \nNumber of pre-selected leptons",
        "Spanish": "Tipo: Int \nNúmero de leptones preseleccionados",
    },
    "lep_truthMatched": {
        "English": "Type: Vector<Bool> \nIndicates if the lepton is matched to a simulated lepton",
        "Spanish": "Tipo: Vector<Bool> \nIndica si el leptón está emparejado con un leptón simulado",
    },
    "lep_trigMatched": {
        "English": "Type: Vector<Bool> \nIndicates if the lepton is the one triggering the event",
        "Spanish": "Tipo: Vector<Bool> \nIndica si el leptón es el que dispara el evento",
    },
    "lep_pt": {
        "English": "Type: Vector<Float> \nTransverse momentum of the lepton",
        "Spanish": "Tipo: Vector<Float> \nMomentum transversal del leptón",
    },
    "lep_eta": {
        "English": "Type: Vector<Float> \nPseudo-rapidity (η) of the lepton",
        "Spanish": "Tipo: Vector<Float> \nPseudo-rapidez (η) del leptón",
    },
    "lep_phi": {
        "English": "Type: Vector<Float> \nAzimuthal angle (φ) of the lepton",
        "Spanish": "Tipo: Vector<Float> \nÁngulo azimutal (φ) del leptón",
    },
    "lep_E": {
        "English": "Type: Vector<Float> \nEnergy of the lepton",
        "Spanish": "Tipo: Vector<Float> \nEnergía del leptón",
    },
    "lep_z0": {
        "English": "Type: Vector<Float> \nZ-coordinate of the lepton track wrt. primary vertex",
        "Spanish": "Tipo: Vector<Float> \nCoordenada Z de la pista del leptón respecto al vértice primario",
    },
    "lep_charge": {
        "English": "Type: Vector<Int> \nCharge of the lepton",
        "Spanish": "Tipo: Vector<Int> \nCarga del leptón",
    },
    "lep_type": {
        "English": "Type: Vector<Int> \nSignifying the lepton type (e or µ)",
        "Spanish": "Tipo: Vector<Int> \nSignifica el tipo de leptón (e o µ)",
    },
    "lep_isTightID": {
        "English": "Type: Vector<Bool> \nIndicates if the lepton satisfies tight ID reconstruction criteria",
        "Spanish": "Tipo: Vector<Bool> \nIndica si el leptón satisface los criterios estrictos de reconstrucción de ID",
    },
    "lep_ptcone30": {
        "English": "Type: Vector<Float> \nSum of track pT in a cone of R=0.3 around lepton (tracking isolation)",
        "Spanish": "Tipo: Vector<Float> \nSuma de pT de las pistas en un cono de R=0.3 alrededor del leptón (aislamiento de seguimiento)",
    },
    "lep_etcone20": {
        "English": "Type: Vector<Float> \nSum of track ET in a cone of R=0.2 around lepton (calorimeter isolation)",
        "Spanish": "Tipo: Vector<Float> \nSuma de ET de las pistas en un cono de R=0.2 alrededor del leptón (aislamiento de calorímetro)",
    },
    "lep_trackd0pvunbiased": {
        "English": "Type: Vector<Float> \nd0 of lepton track at point of closest approach",
        "Spanish": "Tipo: Vector<Float> \nd0 de la pista del leptón en el punto de mayor aproximación",
    },
    "lep_tracksigd0pvunbiased": {
        "English": "Type: Vector<Float> \nd0 significance of lepton track at point of closest approach",
        "Spanish": "Tipo: Vector<Float> \nSignificancia de d0 de la pista del leptón en el punto de mayor aproximación",
    },
    "met_et": {
        "English": "Type: Float \nTransverse energy of the missing momentum vector",
        "Spanish": "Tipo: Float \nEnergía transversal del vector de momento perdido",
    },
    "met_phi": {
        "English": "Type: Float \nAzimuthal angle of the missing momentum vector",
        "Spanish": "Tipo: Float \nÁngulo azimutal del vector de momento perdido",
    },
    "jet_n": {
        "English": "Type: Int \nNumber of pre-selected jets",
        "Spanish": "Tipo: Int \nNúmero de jets preseleccionados",
    },
    "jet_pt": {
        "English": "Type: Vector<Float> \nTransverse momentum of the jet",
        "Spanish": "Tipo: Vector<Float> \nMomentum transversal del jet",
    },
    "jet_eta": {
        "English": "Type: Vector<Float> \nPseudo-rapidity (η) of the jet",
        "Spanish": "Tipo: Vector<Float> \nPseudo-rapidez (η) del jet",
    },
    "jet_phi": {
        "English": "Type: Vector<Float> \nAzimuthal angle (φ) of the jet",
        "Spanish": "Tipo: Vector<Float> \nÁngulo azimutal (φ) del jet",
    },
    "jet_E": {
        "English": "Type: Vector<Float> \nEnergy of the jet",
        "Spanish": "Tipo: Vector<Float> \nEnergía del jet",
    },
    "jet_jvt": {
        "English": "Type: Vector<Float> \nJet vertex tagger discriminant",
        "Spanish": "Tipo: Vector<Float> \nDiscriminante del etiquetador de vértices del jet",
    },
    "jet_trueflav": {
        "English": "Type: Vector<Int> \nFlavour of the simulated jet",
        "Spanish": "Tipo: Vector<Int> \nSabor del jet simulado",
    },
    "jet_truthMatched": {
        "English": "Type: Vector<Bool> \nIndicates if the jet is matched to a simulated jet",
        "Spanish": "Tipo: Vector<Bool> \nIndica si el jet está emparejado con un jet simulado",
    },
    "jet_MV2c10": {
        "English": "Type: Vector<Float> \nOutput from the multivariate b-tagging algorithm",
        "Spanish": "Tipo: Vector<Float> \nSalida del algoritmo multivariante de b-tagging",
    },
    "photon_n": {
        "English": "Type: Int \nNumber of pre-selected photons",
        "Spanish": "Tipo: Int \nNúmero de fotones preseleccionados",
    },
    "photon_truthMatched": {
        "English": "Type: Vector<Bool> \nIndicates if the photon is matched to a simulated photon",
        "Spanish": "Tipo: Vector<Bool> \nIndica si el fotón está emparejado con un fotón simulado",
    },
    "photon_trigMatched": {
        "English": "Type: Vector<Bool> \nIndicates if the photon is the one triggering the event",
        "Spanish": "Tipo: Vector<Bool> \nIndica si el fotón es el que dispara el evento",
    },
    "photon_pt": {
        "English": "Type: Vector<Float> \nTransverse momentum of the photon",
        "Spanish": "Tipo: Vector<Float> \nMomentum transversal del fotón",
    },
    "photon_eta": {
        "English": "Type: Vector<Float> \nPseudo-rapidity of the photon",
        "Spanish": "Tipo: Vector<Float> \nPseudo-rapidez del fotón",
    },
    "photon_phi": {
        "English": "Type: Vector<Float> \nAzimuthal angle of the photon",
        "Spanish": "Tipo: Vector<Float> \nÁngulo azimutal del fotón",
    },
    "photon_E": {
        "English": "Type: Vector<Float> \nEnergy of the photon",
        "Spanish": "Tipo: Vector<Float> \nEnergía del fotón",
    },
    "photon_isTightID": {
        "English": "Type: Vector<Bool> \nIndicates if the photon satisfies tight ID reconstruction criteria",
        "Spanish": "Tipo: Vector<Bool> \nIndica si el fotón satisface los criterios estrictos de reconstrucción de ID",
    },
    "photon_ptcone30": {
        "English": "Type: Vector<Float> \nSum of track pT in a cone of R=0.3 around photon",
        "Spanish": "Tipo: Vector<Float> \nSuma de pT de las pistas en un cono de R=0.3 alrededor del fotón",
    },
    "photon_etcone20": {
        "English": "Type: Vector<Float> \nSum of track ET in a cone of R=0.2 around photon",
        "Spanish": "Tipo: Vector<Float> \nSuma de ET de las pistas en un cono de R=0.2 alrededor del fotón",
    },
    "photon_convType": {
        "English": "Type: Vector<Int> \nInformation about photon conversion",
        "Spanish": "Tipo: Vector<Int> \nInformación sobre la conversión del fotón",
    },
    "largeRjet_n": {
        "English": "Type: Int \nNumber of pre-selected large-R jets",
        "Spanish": "Tipo: Int \nNúmero de jets grandes-R preseleccionados",
    },
    "largeRjet_pt": {
        "English": "Type: Vector<Float> \nTransverse momentum of the large-R jet",
        "Spanish": "Tipo: Vector<Float> \nMomentum transversal del jet grande-R",
    },
    "largeRjet_eta": {
        "English": "Type: Vector<Float> \nPseudo-rapidity of the large-R jet",
        "Spanish": "Tipo: Vector<Float> \nPseudo-rapidez del jet grande-R",
    },
    "largeRjet_phi": {
        "English": "Type: Vector<Float> \nAzimuthal angle of the large-R jet",
        "Spanish": "Tipo: Vector<Float> \nÁngulo azimutal del jet grande-R",
    },
    "largeRjet_E": {
        "English": "Type: Vector<Float> \nEnergy of the large-R jet",
        "Spanish": "Tipo: Vector<Float> \nEnergía del jet grande-R",
    },
    "largeRjet_m": {
        "English": "Type: Vector<Float> \nInvariant mass of the large-R jet",
        "Spanish": "Tipo: Vector<Float> \nMasa invariante del jet grande-R",
    },
    "largeRjet_truthMatched": {
        "English": "Type: Vector<Int> \nIndicates if the large-R jet is matched to a simulated jet",
        "Spanish": "Tipo: Vector<Int> \nIndica si el jet grande-R está emparejado con un jet simulado",
    },
    "largeRjet_D2": {
        "English": "Type: Vector<Float> \nAlgorithm weight for W/Z-boson tagging",
        "Spanish": "Tipo: Vector<Float> \nPeso del algoritmo para el etiquetado de bosones W/Z",
    },
    "largeRjet_tau32": {
        "English": "Type: Vector<Float> \nAlgorithm weight for top-quark tagging",
        "Spanish": "Tipo: Vector<Float> \nPeso del algoritmo para el etiquetado de quarks top",
    },
    "tau_n": {
        "English": "Type: Int \nNumber of pre-selected hadronically decaying τ-leptons",
        "Spanish": "Tipo: Int \nNúmero de τ-leptones que decaen hadrónicamente preseleccionados",
    },
    "tau_pt": {
        "English": "Type: Vector<Float> \nTransverse momentum of the hadronically decaying τ-lepton",
        "Spanish": "Tipo: Vector<Float> \nMomentum transversal del τ-leptón que decae hadrónicamente",
    },
    "tau_eta": {
        "English": "Type: Vector<Float> \nPseudo-rapidity of the hadronically decaying τ-lepton",
        "Spanish": "Tipo: Vector<Float> \nPseudo-rapidez del τ-leptón que decae hadrónicamente",
    },
    "tau_phi": {
        "English": "Type: Vector<Float> \nAzimuthal angle of the hadronically decaying τ-lepton",
        "Spanish": "Tipo: Vector<Float> \nÁngulo azimutal del τ-leptón que decae hadrónicamente",
    },
    "tau_E": {
        "English": "Type: Vector<Float> \nEnergy of the hadronically decaying τ-lepton",
        "Spanish": "Tipo: Vector<Float> \nEnergía del τ-leptón que decae hadrónicamente",
    },
    "tau_charge": {
        "English": "Type: Vector<Int> \nCharge of the hadronically decaying τ-lepton",
        "Spanish": "Tipo: Vector<Int> \nCarga del τ-leptón que decae hadrónicamente",
    },
    "tau_isTightID": {
        "English": "Type: Vector<Bool> \nIndicates if τ-lepton satisfies tight ID reconstruction criteria",
        "Spanish": "Tipo: Vector<Bool> \nIndica si el τ-leptón satisface los criterios estrictos de reconstrucción de ID",
    },
    "tau_truthMatched": {
        "English": "Type: Vector<Bool> \nIndicates if the τ-lepton is matched to a simulated τ-lepton",
        "Spanish": "Tipo: Vector<Bool> \nIndica si el τ-leptón está emparejado con un τ-leptón simulado",
    },
    "tau_trigMatched": {
        "English": "Type: Vector<Bool> \nIndicates if the τ-lepton triggered the event",
        "Spanish": "Tipo: Vector<Bool> \nIndica si el τ-leptón disparó el evento",
    },
    "tau_nTracks": {
        "English": "Type: Vector<Int> \nNumber of tracks in the τ-lepton decay",
        "Spanish": "Tipo: Vector<Int> \nNúmero de pistas en el decaimiento del τ-leptón",
    },
    "tau_BDTid": {
        "English": "Type: Vector<Float> \nOutput of multivariate τ-lepton discrimination algorithm",
        "Spanish": "Tipo: Vector<Float> \nSalida del algoritmo multivariante de discriminación de τ-leptones",
    },
    "ditau_m": {
        "English": "Type: Float \nDi-τ invariant mass using the missing-mass calculator",
        "Spanish": "Tipo: Float \nMasa invariante di-τ usando el calculador de masa perdida",
    },
    "lep_pt_syst": {
        "English": "Type: Vector<Float> \nSystematic uncertainty for lepton momentum scale and resolution",
        "Spanish": "Tipo: Vector<Float> \nIncertidumbre sistemática para la escala y resolución del momentum de los leptones",
    },
    "met_et_syst": {
        "English": "Type: Float \nSystematic uncertainty for MET scale and resolution",
        "Spanish": "Tipo: Float \nIncertidumbre sistemática para la escala y resolución de MET",
    },
    "jet_pt_syst": {
        "English": "Type: Vector<Float> \nSystematic uncertainty for jet energy scale",
        "Spanish": "Tipo: Vector<Float> \nIncertidumbre sistemática para la escala de energía del jet",
    },
    "photon_pt_syst": {
        "English": "Type: Vector<Float> \nSystematic uncertainty for photon energy scale and resolution",
        "Spanish": "Tipo: Vector<Float> \nIncertidumbre sistemática para la escala y resolución de energía del fotón",
    },
    "largeRjet_pt_syst": {
        "English": "Type: Vector<Float> \nSystematic uncertainty for large-R jet energy resolution",
        "Spanish": "Tipo: Vector<Float> \nIncertidumbre sistemática para la resolución de energía de jets grandes-R",
    },
    "tau_pt_syst": {
        "English": "Type: Vector<Float> \nSystematic uncertainty for τ-lepton reconstruction and energy scale",
        "Spanish": "Tipo: Vector<Float> \nIncertidumbre sistemática para la reconstrucción y escala de energía del τ-leptón",
    },
}



class RootFileBrowser:
    """
    A class for browsing ROOT files, displaying their structure, and plotting histograms.

    Attributes:
        descriptions (dict): Dictionary of descriptions for various ROOT branches.
    """

    def __init__(self):
        """
        Initialize the RootFileBrowser with optional descriptions.

        Parameters:
            descriptions (dict, optional): Descriptions for ROOT branches. Defaults to an empty dictionary.
        """

    def create_tree_items(self, directory, language="en"):
        """
        Convert the ROOT file structure into TreeItems for display, with language-based descriptions.
    
        Parameters:
            directory (uproot.reading.ReadOnlyDirectory): The ROOT file directory object.
            language (str): The selected language ("en" or "es").
    
        Returns:
            List[sac.TreeItem]: A list of TreeItems for display in the tree component.
        """
        items = []
        for key, obj in directory.items():
            if isinstance(obj, uproot.behaviors.TTree.TTree):
                branch_items = []
                for branch in obj.keys():
                    description = DESCRIPTIONS.get(branch, {}).get(language, f"Type: {obj[branch].typename} \nNo description available")
                    branch_items.append(
                        sac.TreeItem(
                            label=f"🍁 {branch}",
                            description=description
                        )
                    )
                items.append(sac.TreeItem(label=f"🌳 {key}", children=branch_items))
            elif isinstance(obj, uproot.reading.ReadOnlyDirectory):
                child_items = self.create_tree_items(directory[key], language)
                items.append(sac.TreeItem(label=f"🌳 {key}", children=child_items))
        return items


    def display_tree_structure(self, directory, language):
        """
        Render the ROOT file tree structure in Streamlit using the Tree component.
    
        Parameters:
            directory (uproot.reading.ReadOnlyDirectory): The ROOT file directory object.
            language (str): The selected language ("en" or "es").
    
        Returns:
            list: The names of the selected branches.
        """
        tree_label = "Tree Structure" if language == "en" else "Estructura del árbol"
        tree_items = self.create_tree_items(directory, language)
        selected = sac.tree(items=tree_items, label=tree_label, open_all=True, checkbox=True, size="md")
        return selected


    def plot_branch_histogram(self, tree, branch):
        """
        Plot a histogram for the data in the specified branch of the ROOT file.

        Parameters:
            tree (uproot.behaviors.TTree.TTree): The ROOT TTree object.
            branch (str): The branch name to plot.
        """
        try:
            data = tree[branch].array(library="np")
            fig, ax = plt.subplots()
            ax.hist(data, bins=30, alpha=0.7, color="skyblue")
            ax.set_title(f"Histogram of {branch}")
            ax.set_xlabel("Value")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Could not plot histogram for {branch}")

    def browse_root_file(self, language="English"):
        """
        Streamlit interface for browsing a ROOT file, selecting branches, and viewing histograms.

        Parameters:
            language (str): Language for the interface. Options are "en" (English) or "es" (Spanish).
        """
        # Translations
        select_file_text = "Select a ROOT file" if language == "English" else "Selecciona un archivo ROOT"
        open_tree_text = "Open to see Tree Structure" if language == "English" else "Haz click para ver la estructura del archivo"

        # File upload option
        root_files = [
            'https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_361106.Zee.1largeRjet1lep.root',
            'https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/Data/data_B.1largeRjet1lep.root',
        ]

        file_labels = [url.split('/')[-2] + '/' + url.split('/')[-1] for url in root_files]
        file_map = dict(zip(file_labels, root_files))
        selected_label = st.selectbox(select_file_text, file_labels)
        selected_file = file_map[selected_label]

        if selected_file:
            try:
                directory = uproot.open(selected_file)

                with st.expander(open_tree_text, expanded=False):
                    selected = self.display_tree_structure(directory, language)

                if selected:
                    selected_branches = [s.split()[-1] for s in selected]
                    for branch in selected_branches:
                        for key, obj in directory.items():
                            if isinstance(obj, uproot.behaviors.TTree.TTree) and branch in obj.keys():
                                self.plot_branch_histogram(obj, branch)

            except Exception as e:
                st.error(f"Error loading file: {e}")
