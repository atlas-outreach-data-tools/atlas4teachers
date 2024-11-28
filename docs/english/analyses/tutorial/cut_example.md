## Example Cut: Filtering Events by Energy
Let's start with a simple cut: selecting only events where the **energy is greater than 50 GeV**.

Here’s what the dataset looks like after applying the cut:

> [!dataframe]
cut_data
> [!end]

Intially, this dataset had {data} rows or events, but after this example cut it has {cut_data_size} events.

By applying this cut, we’ve filtered out events with lower energy and retained those with energy above 50 GeV. To check that this is true, you can see the column `Energy` and confirm that all the rows have an energy greater than 50 GeV.

Now you are ready to **start applying your own cuts to the mock dataset**.

