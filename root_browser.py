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
                        label=f"{branch}",
                        description=self.descriptions.get(branch, f"Type: {obj[branch].typename} \nNo description available")
                    )
                    for branch in obj.keys()
                ]
                items.append(sac.TreeItem(label=f"📂 {key}", children=branch_items))
            elif isinstance(obj, uproot.reading.ReadOnlyDirectory):
                child_items = self.create_tree_items(directory[key])
                items.append(sac.TreeItem(label=f"📁 {key}", children=child_items))
        return items

    def display_tree_structure(self, directory):
        """
        Render the ROOT file tree structure in Streamlit using the Tree component.

        Parameters:
            directory (uproot.reading.ReadOnlyDirectory): The ROOT file directory object.

        Returns:
            list: The names of the selected branches.
        """
        tree_items = self.create_tree_items(directory)
        selected = sac.tree(items=tree_items, label="Tree Structure", open_all=True, checkbox=True, size="xs")
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

    def browse_root_file(self):
        """
        Streamlit interface for browsing a ROOT file, selecting branches, and viewing histograms.
        """
        st.title("ROOT File Browser")

        # File upload option
        uploaded_file = st.file_uploader("Upload a ROOT file", type=["root"])
        root_files = [
            'https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_361106.Zee.1largeRjet1lep.root',
            'https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/Data/data_B.1largeRjet1lep.root',
            'https://atlas-opendata.web.cern.ch/Legacy8TeV/MC/mc_147770.Zee.root',
        ]
        if uploaded_file:
            root_files.append(uploaded_file)

        selected_file = st.selectbox("Select a ROOT file", root_files)

        if selected_file:
            try:
                directory = uproot.open(selected_file)

                with st.expander("🌳 Tree Structure", expanded=True):
                    selected = self.display_tree_structure(directory)

                if selected:
                    selected_branches = [s.split()[-1] for s in selected]  # Extract branch names from selection
                    for branch in selected_branches:
                        for key, obj in directory.items():
                            if isinstance(obj, uproot.behaviors.TTree.TTree) and branch in obj.keys():
                                self.plot_branch_histogram(obj, branch)

            except Exception as e:
                st.error(f"Error loading file: {e}")
