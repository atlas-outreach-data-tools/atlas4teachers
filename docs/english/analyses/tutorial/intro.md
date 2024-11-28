# Tutorial: Understanding Cuts in Data Analysis
Analyzing data is the foundation of physics research. In experiments like those conducted at the ATLAS detector at CERN, we analyze vast amounts of data to search for evidence of particles. This process involves isolating meaningful collisions or events—an essential step for making scientific discoveries. 

This tutorial introduces the concept of **cuts** in data analysis. You'll learn how and why to apply cuts, which are filters that refine the dataset to focus on events of interest. Using a mock dataset you'll explore a step-by-step process to analyze data and uncover meaningful patterns. By the end, you'll have a clearer understanding of how cuts help are done, to later use them to reveal the hidden physics within a larger dataset.

### What is a Mock Dataset?
A **mock dataset** is a simplified version of the data used in real experiments for analyses. It’s designed to illustrate a concept but is much smaller and easier to understand than real data. Using a mock dataset allows us to focus on learning the tools and techniques without being overwhelmed by the complexity of real experimental data. 

The mock dataset here contains rows of data representing simulated events from a physics experiment. Each row has columns describing properties of these events, such as particle energy. We'll analyze this dataset and refine it using **cuts**.
  
Below is the mock dataset. Each row represents an event, and the columns provide information about the properties of that event. We'll apply cuts step-by-step to refine this dataset.