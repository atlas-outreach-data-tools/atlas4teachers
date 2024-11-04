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

![Image 1: Structure of a root file.](images/root_struct.png)

We’ll use uproot to load the data file:

```python
file = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_361106.Zee.1largeRjet1lep.root")
tree = file["mini"]

print("✅ File opened")
```

> [!NOTE]  
If you are curious about where the files above come from, check out the instructions for finding the ATLAS Open Data [here](https://opendata.atlas.cern/docs/data)
> [!END]

To see what’s inside, use `.keys()` and `.classnames()`:

```python
print(file.keys())
```
```python
print(file.classnames())
```

This means *mini* is a TTree object. It should contain all the data we need. To load the mini tree directly:

```python
my_tree = file["mini"]
```

Or specify mini in `uproot.open()`:

```python
my_tree = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_361106.Zee.1largeRjet1lep.root:mini")
```

The `.show()` function allows us to see the full contents of your TTree in setups like a jupyter notebook and the terminal. You get something like this:

```
name                 | typename                 | interpretation                
---------------------+--------------------------+-------------------------------
runNumber            | int32_t                  | AsDtype('>i4')
eventNumber          | int32_t                  | AsDtype('>i4')
channelNumber        | int32_t                  | AsDtype('>i4')
mcWeight             | float                    | AsDtype('>f4')
scaleFactor_PILEUP   | float                    | AsDtype('>f4')
scaleFactor_ELE      | float                    | AsDtype('>f4')
...
```

We see the names of all the different quantities stored. Rather than use the word name (written at the top of the table), we use the word branch. Let's look at an individual branch in this TTree to see its form. We specify what branch we want to look at ("lep_eta") and the type of array we want to output ("np" which is short for numpy array)

```python
lep_eta = my_tree["lep_eta"].array(library="np")
print(lep_eta)
```

In effect, this is a 2D array containing 2 elements: an array of values, and the data type of the array.  It is this method of storing values that allows an array to be 'jagged' - that is, having each row be a different length - without becoming an issue for array manipulation.

We can see how many events are stored in the tree by looking at the length of the array using the `len` function

```python
print(len(lep_eta))
```

### ✍🏻 Your turn

> [!TIP] 
**1)** Replace the hash signs (###) in the cell below to open the _*.root_ data file `"https://atlas-opendata.web.cern.ch/release/2016/MC/mc_105987.WZ.root"`
> [!END]

<details>
    <summary>💡 Click here for hint 1</summary>
    
    What function did we use above to open a .root file?
</details>

```python
my_file = ###

```

<details>
    <summary>💬 Answer</summary>

    my_file = uproot.open("https://atlas-opendata.web.cern.ch/release/2016/MC/mc_105987.WZ.root")
</details>

> [!TIP]  
**2)** Load the tree named "mini" stored in the _.*root_ data file. Print the number of events in this tree.
> [!END]

<details>
    <summary>💡 Click here for hint 1</summary>
    All data is stored in the TTree 'mini'.
</details>


<details>
    <summary>💡 Click here for hint 2</summary>
    Pick a branch (name) and output it as an array.
</details>


<details>
    <summary>💡 Click here for hint 3</summary>
    Look at the length of the array.
</details>

```python
my_tree = my_file[###]
eventNumber = my_tree[###].array(###)
print(###)
```

<details>
    <summary>💬 Answer</summary>
        
    my_tree = my_file["mini"]
    eventNumber = my_tree["eventNumber"].array(library="np")
    print(len(eventNumber))
</details>

> [!TIP]
**3)** We will also need to create variables for the maximum and the minimum number of jets in a single event in this dataset for later.
> [!END]

<details>
    <summary>💡 Click here for hint 1</summary>
    The object you need is called "jet_n". Get an array which is the jet_n for each event
</details>


<details>
    <summary>💡 Click here for hint 2</summary>
    Numpy has two functions, .min() and .max(), that return the minimum and maximum values of an array.
</details>


<details>
    <summary>💡 Click here for hint 3</summary>
    Remember the first event is [0]!
</details>

```python
import numpy as np

jet_n = my_tree[###].array(###)
minimum = np.min(###)
maximum = np.max(###)
print("Minimum number of jets:", ###)
print("Maximum number of jets;", ###)
      
#Peek inside the first event using list indexing
jet_n_Event1 = jet_n[#] 
print("Number of jets in Event 1:", ###)
```

<details>
    <summary>💬 Answer</summary>
        
    jet_n = my_tree["jet_n"].array(library="np")
    minimum = np.min(jet_n)
    maximum = np.max(jet_n)  
    print("Minimum number of jets:", minimum)
    print("Maximum number of jets;", maximum)
    
    jet_n_Event1 = jet_n[0]
    print("Number of jets in Event 1:", jet_n_Event1)
</details>


---

## Step 2: Getting ready to display histograms
Before we can display any histograms, we must import a few modules:
- `hist` is a library that handles the generation and customization of histograms
- `Hist` is a module from `hist` that allows for the generation of a basic histogram

```python
import hist
from hist import Hist
```

