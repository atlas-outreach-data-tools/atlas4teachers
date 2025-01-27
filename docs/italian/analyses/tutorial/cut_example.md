## Esempio di Selezione: Filtraggio degli Eventi per Energia
Iniziamo con una selezione semplice: selezionare solo gli eventi in cui l'**energia è maggiore di 50 GeV**.

Ecco come appare il dataset dopo aver applicato la selezione:

> [!dataframe]
cut_data
> [!end]

Inizialmente, questo dataset aveva {data} righe o eventi, ma dopo questa selezione di esempio ha {cut_data_size} eventi.

Applicando questa selezione, abbiamo filtrato gli eventi con energia più bassa e mantenuto quelli con energia superiore a 50 GeV. Per verificare che ciò sia vero, puoi vedere la colonna `Energy` e confermare che tutte le righe hanno un'energia maggiore di 50 GeV.

Ora sei pronto per **iniziare ad applicare le tue selezioni al dataset di esempio**.