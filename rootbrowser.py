import streamlit as st
import uproot
import streamlit_antd_components as sac

def build_tree(item):
    """
    Builds a flat tree structure with the first-level subkeys treated as leaves.
    If subkeys have further sub-subkeys, they are also included.
    """
    tree = {}

    # If the item has subkeys (it's a directory-like object)
    if hasattr(item, 'keys'):
        for key in item.keys():
            # Check if the subkey itself has further subkeys (sub-subkeys)
            subitem = item[key]
            if hasattr(subitem, 'keys'):  # Subkey has further subkeys
                tree[key] = build_tree(subitem)  # Add sub-subkeys recursively
            else:
                # If it's a ROOT object (like a histogram or TTree), mark it as a leaf
                tree[key] = {'is_root_object': True}
    else:
        # If it's a ROOT object (like a histogram or TTree), mark it as a leaf
        tree['is_root_object'] = True

    return tree

def make_tree(root_file):
    """
    Opens the ROOT file and builds a flat tree structure based on its contents.
    """
    if root_file is None:
        return "Please upload a ROOT file."

    try:
        # Open the ROOT file
        file = uproot.open(root_file)
    except Exception as e:
        return f"Error opening ROOT file: {e}"

    # Get the keys (directories or objects) in the ROOT file
    keys = file.keys()
    
    # Build the tree structure for each key
    tree = {}
    for key in keys:
        item = file[key]
        # Build a flat tree structure with no deeper recursion, checking for sub-subkeys
        tree[key] = build_tree(item)

    return tree

def display_tree(tree):
    """
    Displays the tree structure of the ROOT file using streamlit_antd_components.
    Make the branches and trees expandable/collapsible.
    """
    # Display the tree structure
    
    def display_tree_recursive(tree):
        items = []
        for key, value in tree.items():
            if 'is_root_object' not in value:
                # If this is a directory (subkey with further subkeys), use file emoji 📁
                items.append(sac.TreeItem(f"📁 {key}", children=display_tree_recursive(value)))  # Folder emoji
            else:
                # If this is a ROOT object (leaf), use leaf emoji 🌿
                items.append(sac.TreeItem(f"🌿 {key}"))  # Leaf emoji
        return items
    
    tree_items = display_tree_recursive(tree)
    
    st.write("Tree structure of the ROOT file:")
    sac.tree(items=tree_items, label='ROOT file', open_all=True)

def root_browser():
    """
    Streamlit interface to upload a ROOT file and display its tree structure.
    """
    # Upload the ROOT file
    root_file = st.file_uploader("Upload a ROOT file", type=["root"])
    
    if root_file:
        # Display the tree structure of the ROOT file
        tree = make_tree(root_file)
        
        display_tree(tree)
        
    else:
        st.write("No file uploaded yet.")