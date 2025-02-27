# Introduzione agli istogrammi

Nella fisica delle particelle, l'analisi dell'enorme quantità di dati richiede l'uso di codice informatico piuttosto che l'ispezione manuale. Questa guida coprirà le tecniche di base dell'istogrammazione per aiutarti a visualizzare i dati dalle analisi di fisica delle alte energie (HEP), in particolare il numero di leptoni per evento nei dati del bosone Z a 13 TeV.

Questa risorsa ti guiderà attraverso alcune tecniche di calcolo di base comunemente utilizzate nelle analisi di fisica delle alte energie (HEP). Imparerai come:

1. Interagire con i file di dati di ATLAS
2. Creare, riempire, disegnare e normalizzare istogrammi

**## Passo 0: Configurazione**

Il software che utilizzeremo per analizzare i dati di ATLAS si chiama _uproot_ e _hist_. Usando `uproot`, siamo in grado di elaborare grandi set di dati, fare analisi statistiche e visualizzare i nostri dati utilizzando _hist_. I dati sono memorizzati in un formato chiamato .root

```python
# Importa le librerie
import uproot
import matplotlib.pyplot as plt
import numpy as np

print('✅ Librerie importate')
```

**## Passo 1: Caricamento dei Dati**

I dati di fisica sono comunemente memorizzati in file `[qualcosa].root`. Questi file utilizzano una struttura TTree:
- Il TTree organizza le misure in rami, ognuno dei quali rappresenta una variabile (ad es., energia, impulso).
- Ogni ramo memorizza la variabile misurata per ogni evento nel set di dati.

![Image 1: Struttura di un file root.](images/root_struct.png)

Useremo uproot per caricare il file dei dati:

```python
file = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_361106.Zee.1largeRjet1lep.root")
tree = file["mini"]

print("✅ File aperto")
```

> [!NOTE]
Se sei curioso di sapere da dove provengono i file sopra, dai un'occhiata alle istruzioni per trovare i dati Open Data di ATLAS [qui](https://opendata.atlas.cern/docs/data)
> [!END]

Per vedere cosa c'è dentro, usa `.keys()` e `.classnames()`:

```python
print(file.keys())
```
```python
print(file.classnames())
```

Questo significa che _mini_ è un oggetto TTree. Dovrebbe contenere tutti i dati di cui abbiamo bisogno. Per caricare direttamente il mini albero:

```python
my_tree = file["mini"]
```

Oppure specifica mini in `uproot.open()`:

```python
my_tree = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_361106.Zee.1largeRjet1lep.root:mini")
```

La funzione `.show()` ci permette di vedere il contenuto completo del tuo TTree in contesti come un notebook jupyter e il terminale. Ottieni qualcosa del genere:

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

Vediamo i nomi di tutte le diverse quantità memorizzate. Anziché usare la parola nome (scritta in cima alla tabella), usiamo la parola ramo. Diamo un'occhiata a un singolo ramo in questo TTree per vederne la forma. Specifichiamo quale ramo vogliamo osservare ("lep_eta") e il tipo di array che vogliamo ottenere ("np" che è l'abbreviazione di numpy array).

```python
lep_eta = my_tree["lep_eta"].array(library="np")
print(lep_eta)
```

Effettivamente, questo è un array 2D che contiene 2 elementi: un array di valori e il tipo di dati dell'array. È questo metodo di memorizzazione dei valori che permette a un array di essere 'frastagliato', ovvero di avere ogni riga di lunghezza diversa, senza creare problemi per la manipolazione dell'array.

Possiamo vedere quanti eventi sono memorizzati nell'albero guardando la lunghezza dell'array usando la funzione `len`.

```python
print(len(lep_eta))
```

**### ✍🏻 Il tuo turno**

