import streamlit as st
import uproot
import streamlit_antd_components as sac



def make_tree(directory, path=""):
    # add emoji to tree branches and leaves
    file = uproot.open(directory)

    def make(file_now):
        tree = {}
        for key, obj in file_now.items():
            if isinstance(obj, uproot.behaviors.TTree.TTree):
                tree[key] = {"branches": list(obj.keys())}
            elif isinstance(obj, uproot.reading.ReadOnlyDirectory):
                tree[key] = make(file_now[key])
        return tree
    
    st.write(make(file))
    
    return make(file)

def display_tree(tree):
    # TODO: display tree in a more user-friendly way
    bruh = 1
    
def root_browser():
    """
    Streamlit interface to upload a ROOT file and display its tree structure. use drop down box to select a file with also pre loaded ones
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
            #display_tree(tree)
        else:
            st.write("No ROOT file selected")
    