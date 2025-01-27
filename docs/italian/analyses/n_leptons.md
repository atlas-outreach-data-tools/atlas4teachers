## Number of Leptons in the Final State
When particles are produced in a particle collider, they often decay immediately into other particles. These decay products are what we detect and analyze. By studying the particles in the final state (those visible after all decays), we can infer which particles were originally created in the collision.

To understand this better, let’s take a look at [Feynman diagrams](https://cds.cern.ch/record/2759490/files/Feynman%20Diagrams%20-%20ATLAS%20Cheat%20Sheet.pdf). These diagrams help visualize particle interactions. In the examples below, we are reading the diagrams **from left to right**: the particles on the left are produced in the collision, and the particles on the right are the final decay products that we detect.

Here is a diagram showing a Z boson decaying into two leptons (either electrons or muons):

![Z boson decay into two leptons](images/Z_decay_{theme}.png)

In the previous diagram, the wiggly line on the left represents the Z boson, produced in the collision. As we move to the right, the Z boson reaches a vertex, where it decays into two leptons. These leptons are shown as straight lines, labeled ℓ, which could be either electrons or muons. The arrows on the lines indicate whether each lepton is a particle or an antiparticle: arrows pointing to the right show particles, while arrows pointing to the left show antiparticles. This diagram illustrates how a Z boson decays into a pair of leptons with opposite charges, which we detect in our experiment .

More complex processes, such as Higgs boson decays, can result in more leptons in the final state. For example, here is a Higgs boson decaying into two Z bosons, each of which decays further into two leptons:

![Higgs boson decay into Z bosons and leptons](images/higgs4l_decay_{theme}.png)

A dashed line on the left represents the Higgs boson (H). The Higgs boson decays at a vertex into two Z bosons, shown as wiggly lines labeled Z. Each Z boson then decays further into two leptons, just like in the first diagram. Again, the straight lines with arrows represent the leptons, with the direction of the arrow indicating whether they are particles or antiparticles. In total, this process results in four leptons, which are the final particles we detect. This diagram demonstrates how a Higgs boson decay can lead to multiple particles through a cascade of interactions.

In many particle processes, particles are often produced in pairs. For example, the Z boson decays into two leptons—a particle and its antiparticle—because it interacts equally with both matter and antimatter. Similarly, the Higgs boson produces multiple leptons when its decay involves intermediate particles like Z bosons, which themselves decay into lepton pairs.

The dataset you are analyzing contains events with varying numbers of leptons. Below is a plot showing the distribution of lepton counts in the entire dataset. Events with fewer leptons are more common because simpler processes, like those involving W or Z bosons, occur more frequently than rarer, complex ones like Higgs boson decays.

![Distribution of the number of leptons detected per event in the dataset](images/lepton_plot_{theme}_{lumi}.png)

Study the Feynman diagrams and the data above. Depending on whether you're focusing on finding the Z boson or the Higgs boson, select the number of leptons you expect to observe in your final state.

> [!CAUTION] 
When selecting the number of leptons, additional criteria are applied to ensure the quality of the data. Leptons must be well-separated from other particles (**isolated**) and **accurately identified** as electrons or muons. Since particles can sometimes be misidentified, we use identification levels to measure how confident we are in their type. Additionally, only events with signals strong enough to activate the detector's selection system (called triggers), specifically for identifying electrons or muons, are included.
> [!END]