To create a histogram, we use `Hist` and the `hist.axis.Regular()` function, which takes arguments `(bins, lower_limit, upper_limit, label)`. For example, if we want to count leptons (from 0 to 4), we set up 5 bins, a lower limit of 0, and an upper limit of 4:

```python
hist1 = Hist(hist.axis.Regular(5, -0.5, 4.5, label = "Number of leptons"))
```

The `-0.5` offset centers bins on 0, 1, 2, 3, and 4.

> [!IMPORTANT]  
We don't expect any output to be printed from this step - all we're doing here is telling python the details of the histogram we're planning to fill.
> [!END]

### ✍🏻 Your turn

> [!TIP] 
**4)** Create a template histogram called "Number of jets" to display your plot.
> [!END] 

<details>
    <summary>💡 Click here for hint 1</summary>
    Use the minimum (-0.5) and maximum number of jets (9.5) for your axis limits.
</details>


<details>
    <summary>💡 Click here for hint 2</summary>
    Use the maximum number of jets for your bin numbers.
</details>

```python
my_hist = Hist(hist.axis.Regular(###, ###, ###, label = ###))
```

<details>
    <summary>💬 Answer</summary>
        
    my_hist = Hist(hist.axis.Regular(5, -0.5, 9.5, label = "Number of jets"))
</details>

---

## Step 3: Filling histograms
To fill the histogram, start by extracting the number of leptons from the TTree as a numpy array:

```python
lep_n = my_tree["lep_n"].array(library="np")
```

Then, use `.fill()` to populate the histogram:

```python
hist1.fill(lep_n)
```

To display the histogram, plot it using `.plot()` from `hist` and `plt.show()` from `matplotlib`:

```python
hist1.plot()
plt.show()
```

> [!NOTE]  
Later, we’ll refine the histogram by applying “cuts,” including only events that meet specific criteria.
> [!END]

### ✍🏻 Your turn

> [!TIP]  
**5)** Fill your histogram with the number of jets in each event.
> [!END]

<details>
    <summary>💡 Click here for hint 1</summary>
        Remember: we've already made a template histogram.
</details>


<details>
    <summary>💡 Click here for hint 2</summary>
        The data you're after is "jet_n".
</details>

```python
my_hist.fill(###)
my_hist.###
plt.###
  
```

<details>
    <summary>💬 Answer</summary>
        
    my_hist.fill(jet_n)
    my_hist.plot()
    plt.show()
</details>

---

## Step 4: Drawing histograms

First, let’s set up a basic histogram with a title:

```python
hist2 = Hist(hist.axis.Regular(5, -0.5, 4.5, label="Number of leptons"))
hist2.fill(lep_n)
hist2.plot()
plt.title("Number of leptons in a 13 TeV dataset")
plt.show()
```

To compare lepton counts across datasets, let’s load two datasets and plot them on the same axis:

```python
# Load additional datasets
tr1 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363491.lllv.1largeRjet1lep.root:mini")
lep_n1 = tr1["lep_n"].array(library="np")

tr2 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363492.llvv.1largeRjet1lep.root:mini")
lep_n2 = tr2["lep_n"].array(library="np")
```
Now we can create and fill two histograms:

```python
# Create and fill histograms
hist1 = Hist(hist.axis.Regular(5, -0.5, 4.5, label="Number of leptons"))
hist1.fill(lep_n1)

hist2 = Hist(hist.axis.Regular(5, -0.5, 4.5, label="Number of leptons"))
hist2.fill(lep_n2)
```

Here, the events in question produced leptons and their associated neutrinos.  We're curious as to how many leptons were produced in each event and how these numbers compare, so overlapping our histograms would be preferable. This is a straightforward process. You can fill two separate histograms, and plot them one after the other. Everytime you run `plot()`, it will draw the histogram on top of what is already there. Of course run `plt.show()` to display what you have drawn.

Overlay both histograms and display them together:

```python
# Plot both histograms
hist1.plot()
hist2.plot()
plt.title("Lepton counts per event for multiple datasets")
plt.legend(["Dataset 1", "Dataset 2"])
plt.show()
```

For a stacked version, combine and plot the histograms directly:

```python
histo_sum = hist1 + hist2
histo_sum.plot(histtype="fill")
plt.title("Stacked Lepton Counts per Event")
plt.show()
```

We can also use the `.stack()` function from `hist`, to overlay or stack histograms, though we'll need to prepare a little first. 

Now we need a 'category axis' or `cax`, which operates in a similar manner to a dictionary.  Its $1^{st}$ argument is a list of histogram labels and its $2^{nd}$ argument is a label for the collective axis.  In effect, each histogram label is like a key, linking each histogram to its name, color and position.

```python
# Create a categorized histogram for stacking
ax = hist.axis.Regular(5, -0.5, 4.5, flow=False, name="Number of leptons")
cax = hist.axis.StrCategory(["Dataset 1", "Dataset 2"], name="dataset")

stacked_hist = Hist(ax, cax)
stacked_hist.fill(lep_n1, dataset="Dataset 1")
stacked_hist.fill(lep_n2, dataset="Dataset 2")

stacked_hist.stack("dataset").plot(histtype="fill")
plt.title("Stacked Lepton Counts per Event")
plt.legend()
plt.show()

```

