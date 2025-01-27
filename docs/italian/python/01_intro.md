# Basi di Python

Essere in grado di scrivere codice è una abilità essenziale per un Fisico delle Particelle (o qualsiasi scienziato, per la verità). I nostri dati sono troppo ingombranti per essere elaborati senza l'aiuto dei computer! Un fisico di ATLAS utilizza tipicamente una combinazione dei linguaggi di programmazione C++ e Python per fare qualunque cosa, dall'allestimento delle collisioni protone-protone al ricerca del bosone di Higgs.

Ecco una panoramica dei concetti basilari della programmazione in Python. Prenderemo in considerazione una versione diluita e interattiva del tutorial ufficiale della [documentazione Python](https://docs.python.org/3/tutorial/index.html). Per ulteriori informazioni su qualsiasi argomento, consulta la documentazione Python ufficiale, che sarà il vostro primo punto di contatto.

Python è utilizzato ampiamente da principianti e ingegneri informatici. È divertente! È stato chiamato così perché si riferisce alla serie della BBC "Monty Python's Flying Circus" e si riferisce al suo fondatore come un Benevolo Dittatore per la Vita ([BDFL](https://docs.python.org/3/glossary.html)).

---
  
## Hello, world
Il programma ["Hello, world!"](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) è una tradizione onorata nell' Informatica, che noi ripetteremo. 
L'idea di Hello, world! è di illustrare i concetti basilari di un linguaggio e verificare che l'ambiente di codifica sia stato installato e configurato correttamente. 
Per testare Python in questa app, prova a eseguire il codice della cella qua sotto (il pulsante "esegui" nella parte inferiore destra della cella o `control + Invio` / `command + Invio`).


```python
print("Hello, World!")
```

---

## Numeri, Stringhe e Tipi di Dati Composti
> Seguendo [Un'introduzione informale a Python](https://docs.python.org/3/tutorial/introduction.html)
**### Python come calcolatrice**
Python è bravo in matematica! Esegui gli esempi delle seguenti celle di codice per vedere cosa fanno gli operatori `+`, `-`, `*` e `/`, scoprendo che hanno l'effetto di addizione, sottrazione, moltiplicazione e divisione.

```python
print(2+2)
```

```python
print((50 - 5*6) / 4)
```

Python fornisce inoltre un comodo operatore di potenza `**`.

```python
print(2**7) # Potenza
```

```python
print(4**(1/2)) # Usa la potenza frazionaria per calcolare le radici
```

Hai notato i `#` sopra? Questa notazione dice a Python che tutto ciò che segue il simbolo nella stessa riga non deve essere eseguito come comando, ma è solo un commento.
Perché alcuni dei numeri prodotti da queste operazioni hanno punti decimali, mentre altri no? È perché qui abbiamo due _tipi_ di numeri: tipi `int` e tipi `float`. Il tipo `float` rappresenta un [numero in virgola mobile](https://it.wikipedia.org/wiki/Aritmetica_in_virgola_mobile) ed è la rappresentazione binaria formale di un numero decimale in un computer. Il tipo `int` rappresenta valori interi.
> Se sei fortunato, non dovrai mai preoccuparti della 'precisione in virgola mobile', ma può essere una considerazione significativa, con errori che in passato hanno causato [esplosioni di razzi](http://www-users.math.umn.edu/~arnold/disasters/ariane.html)!

È possibile assegnare un valore a una variabile usando l'operatore `=`.

```python
x = 4
print(x**2)
```

Anche gli operatori in-place `+=`, `-=`, `*=` e `/=` sono molto utili. Questi eseguono un'operazione sulla variabile a cui sono applicati, riassegnando poi quella variabile al risultato dell'operazione.

```python
y = 10
y += 2
print(y)
```
**### Stringhe**
La `stringa` di Python è una sequenza di caratteri racchiusa tra virgolette (`'...'` o `"..."`). Le stringhe possono essere oggetto delle suddette operazioni matematiche e sono indicizzate come se fossero liste di caratteri!

```python
prefix = 'Py'
print(prefix + 'thon')
```

```python
print(3 * 'un' + 'ium')
```

```python
word = 'Python'
# Accedere al primo carattere della stringa che è indicizzato da 0
print(word[0])
# Accedere all'ultimo carattere della stringa che è indicizzato da -1
print(word[-1])
# Suddividere la stringa dall'indice 1 (incluso) al 5 (non incluso)
print(word[1:5])
```

**### Tipi di Dati Composti**
Una lista in Python è un tipo di dato composto e mutabile (cioè, puoi modificarla) utilizzato per raggruppare una sequenza di valori, ordinandoli in modo tale da poter trovare ogni voce nell'array attraverso il suo "numero di casa" o indice.

```python
# Ecco una lista di esempio
nums = [1, 2, 3]
# Le liste sono mutabili
nums[0] = 4 # Come le stringhe, il conteggio degli elementi inizia da 0, non da 1
print(nums)
```

```python
# Le liste possono contenere diversi tipi di dati
nums += ['a']
print(nums)
```

```python
# Le liste possono essere 'suddivise'
print(nums[1:3])
```

La funzione [built-in](https://docs.python.org/3/library/functions.html) [`len(s)`](https://docs.python.org/3/library/functions.html#len) restituisce la lunghezza, o il numero di elementi, di una sequenza o collezione `s`. Un eccellente esempio di utilizzo è trovare quale tra le parole ['Llanfairpwllgwyngyllgogerychwyrndrobwllsantysiliogogogoch'](https://en.wikipedia.org/wiki/Llanfairpwllgwyngyll) e 'supercalifragilisticexpialidocious' è più lunga.

```python
len_llanfair = len('Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch')
len_supercali = len('supercalifragilisticexpialidocious')

print(len_llanfair)
print(len_llanfair / len_supercali)
```

Come tipi di dati composti, le [_tuple_](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences) e i [_dizionari_](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) sono anche frequentemente usati. Riesci a capire cosa fanno dalle pagine collegate? Sentiti libero di creare nuove celle di codice qui per esplorare.

## Controllo del Flusso
Nei frammenti di codice di esempio precedenti (le operazioni matematiche e sulle stringhe, e le manipolazioni delle liste), abbiamo programmato i nostri comandi per essere eseguiti riga per riga. Sarebbe giusto dire che questi programmi dall'alto verso il basso sono piuttosto noiosi. Un programma può essere reso più complesso mostrando un [controllo del flusso](https://it.wikipedia.org/wiki/Controllo_di_flusso) attraverso l'uso di [__istruzioni di controllo del flusso__](https://docs.python.org/3/tutorial/controlflow.html).

Python ha due tipi di istruzioni di controllo del flusso: istruzioni condizionali e costrutti di loop. Le istruzioni condizionali (`if`, `elif`, `else`) vengono utilizzate per eseguire blocchi di codice solo quando vengono soddisfatte determinate condizioni – Python esegue il comando menzionato dopo la dichiarazione "if" solo se la condizione "if" è vera, altrimenti non lo esegue. I costrutti di loop sono utilizzati per eseguire blocchi di codice un certo numero di volte (`for`) o mentre certe condizioni sono soddisfatte (`while`).

### Istruzioni `if`

```python
x = 12
# Esempio di blocco condizionale 'if'
if x < 0: # Python verifica se questa è una condizione vera
    print('Hai inserito un numero negativo!')
elif x == 0: # Abbreviazione di 'else if', questa condizione viene verificata se l'istruzione 'if' è falsa
    print('Hai inserito zero')
else: # Tutti gli altri casi
    print('Hai inserito un numero positivo')
```

Hai notato lo spazio bianco (specificamente, 4 spazi) davanti ai blocchi di codice dopo `if`, `elif` e `else`? Lo chiamiamo _indentazione_ e dice a Python quali righe di codice devono essere eseguite solo se l'istruzione di controllo del flusso è vera. Questo ha il vantaggio che il codice diventa facilmente leggibile per gli esseri umani. Quindi, ricorda, indentazione = 4 volte barra spaziatrice.

### Istruzioni `for`

Le istruzioni `for` in Python ti permettono di iterare sugli elementi di qualsiasi sequenza (come una lista o una stringa) nell'ordine.

Nota di nuovo l'_indentazione_!

```python
# Misura alcune stringhe in un ciclo `for`
words = ['cat', 'window', 'defenestrate', 'quark']
for w in words:
    print(w, len(w))
```

In congiunzione con le istruzioni `for`, la funzione integrata [`range()`](https://docs.python.org/3/library/stdtypes.html#range) è spesso utile. Restituisce un oggetto range, costruito chiamando `range(stop)` o `range(start, stop[, step])`, che rappresenta una sequenza di numeri che vanno da `start` (0 di default) a `stop` in passi di `step` (1 di default).

```python
# Esempio di ciclo 'for' su un range che aggiunge elementi a una lista
items = []
for i in range(10):
    items.append(i) # .append() è un altro modo utile per aggiungere qualcosa alla fine di una lista in python
print(items)
```

### Istruzioni `while`

Un ciclo `while` viene eseguito finché la `condition` è vera. La cella sottostante è un esempio di un ciclo `while`:

```python
# Un uso interessante del ciclo while: calcolare la serie di Fibonacci!
a, b = 0, 1
while a < 1000:
    print(a, end=' ')
    a, b = b, a + b
```

Se la condizione è sempre vera, si ha un ciclo infinito, un ciclo che non finirà mai. Nelle applicazioni, puoi interrompere l'esecuzione del codice facendo clic sul pulsante di stop nell'angolo in alto a destra.

## Funzioni

Cosa succede se vogliamo utilizzare un blocco di codice più volte e in posizioni diverse? Potremmo semplicemente copiare e incollare quel blocco di codice ogni volta che vogliamo usarlo, ma c'è un modo migliore! Possiamo racchiudere il blocco di codice in una [__funzione__](https://docs.python.org/3/tutorial/controlflow.html#defining-functions) e 'chiamare' quella funzione tutte le volte che vogliamo.

Per creare una funzione in Python, indichiamo dove iniziano e finiscono i calcoli all'interno della funzione usando l'indentazione (come per `if/else`, `for` e `while` sopra).

Ecco le parti importanti delle funzioni in Python:

- Iniziano con `def`, poi segue il nome scelto per la funzione e poi, tra parentesi tonde, il nome o i nomi delle variabili di input, seguito da due punti.
- Le righe successive, dove effettivamente fai calcolare qualcosa alla funzione, devono iniziare con 4 spazi bianchi.
- Dichiari esplicitamente quale valore è il valore di uscita con `return` seguito dal nome dell'output.

Nella sezione precedente abbiamo calcolato tutti i termini della sequenza di Fibonacci che sono inferiori a 1000. Creando una funzione `fibonacci(n)` del nostro codice di Fibonacci, possiamo fornire il limite superiore come parametro `n` della funzione e calcolare la serie fino a molti diversi valori di `n`!

```python
def fibonacci(n):
    '''Calcolare e stampare i termini della serie di Fibonacci
    che sono inferiori a `n`.'''
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
    print()
    return

# Stampare i termini della serie di Fibonacci che sono inferiori a n = 10
fibonacci(10)
```

Hai notato l'istruzione `return` nella definizione della funzione `fibonacci`? Non faceva nulla! Ma in generale possiamo usare l'istruzione `return` per restituire (cioè _passare_) informazioni dall'interno di una funzione all'esterno. Considera il seguente aggiornamento della funzione originale `fibonacci`. Questa restituisce una lista dei termini della serie di Fibonacci, che potrebbe essere più utile rispetto allo stamparli!

```python
def return_fibonacci_series(n):
    '''Calcolare i termini della serie di Fibonacci
    che sono inferiori a `n`, restituendo una lista del risultato.'''
    # Creare una lista chiamata 'series' per memorizzare i termini
    series = []
    # Calcolare i termini fino a n
    a, b = 0, 1
    while a < n:
        series.append(a)
        a, b = b, a + b
    # Restituire la serie
    return series
```

Verifichiamo se questa funzione si comporta come ci aspettiamo. Lo faremo chiamandola con `n = 100` e poi operando sulla lista restituita.

```python
result = return_fibonacci_series(100)
  
# Stampare il risultato...
print(result)
  
# Invertire il risultato e stamparlo, solo per divertimento...
reversed_result = list(reversed(result))
print(reversed_result)
```

Quando abbiamo stampato la serie di Fibonacci in un ciclo `for`, abbiamo finito per stampare ogni nuova serie molte volte. Usando la lista restituita dalla funzione aggiornata di Fibonacci, ora possiamo stampare la serie solo se differisce dalla serie precedente! Il prossimo esempio illustra come implementare ciò:

```python
# Variabile per contenere il termine attualmente più grande
largest_term = -1
  
for n in range(10000):
    # Chiamare la funzione aggiornata di Fibonacci che restituisce una lista di termini
    series = return_fibonacci_series(n)
    # Se la serie contiene termini (`if series` verifica che `series` non sia vuota = [])
    if series:
        # Se il termine più grande è maggiore del termine più grande visto finora
        series_largest_term = series[-1]
        if series_largest_term > largest_term:
            # Stampare la serie
            for term in series:
                print(term, end=' ')
            print()
            # Aggiornare il termine più grande
            largest_term = series_largest_term
```

Come vedi in quest'ultimo esempio, le tecniche di codifica che abbiamo appreso in questo notebook ci permettono di scrivere alcuni programmi veramente complessi!

---

## Moduli
Abbiamo scritto piccoli snippet di codice usa e getta e li abbiamo eseguiti, per poi procedere e dimenticarcene. Quando si tratta di scrivere un programma più elaborato, è più conveniente mettere il tuo codice in un file. Quando un file è riempito con definizioni Python, diventa un [__modulo__][module] che può essere _importato_ da altri file Python per permettere l'uso del suo contenuto.

L'approccio orientato ai moduli nello sviluppo software ha l'effetto di mantenere il tuo codice organizzato, ma soprattutto facilita la condivisione del codice. Nel mondo del software open-source e gratuito, gran parte del codice che dovrai mai scrivere è già stato scritto ed è disponibile per l'uso! Raramente si deve codificare tutto da zero.

Tra le librerie più popolari ci sono:
* [`numpy`](https://numpy.org/) per il calcolo numerico
* [`matplotlib`](https://matplotlib.org/) per la visualizzazione dei dati
* [`tensorflow`](https://www.tensorflow.org/) per l'apprendimento automatico
* [`pandas`](https://pandas.pydata.org/) per la manipolazione dei dati

Queste librerie di moduli sono disponibili gratuitamente. Esploriamo più nel dettaglio le prime due.

### Il modulo `numpy`
Se vogliamo fare qualche operazione matematica più complicata (come spesso accade in fisica), possiamo usare un pacchetto chiamato `"numpy"`, che è una libreria molto potente e spesso utilizzata per operazioni numeriche. Cominciamo importandolo.

```python
import numpy as np
```

Potremmo anche scrivere "import numpy", ma allora dovremmo digitare ogni volta che vogliamo usare una funzione di numpy "numpy.nome_della_funzione", mentre con "as np" risparmiamo qualche battitura e dobbiamo solo scrivere "np.nome_della_funzione".

`numpy` ci offre modi alternativi di eseguire operazioni, oltre a una propria versione delle liste chiamate "array".

```python
print(np.sqrt(2))
```
```python
print(np.power(2, 10))
```
```python
arr = np.array([2., 4., 6., 8., 10.])
print(arr)
```
Gli array di `numpy` possono essere indicizzati e suddivisi allo stesso modo delle liste regolari:
```python
print(arr[4])
print(arr[-1])
print(arr[0:3])
```

`numpy` ha anche una propria versione della funzione `range()` - `np.arange()`.

```python
print(np.arange(2, 2.8, 0.1)) #(inizio, fine, [passo])
```

**Ma**, `numpy` ha anche comandi molto utili che non sono disponibili di default in Python.

Un esempio è `np.zeros` che crea un array riempito con zeri (e avrà tanti zeri quanti sono i numeri che dai tra parentesi).

```python
print(np.zeros(5))
```

Se vuoi invece un array riempito con unità:

```python
print(np.ones(3))
```

Per creare un array con, diciamo, 5 numeri distribuiti linearmente tra i valori 1 e 10:

```python
print(np.linspace(1, 100, 5))
```

Per creare un array con 5 numeri distribuiti logaritmicamente tra i valori 10$^1$ e 10$^{10}$:

```python
print(np.logspace(1, 10, 5))
```

A differenza delle liste in Python, gli array di `numpy` possono essere manipolati molto facilmente! Supponiamo, ad esempio, di avere un array con alcuni numeri e si desidera moltiplicare ogni numero nell'array per un fattore di 2. Prima creiamo l'array:

```python
arr = np.arange(2,12)
print(arr)
```

Poi creiamo il nuovo array con i valori moltiplicati:

```python
newarr = 2 * arr
print(newarr)
```

Facile!

### Il modulo `matplotlib`

Uno dei punti di forza di Python è che è abbastanza facile organizzare i tuoi dati (ad esempio, le tue misure) in array e poi tracciarli in un bel grafico.

Per fare il plotting in Python, si utilizza la libreria `matplotlib.pyplot`. Come prima, caricheremo la libreria con una scorciatoia conveniente in modo da dover digitare meno in seguito:

```python
import matplotlib.pyplot as plt
```

Ora definiamo alcuni dati come quelli che andranno sull'asse X del nostro grafico, e altri dati che andranno sull'asse Y.

Supponiamo che i nostri valori di x siano interi tra 0 e 10:

```python
x = np.arange(0, 10)
print(x)
```

E supponiamo che i nostri valori di y siano i valori di x elevati alla potenza di due:

```python
y = x**2
print(y)
```

Ora vogliamo tracciare i dati x e y. Prima diciamo a Python di creare una nuova figura con il comando `plt.figure()`; per ora non fa molto, ma può diventare importante quando si fanno più figure e si vuole iniziare ogni volta un nuovo grafico e non sovrapporre al vecchio. Dopo aver creato la figura vuota, tracciamo i dati x e y con il comando `plt.plot`.

```python
plt.figure()
plt.plot(x, y)
plt.show()
```

Ora possiamo vedere il nostro grafico! Tuttavia, al momento non sembra molto interessante. Aggiungiamo qualche linea extra per cambiarlo:

```python
plt.plot(x, y, 'o', label='y') # questo traccia solo marker circolari, ma non linee
plt.plot(x, 1.1*y, '-o', label='1.1y') # questo traccia marker e linee
plt.plot(x, 0.9*y, '--', label='0.9y') # questo traccia linee tratteggiate invece di linee solide
plt.axis([3, 10, 0, 100]) # questo zoom in una certa parte del grafico (x_inizio, x_fine, y_inizio, y_fine)
plt.xlabel('asse x') # Aggiunge un'etichetta all'asse x
plt.ylabel('asse y') # Aggiunge un'etichetta all'asse y
plt.title('Il mio grafico') # Aggiunge un titolo al grafico
plt.legend(loc='best') # Aggiunge una legenda, nella posizione che matplotlib ritiene migliore
```

Come puoi vedere, matplotlib sceglie automaticamente un nuovo colore se tracci qualcosa di nuovo nello stesso grafico. Puoi anche controllare direttamente quale colore vuoi usare con queste abbreviazioni:

- 'b' = blu
- 'g' = verde
- 'r' = rosso
- 'y' = giallo
- 'c' = ciano
- 'm' = magenta
- 'k' = nero
- 'w' = bianco

E alcuni marker diversi:

- 'o' per un grande cerchio
- '.' per un piccolo cerchio
- 's' per un quadrato
- '*' per una stella
- '+' per un segno di più
- e molti altri

E ci sono vari stili di linea da utilizzare:

- '-' per una linea solida
- '--' per una linea tratteggiata
- ':' per una linea punteggiata
- '-.' per una linea mista tratto-punto

e solo il simbolo del marker, ma nessun simbolo per la linea per avere solo i marker.

Ecco un esempio di come usare tutto ciò:

```python
plt.figure(figsize=(8,6))
plt.plot(x, 0.1*y, 'b-')
plt.plot(x, 0.2*y, 'g-o')
plt.plot(x, 0.3*y, 'y--*')
plt.plot(x, 0.4*y, 'r.')
plt.plot(x, 0.5*y, 'm-.')
plt.plot(x, 0.6*y, 'ws')
plt.plot(x, 0.7*y, 'k:+')
plt.xlabel('asse x') # Aggiunge un'etichetta all'asse x
plt.ylabel('asse y') # Aggiunge un'etichetta all'asse y
plt.title('Un altro grafico') # Aggiunge un titolo al grafico
plt.show()
```

---

## Conclusione
Siamo passati molto rapidamente da zero a sessanta nel programmare in Python! Abbiamo lavorato in un notebook Jupyter dove possiamo eseguire codice interattivamente e scrivere testo per annotare cosa stiamo facendo. Dopo aver detto `'Hello, World!'`, abbiamo imparato a fare matematica con Python e come usare stringhe e tipi di dati composti. Utilizzando istruzioni di controllo del flusso, abbiamo visto che possiamo scrivere programmi molto complessi, che possiamo organizzare in funzioni e moduli per comodità e condivisibilità!

Su tutte queste caratteristiche siamo stati brevi per poter passare rapidamente a argomenti più interessanti. A tale scopo, abbiamo omesso o sorvolato molti dettagli e molte tecnicalità - c'è molto di più da imparare! Ma imparare indipendentemente a fare qualcosa di nuovo può essere parte del divertimento ed è certamente parte del lavoro. Quando programmi, è normale non sapere immediatamente come fare qualcosa.

> [!CAUTION]
Utilizzando Python, fai parte di una grande comunità globale. Questo significa che internet è pieno di consigli su come scrivere bene il codice Python. Descrivere il tuo problema a un motore di ricerca spesso porta a una soluzione immediata. Fai buon uso di ciò che altri Pythonisti sanno su Python!
> [!END]

Buona fortuna nell'analisi dei dati aperti di ATLAS! Speriamo che questa introduzione alla programmazione in Python ti sia utile.

Se vuoi continuare a imparare come Python viene utilizzato nella fisica delle particelle sperimentale, ti consigliamo di dare un'occhiata alla scheda "Introduzione all'istogrammazione" su questa pagina.