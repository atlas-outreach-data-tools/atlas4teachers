import streamlit as st
import uproot
import streamlit_antd_components as sac
import matplotlib.pyplot as plt

class RootFileBrowser:
    """
    A class for browsing ROOT files, displaying their structure, and plotting histograms.

    Attributes:
        descriptions (dict): Dictionary of descriptions for various ROOT branches.
    """

    def __init__(self, descriptions=None):
        """
        Initialize the RootFileBrowser with optional descriptions.

        Parameters:
            descriptions (dict, optional): Descriptions for ROOT branches. Defaults to an empty dictionary.
        """
        self.descriptions = descriptions or {}

    def create_tree_items(self, directory):
        """
        Convert the ROOT file structure into TreeItems for display.

        Parameters:
            directory (uproot.reading.ReadOnlyDirectory): The ROOT file directory object.

        Returns:
            List[sac.TreeItem]: A list of TreeItems for display in the tree component.
        """
        items = []
        for key, obj in directory.items():
            if isinstance(obj, uproot.behaviors.TTree.TTree):
                branch_items = [
                    sac.TreeItem(
                        label=f"🍁 {branch}",
                        description=self.descriptions.get(branch, f"Type: {obj[branch].typename} \nNo description available")
                    )
                    for branch in obj.keys()
                ]
                items.append(sac.TreeItem(label=f"🌳 {key}", children=branch_items))
            elif isinstance(obj, uproot.reading.ReadOnlyDirectory):
                child_items = self.create_tree_items(directory[key])
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
        tree_label = "Tree Structure" if language == "English" else "Estructura del árbol"
        tree_items = self.create_tree_items(directory)
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
