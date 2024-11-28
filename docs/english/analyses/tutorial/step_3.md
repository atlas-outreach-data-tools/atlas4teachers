The filtered dataset now contains {filtered_data_size} events. The table below shows only the events matching this selection, and the one made in step 1.

> [!dataframe]
filtered_data
> [!end]

## Step 3: Filter Events by Energy
Energy is a key property in particle physics because it provides insights into the nature of interactions and decays in the events being analyzed. Higher-energy events can produce heavier particles, such as the Higgs boson, and the energy of decay products helps identify the original particles and their behavior. By focusing on specific energy ranges, we can filter out background noise and isolate meaningful events. Each event in our dataset has an associated **energy** value measured in giga-electronvolts (GeV).

In this step, you can filter the dataset by specifying an **energy range**. This allows you to focus on events within a particular  range of interest.

Use the slider below to select the minimum and maximum energy values (in GeV). For example: A range of **20 to 150 GeV** retains events where the energy falls between these limits.

As you adjust the slider, the dataset will dynamically update to reflect your chosen energy range. You can verify that the cut was applied by looking at the `Energy` column and making sure none of the values are below the minimum or above of the maximum of the selected range.