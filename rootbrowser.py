import streamlit as st
import uproot
import streamlit_antd_components as sac

def make_tree(directory, path=""):
    """
    Create a dictionary with the tree structure of a ROOT file.
    """
    
    file = uproot.open(directory) # Open the ROOT file

    def make(file_now): # Recursive function to create the tree structure
        tree = {}
        for key, obj in file_now.items():
            if isinstance(obj, uproot.behaviors.TTree.TTree):
                tree[key] = {"branches": list(obj.keys())} # Add the branches of the tree
                
            elif isinstance(obj, uproot.reading.ReadOnlyDirectory):
                tree[key] = make(file_now[key]) # Recursively add the subdirectories
                
        return tree
        
    return make(file)

def create_tree_items(data):
    """
    Create a list of TreeItems from a dictionary with nested dictionaries and lists.
    """
    
    items = []
    for key, value in data.items():
        if isinstance(value, dict):
            # Create a TreeItem for folders (dictionaries), recursively adding children
            child_items = create_tree_items(value)
            items.append(sac.TreeItem(label=f"📁 {key}", children=child_items))
        elif isinstance(value, list):
            # Create TreeItems for lists, each item in the list becomes a child leaf
            list_items = [sac.TreeItem(label=f"🍃 {item}") for item in value]
            items.append(sac.TreeItem(label=f"📂 {key}", children=list_items))
        else:
            # Leaf node
            items.append(sac.TreeItem(label=f"🍂 {key}: {value}"))
    return items


def display_tree(tree):
    # Use sac.tree to display the tree structure
    tree_items = create_tree_items(tree)
    sac.tree(items=tree_items, label='Tree Structure', open_all=True, checkbox=True)


def root_browser():
    """
    Streamlit interface to upload a ROOT file and display its tree structure. Use drop down box to select a file with also pre-loaded ones.
    """
    # Upload the ROOT file
    uploaded = st.file_uploader("Upload a ROOT file", type=["root"])
    
    list = ['https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_361106.Zee.1largeRjet1lep.root', 
            'https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/Data/data_B.1largeRjet1lep.root',
            'https://atlas-opendata.web.cern.ch/Legacy8TeV/MC/mc_147770.Zee.root', uploaded]
    
    root_file = st.selectbox("Select a ROOT file", list)
    button = st.button("Display tree")
    
    if button:
        if root_file:
            tree = make_tree(root_file)
            display_tree(tree)
        else:
            st.write("No ROOT file selected")