> [!TIP]
**1)** Sostituisci i segni di cancelletto (###) nella cella sottostante per aprire il file dati _*.root_ `"https://atlas-opendata.web.cern.ch/release/2016/MC/mc_105987.WZ.root"`
> [!END]

<details>
<summary>💡 Clicca qui per suggerimento 1</summary>
Quale funzione abbiamo usato sopra per aprire un file .root?
</details>

```python
my_file = ###
  
```

<details>
<summary>💬 Risposta</summary>
  
my_file = uproot.open("https://atlas-opendata.web.cern.ch/release/2016/MC/mc_105987.WZ.root")
</details>

> [!TIP]
**2)** Carica l'albero denominato "mini" memorizzato nel file dati _.*root_. Stampa il numero di eventi in questo albero.
> [!END]

<details>
<summary>💡 Clicca qui per suggerimento 1</summary>
Tutti i dati sono memorizzati nel TTree 'mini'.
</details>

<details>
<summary>💡 Clicca qui per suggerimento 2</summary>
Scegli un ramo (nome) e restituiscilo come un array.
</details>

<details>
<summary>💡 Clicca qui per suggerimento 3</summary>
Guarda la lunghezza dell'array.
</details>

```python
my_tree = my_file["###"]
eventNumber = my_tree["###"].array(library="np")
print(len(eventNumber))
```
<details>
    <summary>💬 Risposta</summary>
        
    my_tree = my_file["mini"]
    eventNumber = my_tree["eventNumber"].array(library="np")
    print(len(eventNumber))
</details>

> [!TIP]
**3)** Avremo anche bisogno di creare variabili per il numero massimo e minimo di jet in un singolo evento in questo dataset per dopo.
> [!END]

<details>
    <summary>💡 Clicca qui per suggerimento 1</summary>
    L'oggetto di cui hai bisogno si chiama "jet_n". Ottieni un array che è il jet_n per ogni evento.
</details>


<details>
    <summary>💡 Clicca qui per suggerimento 2</summary>
    Numpy ha due funzioni, .min() e .max(), che restituiscono i valori minimo e massimo di un array.
</details>


<details>
    <summary>💡 Clicca qui per suggerimento 3</summary>
    Ricorda che il primo evento è [0]!
</details>

```python
import numpy as np

jet_n = my_tree[###].array(###)
minimum = np.min(###)
maximum = np.max(###)
print("Numero minimo di jet:", ###)
print("Numero massimo di jet:", ###)
      
#Dai un'occhiata al primo evento usando l'indicizzazione delle liste
jet_n_Event1 = jet_n[#] 
print("Numero di jet nell'Evento 1:", ###)
```

<details>
    <summary>💬 Risposta</summary>
        
    jet_n = my_tree["jet_n"].array(library="np")
    minimum = np.min(jet_n)
    maximum = np.max(jet_n)  
    print("Numero minimo di jet:", minimum)
    print("Numero massimo di jet:", maximum)
    
    jet_n_Event1 = jet_n[0]
    print("Numero di jet nell'Evento 1:", jet_n_Event1)
</details>


---

## Passo 2: Prepararsi a visualizzare gli istogrammi
Prima di poter visualizzare qualsiasi istogramma, dobbiamo importare alcuni moduli:
- `hist` è una libreria che gestisce la generazione e la personalizzazione degli istogrammi
- `Hist` è un modulo di `hist` che consente la generazione di un istogramma di base

```python
import hist
from hist import Hist
```

Per creare un istogramma, utilizziamo `Hist` e la funzione `hist.axis.Regular()`, che prende come argomenti `(bins, lower_limit, upper_limit, label)`. Ad esempio, se vogliamo contare i leptoni (da 0 a 4), impostiamo 5 bin, un limite inferiore di 0 e un limite superiore di 4:

```python
hist1 = Hist(hist.axis.Regular(5, -0.5, 4.5, label = "Numero di leptoni"))
```

L'offset di `-0.5` centra i bin su 0, 1, 2, 3 e 4.

