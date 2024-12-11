Usaremos uproot para cargar el archivo de datos:

```python
file = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_361106.Zee.1largeRjet1lep.root")
tree = file["mini"]

print("✅ File opened")
```

> [!NOTE]  
Si tienes curiosidad sobre el origen de los archivos anteriores, consulta las instrucciones para encontrar los datos abiertos de ATLAS [aquí](https://opendata.atlas.cern/docs/data)
> [!END]

Para ver qué hay dentro, usa `.keys()` y `.classnames()`:

```python
print(file.keys())
```
```python
print(file.classnames())
```

Esto significa que *mini* es un objeto TTree. Debe contener todos los datos que necesitamos. Para cargar el miniárbol directamente:

```python
my_tree = file["mini"]
```

O especifica mini en `uproot.open()`:

```python
my_tree = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_361106.Zee.1largeRjet1lep.root:mini")
```

La función `.show()` nos permite ver el contenido completo de nuestro TTree en configuraciones como Jupyter Notebook y la terminal. Obtendrás algo como esto:

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

Vemos los nombres de todas las diferentes variables almacenadas. En lugar de utilizar la palabra nombre (escrita en la parte superior de la tabla), utilizamos la palabra rama. Observemos una rama individual en este TTree para ver su forma. Especificamos qué rama queremos ver ("lep_eta") y el tipo de matriz que queremos generar ("np", que es la abreviatura de matriz numpy)

```python
lep_eta = my_tree["lep_eta"].array(library="np")
print(lep_eta)
```

En efecto, se trata de una matriz 2D que contiene 2 elementos: una matriz de valores y el tipo de datos de la matriz. Este método de almacenamiento de valores es el que permite que una matriz sea "irregular" (es decir, que cada fila tenga una longitud diferente) sin que se convierta en un problema para la manipulación de la matriz.

Podemos ver cuántos eventos se almacenan en el árbol observando la longitud de la matriz utilizando la función `len`

```python
print(len(lep_eta))
```

### ✍🏻 Tu turno

> [!TIP]  
**1)** Reemplace los signos numeral (###) en la celda a continuación para abrir el archivo de datos _*.root_ `"https://atlas-opendata.web.cern.ch/release/2016/MC/mc_105987.WZ.root"`
> [!END]

<details>
    <summary>💡 Clic aquí para obtener la pista 1</summary>
    
    ¿Qué función usamos arriba para abrir un archivo .root?
</details>

```python
my_file = ###

```

<details>
    <summary>💬 Respuesta</summary>

    my_file = uproot.open("https://atlas-opendata.web.cern.ch/release/2016/MC/mc_105987.WZ.root")
</details>

> [!TIP]  
**2)** Carga el árbol denominado "mini" almacenado en el archivo de datos _.*root_. Imprime la cantidad de eventos en este árbol.
> [!END]

<details>
    <summary>💡 Clic aquí para obtener la pista 1</summary>
    Todos los datos se almacenan en el TTree 'mini'.
</details>


<details>
    <summary>💡 Clic aquí para obtener la pista 2</summary>
    Seleccione una rama (nombre) y genere su salida como una matriz.
</details>


<details>
    <summary>💡 Clic aquí para obtener la pista 3</summary>
    Mira la longitud del arreglo.
</details>

```python
my_tree = my_file[###]
eventNumber = my_tree[###].array(###)
print(###)
```

<details>
    <summary>💬 Respuesta</summary>
        
    my_tree = my_file["mini"]
    eventNumber = my_tree["eventNumber"].array(library="np")
    print(len(eventNumber))
</details>

> [!TIP]
**3)** También necesitaremos crear variables para el número máximo y mínimo de jets en un solo evento en este conjunto de datos para más adelante.
> [!END]

<details>
    <summary>💡 Clic aquí para obtener la pista 1</summary>
    El objeto que necesitas se llama "jet_n". Obtén un arreglo que es jet_n para cada evento.
</details>


<details>
    <summary>💡 Clic aquí para obtener la pista 2</summary>
    Numpy tiene dos funciones, .min() y .max(), que devuelven los valores mínimo y máximo de una matriz.
</details>


<details>
    <summary>💡 Clic aquí para obtener la pista 3</summary>
    ¡Recuerde que el primer evento es [0]!
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
    <summary>💬 Respuesta</summary>
        
    jet_n = my_tree["jet_n"].array(library="np")
    minimum = np.min(jet_n)
    maximum = np.max(jet_n)  
    print("Minimum number of jets:", minimum)
    print("Maximum number of jets;", maximum)
    
    jet_n_Event1 = jet_n[0]
    print("Number of jets in Event 1:", jet_n_Event1)
</details>


---

## Paso 2: Preparación para mostrar histogramas
Antes de poder mostrar cualquier histograma, debemos importar algunos módulos:
- `hist` es una biblioteca que maneja la generación y personalización de histogramas
- `Hist` es un módulo de `hist` que permite la generación de un histograma básico

```python
import hist
from hist import Hist
```

Para crear un histograma, usamos `Hist` y la función `hist.axis.Regular()`, que toma los argumentos `(bins, lower_limit, upper_limit, label)`. Por ejemplo, si queremos contar leptones (de 0 a 4), configuramos 5 contenedores, un límite inferior de 0 y un límite superior de 4:

