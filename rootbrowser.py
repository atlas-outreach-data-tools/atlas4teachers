import streamlit as st
import uproot
import streamlit_antd_components as sac
import matplotlib.pyplot as plt
import pandas as pd

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
    
    if not tree:
        return
        
    # Create a list of TreeItems from the tree structure
    tree_items = create_tree_items(tree)
    # Display the tree structure
    print(tree_items)
    return sac.tree(items=tree_items, label='Tree Structure', open_all=True, checkbox=True)

def print_types(directory, filter):
    
    if not filter:
        return
    
    for key, obj in directory.items():
        if isinstance(obj, uproot.behaviors.TTree.TTree):
            branches = obj.keys()
            for branch in branches:
                if branch == filter:
                    ## print the types
                    st.write(obj[branch].typename)
                    plot_branch_histogram(obj, branch)
                    
        elif isinstance(obj, uproot.reading.ReadOnlyDirectory):
            print_types(directory, filter)
    
    return

def plot_branch_histogram(tree, branch):

    try:
        data = tree[branch].array(library="np")
        fig, ax = plt.subplots()
        ax.hist(data, bins=30, alpha=0.7, color="skyblue")
        ax.set_title(f"Histogram of {branch}")
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    except:
        st.write("plot histogram not supported")
    
    
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
    
    with st.expander(f"🌳 Tree", expanded=False):
        tree = make_tree(root_file)
        selected = display_tree(tree)
        if selected is not None:
            for i in selected:
                print_types(uproot.open(root_file), i[2:])
                
                