> [!IMPORTANT]  
Non ci aspettiamo che venga stampato alcun output da questo passaggio - tutto ciò che stiamo facendo qui è dire a Python i dettagli dell'istogramma che stiamo pianificando di riempire.
> [!END]

### ✍🏻 Il tuo turno

> [!TIP] 
**4)** Crea un istogramma di modello chiamato "Numero di jet" per visualizzare il tuo grafico.
> [!END] 

<details>
    <summary>💡 Clicca qui per suggerimento 1</summary>
    Usa il numero minimo (-0.5) e massimo di jet (9.5) per i limiti dell'asse.
</details>


<details>
    <summary>💡 Clicca qui per suggerimento 2</summary>
    Usa il numero massimo di jet per il numero di bin.
</details>

```python
my_hist = Hist(hist.axis.Regular(###, ###, ###, label = ###))
```

<details>
    <summary>💬 Risposta</summary>
        
    my_hist = Hist(hist.axis.Regular(5, -0.5, 9.5, label = "Numero di jet"))
</details>

---

## Passo 3: Riempire gli istogrammi
Per riempire l'istogramma, inizia estraendo il numero di leptoni dal TTree come array numpy:

```python
lep_n = my_tree["lep_n"].array(library="np")
```

Quindi, usa `.fill()` per popolare l'istogramma:

```python
hist1.fill(lep_n)
```

Per visualizzare l'istogramma, traccialo utilizzando `.plot()` da `hist` e `plt.show()` da `matplotlib`:

```python
hist1.plot()
plt.show()
```

> [!NOTE]  
Più avanti, perfezioneremo l'istogramma applicando dei "tagli", includendo solo eventi che soddisfano criteri specifici.
> [!END]

### ✍🏻 Il tuo turno

> [!TIP]  
**5)** Riempi il tuo istogramma con il numero di jet in ogni evento.
> [!END]

<details>
    <summary>💡 Clicca qui per suggerimento 1</summary>
        Ricorda: abbiamo già creato un istogramma di modello.
</details>


<details>
    <summary>💡 Clicca qui per suggerimento 2</summary>
        I dati che ti interessano sono "jet_n".
</details>

```python
my_hist.fill(###)
my_hist.###
plt.###
  
```

<details>
    <summary>💬 Risposta</summary>
        
    my_hist.fill(jet_n)
    my_hist.plot()
    plt.show()
</details>

---

## Passo 4: Disegnare gli istogrammi

Per prima cosa, impostiamo un istogramma di base con un titolo:

```python
hist2 = Hist(hist.axis.Regular(5, -0.5, 4.5, label="Numero di leptoni"))
hist2.fill(lep_n)
hist2.plot()
plt.title("Numero di leptoni in un dataset a 13 TeV")
plt.show()
```

Per confrontare i conteggi dei leptoni tra i dataset, carichiamo due dataset e tracciamoli sullo stesso asse:

```python
# Carica dataset aggiuntivi
tr1 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363491.lllv.1largeRjet1lep.root:mini")
lep_n1 = tr1["lep_n"].array(library="np")

tr2 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363492.llvv.1largeRjet1lep.root:mini")
lep_n2 = tr2["lep_n"].array(library="np")
```

Ora possiamo creare e riempire due istogrammi:

```python
# Crea e riempi istogrammi
hist1 = Hist(hist.axis.Regular(5, -0.5, 4.5, label="Numero di leptoni"))
hist1.fill(lep_n1)

hist2 = Hist(hist.axis.Regular(5, -0.5, 4.5, label="Numero di leptoni"))
hist2.fill(lep_n2)
```

Qui, gli eventi in questione hanno prodotto leptoni e i loro neutrini associati. Siamo curiosi di sapere quanti leptoni sono stati prodotti in ogni evento e come questi numeri si confrontano, quindi sovrapporre i nostri istogrammi sarebbe preferibile. Questo è un processo semplice. Puoi riempire due istogrammi separati e tracciarli uno dopo l'altro. Ogni volta che esegui `plot()`, disegnerà l'istogramma sopra ciò che è già presente. Ovviamente esegui `plt.show()` per visualizzare ciò che hai disegnato.