```python
hist1 = Hist(hist.axis.Regular(5, -0.5, 4.5, label = "Number of leptons"))
```

El desplazamiento `-0.5` centra los contenedores en 0, 1, 2, 3 y 4. 

> [!IMPORTANT]  
No esperamos que se imprima ningún resultado de este paso; todo lo que estamos haciendo aquí es decirle a Python los detalles del histograma que planeamos completar.
> [!END]

### ✍🏻 Tu turno

**4)** Cree un histograma de plantilla llamado "Número de jets" para mostrar su gráfico.

<details>
    <summary>💡 Clic aquí para obtener la pista 1</summary>
    Utiliza el número mínimo (-0,5) y máximo de jets (9,5) para los límites del eje.
</details>


<details>
    <summary>💡 Clic aquí para obtener la pista 2</summary>
    Utiliza el número máximo de chorros para sus números de contenedores.
</details>

```python
my_hist = Hist(hist.axis.Regular(###, ###, ###, label = ###))
```

<details>
    <summary>💬 Respuesta</summary>
        
    my_hist = Hist(hist.axis.Regular(5, -0.5, 9.5, label = "Número de jets"))
</details>

---

## Step 3: Filling histograms
Para rellenar el histograma, comenzamos extrayendo la cantidad de leptones del TTree como una matriz numpy:

```python
lep_n = my_tree["lep_n"].array(library="np")
```

Luego, usamos `.fill()` para rellenar el histograma:

```python
hist1.fill(lep_n)
```

Para mostrar el histograma, lo dibujamos usando `.plot()` de `hist` y `plt.show()` de `matplotlib`:

```python
hist1.plot()
plt.show()
```

> [!NOTE]  
Más adelante, refinaremos el histograma aplicando "cortes", incluyendo solo eventos que cumplan con criterios específicos.
> [!END]

### ✍🏻 Tu turno

> [!TIP]  
**5)** Llene su histograma con el número de chorros en cada evento.
> [!END]

<details>
    <summary>💡 Clic aquí para obtener la pista 1</summary>
        Recuerda: ya hemos creado un histograma de plantilla.
</details>


<details>
    <summary>💡 Clic aquí para obtener la pista 2</summary>
        Los datos que buscas son "jet_n".
</details>

```python
my_hist.fill(###)
my_hist.###
plt.###
  
```

<details>
    <summary>💬 Respuesta</summary>
        
    my_hist.fill(jet_n)
    my_hist.plot()
    plt.show()
</details>

---

## Paso 4: Dibujar histogramas

Primero, vamos a crear un histograma básico con un título:

```python
hist2 = Hist(hist.axis.Regular(5, -0.5, 4.5, label="Number of leptons"))
hist2.fill(lep_n)
hist2.plot()
plt.title("Número de leptones en un conjunto de datos de 13 TeV")
plt.show()
```

Para comparar los conteos de leptones en diferentes conjuntos de datos, carguemos dos conjuntos de datos y representémoslos en el mismo eje:

```python
# Cargar conjuntos de datos adicionales
tr1 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363491.lllv.1largeRjet1lep.root:mini")
lep_n1 = tr1["lep_n"].array(library="np")

tr2 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363492.llvv.1largeRjet1lep.root:mini")
lep_n2 = tr2["lep_n"].array(library="np")
```
Ahora podemos crear y rellenar dos histogramas:

```python
# Create and fill histograms
hist1 = Hist(hist.axis.Regular(5, -0.5, 4.5, label="Number of leptons"))
hist1.fill(lep_n1)

hist2 = Hist(hist.axis.Regular(5, -0.5, 4.5, label="Number of leptons"))
hist2.fill(lep_n2)
```

Aquí, los eventos en cuestión produjeron leptones y sus neutrinos asociados. Tenemos curiosidad por saber cuántos leptones se produjeron en cada evento y cómo se comparan estos números, por lo que sería preferible superponer nuestros histogramas. Este es un proceso sencillo. Puede completar dos histogramas separados y trazarlos uno después del otro. Cada vez que ejecute `plot()`, dibujará el histograma sobre lo que ya está allí. Por supuesto, ejecute `plt.show()` para mostrar lo que ha dibujado.

Superpongamos ambos histogramas y mostremoslos juntos:

```python
# Plot both histograms
hist1.plot()
hist2.plot()
plt.title("Recuentos de leptones por evento para varios conjuntos de datos")
plt.legend(["Dataset 1", "Dataset 2"])
plt.show()
```

Para una versión apilada, combinamos y graficamos los histogramas directamente:

```python
histo_sum = hist1 + hist2
histo_sum.plot(histtype="fill")
plt.title("Recuentos de leptones apilados por evento")
plt.show()
```

También podemos usar la función `.stack()` de `hist`, para superponer o apilar histogramas, aunque primero necesitaremos prepararnos un poco.