This looks the same as the output from our previous overlay method, as it should! This plot is slightly more discernible. The added legend also helps.

### ✍🏻 Your turn

> [!TIP]
**6)** Display multiple histograms for lepton number on the same plot.  You'll need the below files:
- 4 leptons - https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363490.llll.4lep.root
- 3 leptons - https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363491.lllv.1largeRjet1lep.root
> [!END]

<details>
    <summary>💡 Click here for hint 1</summary>
        You'll need to access the TTree data for lepton number 2 separate times, 1 for each dataset.
</details>


<details>
    <summary>💡 Click here for hint 2</summary>
        Think about the bin numbers and boundaries for your axis, and remember that we have 2 datasets when generating the category axis.
</details>


<details>
    <summary>💡 Click here for hint 3</summary>
        You'll need to fill your template histogram 2 times.
</details>

```python
### Repeat for each root file
tr1 = uproot.open(###)
lep_n1 = tr1[###].array(###)

### Repeat 4 times
ax = hist.axis.Regular(###)
cax = hist.axis.StrCategory([###], name = ###)
full_hist = Hist(###, ###)

full_hist.fill(###, c = ###)
### Repeat 4 times

s = full_hist.stack(###)
s.###
plt.title(###)
plt.###
plt.###
```

<details>
    <summary>💬 Answer</summary>

    # Load the datasets with 4 leptons and 3 leptons
    tr1 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363490.llll.4lep.root:mini")
    lep_n1 = tr1["lep_n"].array(library="np")

    tr2 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363491.lllv.1largeRjet1lep.root:mini")
    lep_n2 = tr2["lep_n"].array(library="np")

    # Define the histogram axes
    ax = hist.axis.Regular(6, -0.5, 5.5, name="Number of leptons")
    cax = hist.axis.StrCategory(["4 leptons", "3 leptons + neutrino"], name="dataset")

    # Create and fill the categorized histogram
    full_hist = Hist(ax, cax)
    full_hist.fill(lep_n1, dataset="4 leptons")
    full_hist.fill(lep_n2, dataset="3 leptons + neutrino")

    # Plot the stacked histogram
    s = full_hist.stack("dataset")
    s.plot(histtype="fill")
    plt.title("Lepton Counts per Event for Two Datasets")
    plt.legend()
    plt.show()
</details>

---

## Step 5: Normalising histograms
Often, we are more interested in the **proportions** of our histogram than the absolute number of events it contains (which can change depending on what dataset you use).  Our final step will be to rescale the y-axis of our histogram to that the histogram's total is equal to 1. This is called **normalisation**.

First, extract bin values (heights) as an array and calculate the sum. We use the `.sum()` function on our array of bin values to sum the values it contains, then create a new array containing each of the original bin values divided by the sum.

```python
arr = hist1.values()
arr_normalized = arr / arr.sum()
```

Create a new histogram and set its bin values to the normalized values:

```python
hist_normalized = Hist(hist.axis.Regular(5, -0.5, 4.5, flow=False, label="Number of leptons"))
hist_normalized[...] = arr_normalized  # Assign normalized bin values
```

Let's see what we get!

```python
hist_normalized.plot(histtype="fill")
plt.title("Normalized Lepton Count")
plt.show()
```

Now let's show that this is normalised - we've already used the function required to do this!

```python
print(hist_normalized.sum())
```

### ✍🏻 Your turn
> [!TIP]
**6)** Normalise your histogram and redraw it.
> [!END]

<details>
    <summary>💡 Click here for hint 1</summary>
        Use `.values()` to access the height of each bar in the histogram.
</details>


<details>
    <summary>💡 Click here for hint 2</summary>
        Use `.sum` to find the sum of these heights - you'll need to divide each bar's height by the sum.
</details>


<details>
    <summary>💡 Click here for hint 3</summary>
        Redraw your histogram and assign new values to each bin.
</details>

```python
heights = my_hist.###
norm_heights = ###/heights.###
new_hist = Hist(hist.axis.Regular(###, ###, ###, label = ###))
new_hist[###] = norm_heights[###]
new_hist.###
plt.###
```

<details>
    <summary>💬 Answer</summary>
        
    # Get the bin values from the original histogram and normalize them
    heights = my_hist.values()
    norm_heights = heights / heights.sum()

    # Create a new histogram with the normalized values
    new_hist = Hist(hist.axis.Regular(5, -0.5, 4.5, label="Number of jets"))
    new_hist[...] = norm_heights  # Assign normalized values to bins

    # Plot the normalized histogram
    new_hist.plot(histtype="fill")
    plt.title("Normalized Jet Count per Event")
    plt.show()
</details>

---

**Congratulations!** You've worked with actual ATLAS data like a real particle physicist!

If you want to continue learning how to use Python to analyse the public data from ATLAS, you can check out the [notebooks in the ATLAS Open Data website](https://opendata.atlas.cern/docs/category/analysis-notebooks).

