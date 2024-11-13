from os import write
import streamlit as st
import uproot
import streamlit_antd_components as sac

def make_tree(root_file):
    """
    Creates a tree structure of the ROOT file. Works when the ROOT file has multiple keys, objects, or branches,
    but skips over empty or missing subkeys and handles ROOT objects (like histograms) properly.
    """
    
    # Check if a ROOT file has been uploaded
    if root_file is None:
        return "Please upload a ROOT file."
    
    # Open the ROOT file
    file = uproot.open(root_file)
    
    # Get the keys of the ROOT file
    keys = file.keys()
    
    # Create a tree structure
    tree = {}
    for key in keys:
        tree[key] = {}
        
        # Get the current item (could be a histogram, tree, or a container)
        item = file[key]
        
        # Check if the item is a dictionary-like object (which would have subkeys)
        if hasattr(item, 'keys'):
            # If it's a dictionary-like object, we can check for subkeys
            subkeys = item.keys()
            if subkeys:
                for subkey in subkeys:
                    tree[key][subkey] = {}
                    
                    # Check if the subkey has further subkeys (recursive)
                    subsubkeys = item[subkey].keys() if hasattr(item[subkey], 'keys') else []
                    if subsubkeys:
                        for subsubkey in subsubkeys:
                            tree[key][subkey][subsubkey] = {}
                            
                            # Check for further subsubsubkeys (recursive)
                            subsubsubkeys = item[subkey][subsubkey].keys() if hasattr(item[subkey][subsubkey], 'keys') else []
                            if subsubsubkeys:
                                for subsubsubkey in subsubsubkeys:
                                    tree[key][subkey][subsubkey][subsubsubkey] = {}
        else:
            # If the item is not a dictionary-like object, it's likely a ROOT object (e.g., a histogram)
            tree[key]['is_root_object'] = True  # Add metadata indicating it's a ROOT object
            
    return tree

def root_browser():
    """
    Draws the Streamlit interface for uploading a ROOT file and displaying its tree structure.
    """
    # Upload the ROOT file
    root_file = st.file_uploader("Upload a ROOT file", type=["root"])
    
    # Display the tree structure of the ROOT file
    tree = make_tree(root_file)
    st.write(tree)
    
    print(tree)