Sovrapponi entrambi gli istogrammi e visualizzali insieme:

```python
# Traccia entrambi gli istogrammi
hist1.plot()
hist2.plot()
plt.title("Conteggi di leptoni per evento per più dataset")
plt.legend(["Dataset 1", "Dataset 2"])
plt.show()
```

Per una versione impilata, combina e traccia gli istogrammi direttamente:

```python
histo_sum = hist1 + hist2
histo_sum.plot(histtype="fill")
plt.title("Conteggi di leptoni impilati per evento")
plt.show()
```

Possiamo anche usare la funzione `.stack()` di `hist`, per sovrapporre o impilare gli istogrammi, anche se dovremo prepararci un po' prima.

Ora abbiamo bisogno di un 'asse categoria' o `cax`, che funziona in modo simile a un dizionario. Il suo $1^{st}$ argomento è una lista di etichette degli istogrammi e il suo $2^{nd}$ argomento è un'etichetta per l'asse collettivo. In effetti, ogni etichetta dell'istogramma è come una chiave, collegando ogni istogramma al suo nome, colore e posizione.

```python
# Crea un istogramma categorizzato per l'impilamento
ax = hist.axis.Regular(5, -0.5, 4.5, flow=False, name="Numero di leptoni")
cax = hist.axis.StrCategory(["Dataset 1", "Dataset 2"], name="dataset")

stacked_hist = Hist(ax, cax)
stacked_hist.fill(lep_n1, dataset="Dataset 1")
stacked_hist.fill(lep_n2, dataset="Dataset 2")

stacked_hist.stack("dataset").plot(histtype="fill")
plt.title("Conteggi di leptoni impilati per evento")
plt.legend()
plt.show()
```

Questo sembra lo stesso dell'output del nostro precedente metodo di sovrapposizione, come dovrebbe! Questo grafico è leggermente più discernibile. La legenda aggiunta aiuta anche.

### ✍🏻 Il tuo turno

> [!TIP]
**6)** Visualizza più istogrammi per il numero di leptoni nello stesso grafico. Avrai bisogno dei seguenti file:
- 4 leptoni - https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363490.llll.4lep.root
- 3 leptoni - https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363491.lllv.1largeRjet1lep.root
> [!END]

<details>
    <summary>💡 Clicca qui per suggerimento 1</summary>
        Avrai bisogno di accedere ai dati del TTree per il numero di leptoni 2 volte separate, 1 per ogni dataset.
</details>

<details>
    <summary>💡 Clicca qui per suggerimento 2</summary>
        Pensa ai numeri di bin e ai confini per il tuo asse, e ricorda che abbiamo 2 dataset quando generiamo l'asse categoria.
</details>

<details>
    <summary>💡 Clicca qui per suggerimento 3</summary>
        Avrai bisogno di riempire il tuo istogramma modello 2 volte.
</details>

```python
### Ripeti per ogni file root
tr1 = uproot.open(###)
lep_n1 = tr1[###].array(###)

### Ripeti 4 volte
ax = hist.axis.Regular(###)
cax = hist.axis.StrCategory([###], name = ###)
full_hist = Hist(###, ###)

full_hist.fill(###, c = ###)
### Ripeti 4 volte

s = full_hist.stack(###)
s.###
plt.title(###)
plt.###
plt.###
```

