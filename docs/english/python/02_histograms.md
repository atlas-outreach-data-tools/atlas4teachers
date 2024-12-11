# Introduction to Histogramming
In particle physics, analyzing the massive amount of data requires computer code rather than manual inspection. This guide will cover basic histogramming techniques to help you visualize data from high-energy physics (HEP) analyses, specifically the number of leptons per event in 13 TeV Z boson data.

This resource will walk you through some basic computing techniques commonly used in high energy physics (HEP) analyses. You will learn how to:

1. Interact with ATLAS data files
2. Create, fill, draw, and normalize histograms
    
## Step 0: Set Up
The software we will use to analyse our ATLAS data is called *uproot* and *hist*. Using `uproot`, we are able to process large datasets, do statistical analyses, and visualise our data using *hist*. The data is stored in a format called .root

```python
#Import the libraries
import uproot
import matplotlib.pyplot as plt
import numpy as np

print('✅ Libraries imported')
```

## Step 1: Loading Data

Physics data is commonly stored in `[something].root` files. These files use a TTree structure:
- The TTree organizes measurements in branches, each representing a variable (e.g., energy, momentum).
- Each branch stores the measured variable for each event in the dataset.