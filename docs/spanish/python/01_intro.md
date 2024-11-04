# Conceptos Básicos de Python
Ser capaz de programar es una habilidad esencial para un físico de partículas (o cualquier científico, de hecho). ¡Nuestros conjuntos de datos son simplemente demasiado grandes para procesarlos sin la ayuda de computadoras! Un físico de ATLAS generalmente usa una combinación de los lenguajes de programación C++ y Python para lograr todo, desde simular colisiones de protones hasta buscar bosones de Higgs.

Aquí revisamos algunos de los conceptos básicos de programación en Python. Lo haremos presentando una versión diluida e interactiva del tutorial de la [documentación oficial de Python](https://docs.python.org/3/tutorial/index.html). Para obtener más información sobre cualquier tema, deje que la documentación oficial de Python sea su primer punto de contacto. Le proporcionaremos enlaces a partes específicas del tutorial a medida que avancemos.

Python es ampliamente utilizado por principiantes e ingenieros de software por igual, tanto por negocios como por placer. ¡Puede ser divertido! Su nombre deriva de la serie de la BBC "Monty Python's Flying Circus" y se refiere a su fundador como un dictador benévolo vitalicio ([BDFL](https://docs.python.org/3/glossary.html)).

---

## Hola, mundo 
El programa ["¡Hola, mundo!"](https://es.wikipedia.org/wiki/Hola_mundo) es una tradición consagrada en Ciencias de la Computación que se respetará aquí. La idea de Hola Mundo es ilustrar los conceptos básicos de un lenguaje y verificar que el entorno de programación se haya instalado y configurado correctamente. Por lo tanto, para probar Python en esta app, intenta ejecutar el código de la siguiente celda ((el botón "run" en la esquina inferior derecha de la celda o `control + Enter` / `comando + Enter`))... si hace lo que esperas, ¡entonces estás listo!

```python
print("¡Hola, mundo!")
```

---

## Numbers, Strings, and Compound Data Types
>Siguiendo [An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html)
                
### Python as a calculator
¡Python es bueno en matemáticas! Ejecute los ejemplos de las siguientes celdas de código para ver qué hacen los operadores `+`, `-`, `*` y `/`, y descubra que tienen el efecto de sumar, restar, multiplicar y dividir.

```python
print(2+2)
```

```python
print((50 - 5*6) / 4)
```

Python también proporciona un práctico operador de potencia `**`.

```python
print(2**7) # Potencia
```

```python
print(4**(1/2)) # Usa potencias fraccionarias para calcular raíces
```

¿Observa los signos "#" que aparecen arriba? Esta notación le indica a Python que todo lo que aparece después del hashtag en esa misma línea no debe ejecutarse como un comando, sino que es solo un comentario.
                
¿Por qué algunos de los números producidos por estas operaciones tienen puntos decimales, mientras que otros no? Esto se debe a que tenemos aquí dos _tipos_ de números: los tipos `int` y los tipos `float`. El tipo `float` representa un [número de punto flotante](https://es.wikipedia.org/wiki/Coma_flotante)
y es la representación binaria formulaica de un número decimal en una computadora. El tipo `int` representa valores enteros.
> Si tiene suerte, nunca tendrá que preocuparse por la "precisión de punto flotante", pero puede ser una consideración importante, ya que en el pasado los errores aquí han causado [explosiones de cohetes](https://es.wikipedia.org/wiki/Ariane_5)!

Es posible asignar un valor a una variable utilizando el operador `=`.

```python
x = 4
print(x**2)
```

También contamos con los prácticos operadores in situ `+=`, `-=`, `*=` y `/=`. Estos realizan una operación en la variable a la que se aplican y luego reasignan esa variable al resultado de la operación.

```python
y = 10
y += 2
print(y)
```
    
### Strings
La `string` de Python es una cadena de caracteres entre comillas (`'...'` o `"..."`). Las cadenas pueden manipularse mediante las operaciones matemáticas
anteriores y se indexan como si fueran listas de caracteres.

```python
prefix = 'Py'
print(prefix + 'thon')
```

```python
print(3 * 'un' + 'ium')
```
    
```python
word = 'Python'
# Acceda al primer carácter de la cadena que está indexada por 0                  
print(word[0])
# Acceda al último carácter de la cadena que está indexada por -1
print(word[-1])
# Cortar la cadena desde el índice 1 (incluido) hasta el 5 (no incluido)
print(word[1:5])
```

### Tipos de datos compuestos
Una lista de Python es un tipo de datos compuesto (la lista en sí contiene valores de un tipo determinado) y mutable (es decir, se puede cambiar)para agrupar una secuencia de valores y ordenarlos de una determinada manera para que podamos encontrar cada entrada en la matriz por su índice.

```python
# A continuación se muestra una lista de ejemplo
nums = [1, 2, 3]
# Las listas son mutables
nums[0] = 4 #Al igual que las cadenas, la numeración de los elementos empieza en 0 no en 1
print(nums)
```

```python
# Las listas pueden contener diferentes tipos de datos.
nums += ['a']
print(nums)
```

```python
# Las listas se pueden 'dividir'
print(nums[1:3])
```

La función [incorporada](https://docs.python.org/3/library/functions.html) [`len(s)`](https://docs.python.org/3/library/functions.html#len) devuelve la longitud o la cantidad de elementos de una secuencia o colección `s`. Un excelente ejemplo de caso de uso es encontrar cuál de las palabras ['Llanfairpwllgwyngyllgogerychwyrndrobwllsantysiliogogogoch'](https://es.wikipedia.org/wiki/Llanfairpwllgwyngyll) y 'supercalifragilisticexpialidocious' es más larga.

```python
len_llanfair = len('Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch')
len_supercali = len('supercalifragilisticexpialidocious')

print(len_llanfair)
print(len_llanfair / len_supercali)
```

Como tipos de datos compuestos, también se utilizan con frecuencia [_tuplas_](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences) y [_diccionarios_](https://docs.python.org/3/tutorial/datastructures.html#dictionaries). ¿Puedes averiguar cómo funcionan a partir de las páginas vinculadas?

## Estructuras de control de flujo
En los fragmentos de código del ejemplo anterior (las operaciones matemáticas y de cadenas, y las manipulaciones de listas), programamos nuestros comandos para que se ejecuten línea por línea. Sería justo decir que estos programas de arriba a abajo son bastante aburridos. Se puede hacer que un programa muestre una [estructura de control de flujo](https://es.wikipedia.org/wiki/Estructuras_de_control) más complejo mediante el uso de [_declaraciones de estructuras de control de flujo_](https://docs.python.org/3/tutorial/controlflow.html).

Python tiene dos tipos de declaraciones de control de flujo: declaraciones condicionales y construcciones de bucle. Las declaraciones condicionales (`if`, `elif`, `else`) se utilizan para ejecutar bloques de código solo cuando se cumplen ciertas condiciones: Python solo hace lo que se menciona después de la declaración "if" si la declaración "if" es correcta; de lo contrario, no lo hace. Las construcciones de bucle se utilizan para ejecutar bloques de código una cierta cantidad de veces (`for`) o mientras se cumplan ciertas condiciones (`while`).

### Sentencias `if`

```python
x = 12 # Puedes cambiar el número
# Ejemplo de bloque condicional 'if'
if x < 0: #Python comprueba si esta es una declaración verdadera
    print('Introdujiste un número negativo')
elif x == 0: #Para 'else if', esta condición se verifica si la declaración 'if' es falsa
    print('Ingresaste cero')
else: #Todos los demás casos
    print('Ingresaste un número positivo')
```

¿Observa los espacios en blanco (específicamente, 4 espacios) que se encuentran frente a los bloques de código después de `if`, `elif` y `else`? A esto lo llamamos _indentación_ y le indica a Python qué líneas de código solo deben ejecutarse si la declaración del flujo de control es verdadera. Esto tiene la ventaja de que el código se vuelve fácilmente legible para los humanos. Por lo tanto, recuerde, indentación = 4 veces la barra espaciadora.

### Sentencias `for`

Las sentencias `for` en Python permiten iterar sobre los elementos de cualquier secuencia (como una lista o cadena) en orden.

¡Observe nuevamente la _sangría_!

```python
# Measure some strings in a `for` loop
words = ['gato', 'ventana', 'defenestrar', 'quark']
for w in words:
    print(w, len(w))
```
Junto con las instrucciones `for`, la función incorporada [`range()`](https://docs.python.org/3/library/stdtypes.html#range) suele ser útil. Devuelve un objeto de rango, construido al llamar a `range(stop)` o `range(start, stop[, step])`, que representa una secuencia de números que va desde `start` (0 por defecto) hasta `stop` en pasos de `step` (1 por defecto).

```python
# Ejemplo de bucle 'for' sobre un rango que inserta elementos en una lista
items = []
for i in range(10):
    items.append(i) #.append() es otra forma útil de agregar algo al final de una lista de Python
print(items)
```

### Sentencias `while`
Un bucle `while` se ejecuta mientras la `condición` sea verdadera. La celda a continuación es un ejemplo de un bucle `while`:

```python
#Un uso interesante del bucle while: calcula la serie de Fibonacci
a, b = 0, 1
while a < 1000:
print(a, end=' ')
a, b = b, a + b
```

Si la condición siempre es verdadera, entonces tienes un bucle infinito, un bucle que nunca terminará. En el app, puedes interrumpir  haciendo clic en el botón de "stop" arriba a la derecha.

## Funciones
¿Qué sucede si queremos usar un bloque de código varias veces y en diferentes lugares? Simplemente podríamos copiar y pegar ese bloque de código cada vez que queramos usarlo, ¡pero hay una forma mejor! Podemos envolver el bloque de código en una [_función_](https://docs.python.org/3/tutorial/controlflow.html#defining-functions) y "llamar" a esa función tantas veces como queramos.

Para crear una función en Python, indicamos dónde está el comienzo y el final de los cálculos dentro de la función usando sangría (como para `if/else`, `for` y `while` arriba).

Estas son las partes importantes de las funciones de Python:

- Comienzan con `def`, luego viene el nombre que ha elegido para la función y luego, entre paréntesis, el nombre de la variable de entrada y luego dos puntos.
- Las siguientes líneas, donde realmente haces que la función calcule algo, deben comenzar con 4 espacios en blanco.
- Le dices explícitamente a la función cuál es el valor de salida con `return` y luego el nombre de la salida.

En la sección anterior, calculamos todos los términos de la secuencia de Fibonacci que son menores que 1000. Al hacer una función `fibonacci(n)` de nuestro código de Fibonacci, podríamos proporcionar el límite superior como un parámetro `n` de la función y calcular la serie hasta muchos valores diferentes de `n`.

```python
def fibonacci(n):
    '''Calcula e imprime los términos de la serie de Fibonacci
    que sean menores que `n`.'''
    a, b = 0, 1
    while a < n:
    print(a, end=' ')
    a, b = b, a + b
    print()

    return

    # Imprime los términos de la serie de Fibonacci que sean menores que n = 10
    fibonacci(10)
```

¿Observaste la declaración `return` en la definición de la función `fibonacci`? ¡No hizo nada! Pero, en general, podemos usar la declaración `return` para devolver (es decir, para _pasar_) información desde el interior de una función hacia el exterior. Considera la siguiente actualización de la función `fibonacci` original. Devuelve una lista de los términos de la serie de Fibonacci, ¡lo que puede ser más útil que imprimirlos!

```python
def return_fibonacci_series(n):
    '''Calcula los términos de la serie de Fibonacci
    que son menores que `n`, devolviendo una lista del resultado.'''

    # Crea una lista llamada 'series' para almacenar los términos
    series = []

    # Calcula los términos hasta n
    a, b = 0, 1
    while a < n:
    series.append(a)
    a, b = b, a + b

    # Devuelve la serie
    return series
```

Vamos a comprobar si esta función se comporta como esperamos. Para ello, la llamaremos con `n = 100` y luego realizaremos una operación sobre la lista devuelta.

```python
result = return_fibonacci_series(100)

# Imprimir el resultado...
print(result)

# Invertir el resultado e imprimirlo, sólo por diversión...
reversed_result = list(reversed(result))
print(reversed_result)

# ¡Haz lo que quieras con la serie de Fibonacci aquí!
# . . .
```

Cuando imprimimos la serie de Fibonacci en un bucle `for`, terminamos imprimiendo cada nueva serie muchas veces. Al utilizar la lista devuelta de la función de Fibonacci actualizada, ¡ahora podemos imprimir la serie sólo si difiere de la serie anterior! El siguiente ejemplo ilustra cómo implementar esto:

```python
# Variable para almacenar el término más grande actualmente
largest_term = -1

for n in range(10000):
    # Llamar a la función de Fibonacci actualizada que devuelve una lista de términos
    series = return_fibonacci_series(n)

    # Si la serie contiene términos (`if series` verifica que `series` no esté vacío = [])
    if series:

        # Si el término más grande es más grande que el término más grande visto hasta ahora
        series_largest_term = series[-1]
        if series_largest_term > largest_term:

            # Imprimir la serie
            for term in series:
                print(term, end=' ')
            print()

            # Actualizar el término más grande
            largest_term = series_largest_term
```

En este último ejemplo, puedes ver que las técnicas de programación que hemos aprendido en este cuaderno nos permiten escribir algunos programas realmente complejos.

---

## Módulos
Hemos estado escribiendo pequeños fragmentos de código descartable y ejecutándolos, antes de pasar a otra cosa y olvidarnos de ellos. Cuando se trata de escribir un programa más elaborado, es más conveniente poner el código en un archivo. Cuando un archivo se llena con definiciones de Python, se convierte en un [_módulo_][módulo] que se puede _importar_ desde otros archivos que hablan Python de modo que se pueda utilizar su contenido.

El enfoque orientado a módulos para el desarrollo de software tiene el efecto de mantener el código organizado, pero lo que es más importante, facilita el intercambio de código. En el mundo del software libre y de código abierto, gran parte del código que necesitará escribir ya se ha escrito y está disponible para su uso. Rara vez es necesario programar todo desde cero.

Las bibliotecas más populares incluyen:
* [`numpy`](https://numpy.org/) para computación numérica
* [`matplotlib`](https://matplotlib.org/) para visualización de datos
* [`tensorflow`](https://www.tensorflow.org/) para aprendizaje automático
* [`pandas`](https://pandas.pydata.org/) para manipulación de datos

Estas bibliotecas de módulos están ahí para usarse sin costo alguno. Veamos las dos primeras con más detalle.

### El módulo `numpy`
Si queremos hacer alguna operación matemática más complicada (como solemos hacer en física), podemos utilizar un paquete llamado `"numpy"`, que es una biblioteca muy potente y de uso frecuente para operaciones numéricas. Comencemos importándolo.

```python
import numpy as np
```
También podríamos escribir simplemente "import numpy", pero entonces tendríamos que escribir cada vez que quisiéramos utilizar una función de numpy "numpy.nombre_de_la_funcion", mientras que con "as np" nos ahorramos un poco de escritura y solo tenemos que escribir "np.nombre_de_la_funcion".

`numpy` nos proporciona formas alternativas de realizar operaciones, así como su propia versión de listas llamadas "arrays".

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
Los arreglos `numpy` se pueden indexar y dividir de la misma manera que las listas normales:

```python
print(arr[4])
print(arr[-1])
print(arr[0:3])
```

También tienen su propia versión de la función `range()`: `np.arange()`.

```python
print(np.arange(2, 2.8, 0.1)) #(empieza, termina, [paso])
```
**Pero**, `numpy` también tiene algunos comandos muy útiles que no están disponibles en por defecto Python.

Un ejemplo es `np.zeros` que crea un arreglo lleno de ceros (y tendrá tantos ceros como los números que proporciones entre paréntesis).

```python
print(np.zeros(5))
```
Si en cambio quieres un arreglo llena de unos:

```python
print(np.ones(3))
```
Para crear un arreglo con, digamos, 5 números espaciados linealmente entre los valores 1 y 10:

```python
print(np.linspace(1, 100, 5))
```

Para crear un arreglo con 5 números espaciados logarítmicamente entre los valores 10$^1$ y 10$^{10}$:

```python
print(np.logspace(1, 10, 5))
```

A diferencia de las listas en Python, los arreglos `numpy` se pueden manipular muy fácilmente. Digamos, por ejemplo, que tienes un arreglo con algunos números y quieres multiplicar cada número de la matriz por un factor de 2. Primero creamos la matriz:

```python
arr = np.arange(2,12)
print(arr)
```

Luego creamos el nuevo arreglo con los valores multiplicados:

```python
newarr = 2 * arr
print(newarr)
```
¡Fácil!

### El módulo `matplotlib`
Una de las ventajas de Python es que es bastante fácil tener los datos (por ejemplo, las mediciones) organizados en matrices y luego representarlos gráficamente en un gráfico de vista agradable.

Para representar gráficamente en Python, utilizamos la biblioteca `matplotlib.pyplot`. Como antes, cargaremos la biblioteca con un atajo conveniente para que tengamos que escribir menos más adelante:
```python
import matplotlib.pyplot as plt
```
Ahora definamos algunos datos como lo que irá en el eje X de nuestro gráfico, y algunos otros datos que irán en el eje Y.

Digamos que nuestros valores x son números enteros entre 0 y 10:

```python
x = np.arange(0, 10)
print(x)
```
Y digamos que nuestros valores y son los valores x elevados a la segunda potencia:

```python
y = x**2
print(y)
```
Ahora queremos graficar los datos x e y. Primero le indicamos a Python que cree una nueva figura con el comando `plt.figure()`; por ahora no hace mucho, pero puede volverse importante cuando estás creando múltiples figuras y quieres comenzar un gráfico nuevo cada vez y no superponerlo en el anterior. Después de crear la figura vacía, graficamos los datos x e y con el comando `plt.plot`.

```python
plt.figure()
plt.plot(x,y)
plt.show()
```

¡Ahora podemos ver nuestro gráfico! Sin embargo, ahora mismo no parece muy interesante. Agreguemos algunas líneas adicionales para cambiar eso:

```python
plt.plot(x, y, 'o', label='y') # esto traza solo marcas circulares, pero no líneas
plt.plot(x, 1.1*y, '-o', label='1.1y') # esto traza marcadores y líneas
plt.plot(x, 0.9*y, '--', label='0.9y') # esto traza líneas discontinuas en lugar de una línea continua
plt.axis([3, 10, 0, 100]) # esto amplía una parte determinada del gráfico (x_start, x_end, y_start, y_end)
plt.xlabel('x axis') # Agrega una etiqueta de eje x
plt.ylabel('y axis') # Agrega un eje y etiqueta
plt.title('Mi gráfico') #Agrega un título a tu gráfico
plt.legend(loc='best') #Agrega una leyenda, en la ubicación que matplotlib considere mejor
```

Como puedes ver, matplotlib elige automáticamente un nuevo color si trazas algo nuevo en el mismo gráfico. También puedes controlar directamente qué color quieres usar con estas abreviaturas:

    'b' = azul
    'g' = verde
    'r' = rojo
    'y' = amarillo
    'c' = cian
    'm' = magenta
    'k' = negro
    'w' = blanco

Y algunos marcadores diferentes:

    'o' para un círculo grande
    '.' para un círculo pequeño
    's' para un cuadrado
    '*' para una estrella
    '+' para un signo más
y muchos más

Y hay varios estilos de línea para usar:

    '-' para una línea sólida
    '--' para una línea discontinua
    ':' para una línea de puntos
    '-.' para una línea de puntos y guiones

y solo el símbolo del marcador, pero ningún símbolo para que la línea tenga solo los marcadores.

Aquí hay un ejemplo de cómo usarlo:

```python
plt.figure(figsize=(8,6))
plt.plot(x, 0.1*y, 'b-')
plt.plot(x, 0.2*y, 'g-o')
plt.plot(x, 0.3*y, 'y--*')
plt.plot(x, 0.4*y, 'r.')
plt.plot(x, 0.5*y, 'm-.')
plt.plot(x, 0.6*y, 'ws')
plt.plot(x, 0.7*y, 'k:+')
plt.xlabel('eje x') #Agrega una etiqueta de eje x
plt.ylabel('eje y') #Agrega una etiqueta de eje y
plt.title('Otro gráfico') #Agrega una Título de tu trama
plt.show()
```

---

## Conclusión

En este cuaderno, hemos pasado muy rápidamente de cero a sesenta en la codificación en Python. Hemos estado trabajando en un cuaderno Jupyter donde podemos ejecutar código de forma interactiva y escribir texto para anotar lo que estamos haciendo. Después de decir "¡Hola, mundo!", aprendimos a hacer matemáticas con Python y a usar cadenas y tipos de datos compuestos. Al usar declaraciones de flujo de control, vimos que podemos escribir programas bastante complejos, que podemos organizar en funciones y módulos para mayor comodidad y capacidad de compartir.

En todas estas características, fuimos breves para poder pasar rápidamente a temas más interesantes. Con ese fin, omitimos o pasamos por alto muchos detalles y tecnicismos: ¡hay mucho más que aprender! Pero aprender de forma independiente cómo hacer algo nuevo puede ser parte de la diversión y, sin duda, es parte del trabajo. Al programar, es normal no saber inmediatamente cómo hacer algo.

> [!IMPORTANT]
Al usar Python, eres parte de una gran comunidad global. Esto significa que el internet está lleno de consejos sobre cómo escribir bien el código Python. Si describes tu problema a un motor de búsqueda, la mayoría de las veces obtendrá una solución de inmediato. ¡Aprovecha lo que otros Pythonistas saben sobre Python!
> [!END]

¡Buena suerte analizando los datos abiertos de ATLAS! Esperamos que esta introducción a la programación en Python le resulte útil. 

Si quieres continuar aprendiendo como se usa Python en física experimental de partículas,te recomendamos revisar el tab de "Introducción a la histogramación" en esta misma página.