Ahora necesitamos un "eje de categorías" o "cax", que funciona de manera similar a un diccionario. Su argumento $1^{st}$ es una lista de etiquetas de histograma y su argumento $2^{nd}$ es una etiqueta para el eje colectivo. En efecto, cada etiqueta de histograma es como una clave que vincula cada histograma con su nombre, color y posición.

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

¡Esto se ve igual que el resultado de nuestro método de superposición anterior, como debería! Este gráfico es ligeramente más perceptible. La leyenda añadida también ayuda.

### ✍🏻 Tu turno

> [!TIP]
**6)** Visualice varios histogramas del número de leptones en el mismo gráfico. Necesitará los siguientes archivos:
- 4 leptones - https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363490.llll.4lep.root
- 3 leptones - https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363491.lllv.1largeRjet1lep.root
> [!END]

<details>
    <summary>💡 Clic aquí para obtener la pista 1</summary>
        Necesitarás acceder a los datos de TTree para el número de leptones 2 veces por separado, 1 para cada conjunto de datos.
</details>


<details>
    <summary>💡 Clic aquí para obtener la pista 2</summary>
        Piensa en los números de contenedores y los límites para su eje y recuerde que tenemos 2 conjuntos de datos al generar el eje de categorías.
</details>


<details>
    <summary>💡 Clic aquí para obtener la pista 3</summary>
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
    <summary>💬 Respuesta</summary>

    # Cargue los conjuntos de datos con 4 leptones y 3 leptones
    tr1 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363490.llll.4lep.root:mini")
    lep_n1 = tr1["lep_n"].array(library="np")

    tr2 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363491.lllv.1largeRjet1lep.root:mini")
    lep_n2 = tr2["lep_n"].array(library="np")

    # Definir los ejes del histograma
    ax = hist.axis.Regular(6, -0.5, 5.5, name="Number of leptons")
    cax = hist.axis.StrCategory(["4 leptons", "3 leptons + neutrino"], name="dataset")

    # Crear y rellenar el histograma categorizado
    full_hist = Hist(ax, cax)
    full_hist.fill(lep_n1, dataset="4 leptons")
    full_hist.fill(lep_n2, dataset="3 leptons + neutrino")

    # Graficar el histograma apilado
    s = full_hist.stack("dataset")
    s.plot(histtype="fill")
    plt.title("Lepton Counts per Event for Two Datasets")
    plt.legend()
    plt.show()
</details>

---

## Paso 5: Normalización de histogramas
A menudo, nos interesan más las **proporciones** de nuestro histograma que el número absoluto de eventos que contiene (que puede cambiar según el conjunto de datos que utilice). Nuestro paso final será reescalar el eje y de nuestro histograma para que el total del histograma sea igual a 1. Esto se llama **normalización**.

Primero, extraemos los valores de los bins (alturas) como una matriz y calculamos la suma. Usamos la función `.sum()` en nuestra matriz de valores de bins para sumar los valores que contiene, luego creamos una nueva matriz que contiene cada uno de los valores de los bins originales divididos por la suma.

```python
arr = hist1.values()
arr_normalized = arr / arr.sum()
```

Creamos un nuevo histograma y establecemos sus valores bin en los valores normalizados:

```python
hist_normalized = Hist(hist.axis.Regular(5, -0.5, 4.5, flow=False, label="Numero of leptones"))
hist_normalized[...] = arr_normalized  # Assign normalized bin values
```

¡Veamos qué conseguimos!

```python
hist_normalized.plot(histtype="fill")
plt.title("Normalized Lepton Count")
plt.show()
```

Ahora demostremos que esto está normalizado: ¡ya hemos utilizado la función necesaria para hacerlo!

```python
print(hist_normalized.sum())
```

### ✍🏻 Tu turno
> [!TIP]
**6)** Normaliza tu histograma y vuelva a dibujarlo.
> [!END]

<details>
    <summary>💡 Clic aquí para obtener la pista 1</summary>
        Utiliza `.values()` para acceder a la altura de cada barra en el histograma.
</details>


<details>
    <summary>💡 Clic aquí para obtener la pista 2</summary>
       Utiliza `.sum` para encontrar la suma de estas alturas: deberá dividir la altura de cada barra por la suma.
</details>


<details>
    <summary>💡 Clic aquí para obtener la pista 3</summary>
        Redibuje su histograma y asigne nuevos valores a cada contenedor.
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
    <summary>💬 Respuesta</summary>
        
    # Obtenemos los valores bin del histograma original y normalicemos
    heights = my_hist.values()
    norm_heights = heights / heights.sum()

    # Creamos un nuevo histograma con los valores normalizados
    new_hist = Hist(hist.axis.Regular(5, -0.5, 4.5, label="Number of jets"))
    new_hist[...] = norm_heights  # Assign normalized values to bins

    # Graficamos el histograma normalizado
    new_hist.plot(histtype="fill")
    plt.title("Normalized Jet Count per Event")
    plt.show()
</details>

---

**¡Felicitaciones!** Has trabajado con datos reales de ATLAS como un verdadero físico de partículas.

Si quieres seguir aprendiendo a usar Python para analizar datos públicos de ATLAS, puedes consultar los [notebooks en el sitio web de ATLAS Open Data](https://opendata.atlas.cern/docs/category/analysis-notebooks).