<details>
    <summary>💬 Risposta</summary>

    # Carica i dataset con 4 leptoni e 3 leptoni
    tr1 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363490.llll.4lep.root:mini")
    lep_n1 = tr1["lep_n"].array(library="np")

    tr2 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363491.lllv.1largeRjet1lep.root:mini")
    lep_n2 = tr2["lep_n"].array(library="np")

    # Definisci gli assi dell'istogramma
    ax = hist.axis.Regular(6, -0.5, 5.5, name="Numero di leptoni")
    cax = hist.axis.StrCategory(["4 leptoni", "3 leptoni + neutrino"], name="dataset")

    # Crea e riempi l'istogramma categorizzato
    full_hist = Hist(ax, cax)
    full_hist.fill(lep_n1, dataset="4 leptoni")
    full_hist.fill(lep_n2, dataset="3 leptoni + neutrino")

    # Traccia l'istogramma impilato
    s = full_hist.stack("dataset")
    s.plot(histtype="fill")
    plt.title("Conteggi di leptoni per evento per due dataset")
    plt.legend()
    plt.show()
</details>

---

## Passo 5: Normalizzare gli istogrammi
Spesso siamo più interessati alle **proporzioni** del nostro istogramma piuttosto che al numero assoluto di eventi che contiene (che può cambiare a seconda del dataset utilizzato). Il nostro ultimo passo sarà quello di riscalare l'asse y del nostro istogramma in modo che il totale dell'istogramma sia uguale a 1. Questo si chiama **normalizzazione**.

Per prima cosa, estrai i valori dei bin (altezze) come array e calcola la somma. Usiamo la funzione `.sum()` sul nostro array di valori dei bin per sommare i valori che contiene, quindi creiamo un nuovo array contenente ciascuno dei valori originali dei bin diviso per la somma.

```python
arr = hist1.values()
arr_normalized = arr / arr.sum()
```

Crea un nuovo istogramma e imposta i suoi valori dei bin sui valori normalizzati:

```python
hist_normalized = Hist(hist.axis.Regular(5, -0.5, 4.5, flow=False, label="Numero di leptoni"))
hist_normalized[...] = arr_normalized  # Assegna i valori normalizzati ai bin
```

Vediamo cosa otteniamo!

```python
hist_normalized.plot(histtype="fill")
plt.title("Conteggio normalizzato dei leptoni")
plt.show()
```

Ora mostriamo che questo è normalizzato - abbiamo già usato la funzione necessaria per farlo!

```python
print(hist_normalized.sum())
```

### ✍🏻 Il tuo turno
> [!TIP]
**6)** Normalizza il tuo istogramma e ridisegnalo.
> [!END]

<details>
    <summary>💡 Clicca qui per suggerimento 1</summary>
        Usa `.values()` per accedere all'altezza di ciascuna barra nell'istogramma.
</details>


<details>
    <summary>💡 Clicca qui per suggerimento 2</summary>
        Usa `.sum` per trovare la somma di queste altezze - dovrai dividere l'altezza di ciascuna barra per la somma.
</details>


<details>
    <summary>💡 Clicca qui per suggerimento 3</summary>
        Ridisegna il tuo istogramma e assegna nuovi valori a ciascun bin.
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
    <summary>💬 Risposta</summary>
        
    # Ottieni i valori dei bin dall'istogramma originale e normalizzali
    heights = my_hist.values()
    norm_heights = heights / heights.sum()

    # Crea un nuovo istogramma con i valori normalizzati
    new_hist = Hist(hist.axis.Regular(5, -0.5, 4.5, label="Numero di jet"))
    new_hist[...] = norm_heights  # Assegna i valori normalizzati ai bin

    # Traccia l'istogramma normalizzato
    new_hist.plot(histtype="fill")
    plt.title("Conteggio normalizzato dei jet per evento")
    plt.show()
</details>

---

**Congratulazioni!** Hai lavorato con dati reali di ATLAS come un vero fisico delle particelle!

Se vuoi continuare a imparare come usare Python per analizzare i dati pubblici di ATLAS, puoi dare un'occhiata ai [notebook nel sito web di ATLAS Open Data](https://opendata.atlas.cern/docs/category/analysis-notebooks).

