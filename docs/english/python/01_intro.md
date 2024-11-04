# Python Basics
Being able to code is an essential skill for a Particle Physicist (or any scientist, for that matter). Our datasets are simply too large to process without the assistance of computers! An ATLAS Physicist typically uses some combination of the C++ and Python programming languages to accomplish everything from simulating proton-proton collisions to searching for Higgs bosons.

Here we review some of the basics of coding in Python.  We will do this by presenting a diluted and interactive version of the tutorial of the [official Python documentation](https://docs.python.org/3/tutorial/index.html). For more information on any topic, let the official Python documentation be your first port of call. We will link to specific parts of the tutorial as we go along.

Python is extensively used by beginners and software engineers alike, for both business and pleasure.  It can be fun!  It is named after the BBC series "Monty Python's Flying Circus" and refers to its founder as a Benevolent Dictator For Life ([BDFL](https://docs.python.org/3/glossary.html)).

---

## Hello, world         
The ["Hello, World!" programme](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) is a time-honoured tradition 
in Computer Science which will be respected here.  The idea of Hello World is to illustrate the basics of a language and 
to verify that the coding environment has been properly installed and set up.  So to test Python in this app, have a 
go at running the code of the next cell (the "run" button in the the lower right corner of the cell or `control + Enter` / `command + Enter`)...if it does what you expect, then you are good to go!

```python
print("Hello, World!")
```

---

## Numbers, Strings, and Compound Data Types
>Following [An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html)
                
### Python as a calculator
Python is good at maths! Run the examples of the following code cells to see what the operators `+`, `-`, `*` and `/` do, to find that they have the effect of addition, subtraction, multiplication, and division.

```python
print(2+2)
```

```python
print((50 - 5*6) / 4)
```
Python additionally provides a convenient power operator `**`.

```python
print(2**7) # Power
```

```python
print(4**(1/2)) # Use fractional powers to calculate roots
```

Notice the `#`'s above? This notation tells Python that everything after the hashtag in that same line should not be executed as a command, but it is just a comment.
                
Why do some of the numbers produced by these operations have decimal points, while others do not?  It is because we have here two _types_ of numbers: `int` types and `float` types.  The `float` type represents a [floating point number](https://en.wikipedia.org/wiki/Floating-point_arithmetic) and is a computer's formulaic binary representation of a decimal number.  The `int` type represents integer values.
> If you are lucky, you will never have to worry about 'floating point precision', but it can be a significant consideration, with errors here having in the past caused [rockets to explode](http://www-users.math.umn.edu/~arnold/disasters/ariane.html)!

It is possible to assign a value to a variable using the `=` operator.          

```python
x = 4
print(x**2)
```

We have also the handy in-place operators `+=`, `-=`, `*=` and `/=`. These perform an operation on the variable they are being applied to, 
then reassigning that variable to the result of the operation.

```python
y = 10
y += 2
print(y)
```
    
### Strings
The Python `string` is a string of characters enclosed in quotation marks (`'...'` or `"..."`).  Strings may be operated upon by the above 
mathematical operations and are indexed as if they were lists of characters!

```python
prefix = 'Py'
print(prefix + 'thon')
```

```python
print(3 * 'un' + 'ium')
```
    
```python
word = 'Python'
# Access the first character of the string which is indexed by 0                    
print(word[0])
# Access the last character of the string which is indexed by -1
print(word[-1])
# Slice the string from index 1 (inclusive) to 5 (not inclusive)
print(word[1:5])
```

### Compound Data Types
A Python list is a mutable (i.e. you can change it), compound (the list itself holds values of a certain type) data type for grouping together a sequence of values, and have them ordered in a certain way so that we can find each entry in the array by its "house number" or index.

```python
# Here is an example list
nums = [1, 2, 3]
# Lists are mutable
nums[0] = 4 #Like strings, the numbering of the elements starts at 0, not 1
print(nums)
```

```python
# Lists can contain different data types
nums += ['a']
print(nums)
```

```python
# Lists can be 'sliced'
print(nums[1:3])
```

The [built-in](https://docs.python.org/3/library/functions.html) function [`len(s)`](https://docs.python.org/3/library/functions.html#len) returns the length of, or number of items in, a sequence or collection `s`.  One excellent example use case is to find which of the words ['Llanfairpwllgwyngyllgogerychwyrndrobwllsantysiliogogogoch'](https://en.wikipedia.org/wiki/Llanfairpwllgwyngyll) and 'supercalifragilisticexpialidocious' is longer.

```python
len_llanfair = len('Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch')
len_supercali = len('supercalifragilisticexpialidocious')

print(len_llanfair)
print(len_llanfair / len_supercali)
```

As compound data types, [_tuples_](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences) and [_dictionaries_](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) are also frequently used.  Can you figure out what they do from the linked pages?  Feel free to make new code cells here to explore.

## Control Flow 
In the preceding example code snippets (the mathematical and string operations, and list manipulations), we programmed our commands to be executed line-by-line.  It would be fair to say that these top-to-bottom programmes are quite dull.  A programme may be made to exhibit a more complex [control flow](https://en.wikipedia.org/wiki/Control_flow) by use of [_control flow statements_](https://docs.python.org/3/tutorial/controlflow.html).  

Python has two types of control flow statements - conditional statements and loop constructs.  Conditional statements (`if`, `elif`, `else`) are used to execute blocks of code only when certain conditions are met - Python only does the thing mentioned after the "if" statement if the "if" statement is correct, otherwise it doesn't do it.  Loop constructs are used to execute blocks of code some number of times (`for`) or while certain conditions are met (`while`).

### `if` Statements

```python
x = 12 #You can change the integer here
# Example conditional 'if' block
if x < 0: #Python checks if this is a true statement
    print('You entered a negative number!')
elif x == 0: #Short for 'else if', this condition is checked if the 'if' statement is false
    print('You entered zero')
else: #All other cases
    print('You entered a positive number')
```

Notice the whitespace (specifically, 4 spaces) in front of the code blocks after `if`, `elif` and `else`? We call this _indentation_, and it tells Python which lines of code should only be executed if the control flow statement is true. This has the advantage that the code becomes easily readable for humans. So, remember, indent = 4 times space bar.|

### `for` Statements

`for` statements in Python allow you to iterate over the items of any sequence (like a list or string) in order.

Notice again the _indentation_!

```python
# Measure some strings in a `for` loop
words = ['cat', 'window', 'defenestrate', 'quark']
for w in words:
    print(w, len(w))
```
In conjunction with `for` statements, the built-in [`range()`](https://docs.python.org/3/library/stdtypes.html#range) function is often useful.  It returns a range object, constructed by calling `range(stop)` or `range(start, stop[, step])`, that represents a sequence of numbers that goes from `start` (0 by default) to `stop` in steps of `step` (1 by default).

```python
# Example 'for' loop over a range that pushes items onto a list
items = []
for i in range(10):
    items.append(i) #.append() is another useful way to add something to the end of a python list
print(items)
```

### `while` Statements
A `while` loop executes for as long as `condition` is true. The cell below is an example of a `while` loop:

```python
#An interesting use of the while loop: calculate the Fibonacci series!
a, b = 0, 1
while a < 1000:
    print(a, end=' ')
    a, b = b, a + b
```

If the condition is always true, then you have an infinite loop - a loop that will never end. In the apps, you can interrupt code running by clicking the stop button in the upper right corner.

## Functions
What if we want to use some block of code multiple times and in different places?  We could simply copy-and-paste that block of code every time we want to use it, but there is a better way!  We can wrap the block of code in a [_function_](https://docs.python.org/3/tutorial/controlflow.html#defining-functions) and 'call' that function as many times as we like.

To create function in Python we indicate where the beginning and end of the calculations inside the function is using indentation (like for `if/else`, `for` and `while` above).

Here are the important parts of Python functions:

 - They start with `def`, then comes the name you have chosen for the function, and then in round brackets the name(s) of the input variable(s), then a colon.
 - The next lines, where you actually have the function calculate something, needs to start with 4 white spaces.
 - You explicitly tell the function which value is the output value with `return` and then the name of the output.

In the preceding section, we calculated all the terms of the Fibonacci sequence that are less than 1000.  By making a function `fibonacci(n)` of our Fibonacci code, we could provide the upper limit as a parameter `n` of the function and calculate the series up to many different values of `n`!

```python
def fibonacci(n):
    '''Calculate and print out the terms of the Fibonacci series 
    that are less than `n`.'''
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
    print()
    
    return

# Print the terms of the Fibonacci series that are less than n = 10
fibonacci(10)
```

Did you notice the `return` statement in the definition of the `fibonacci` function?  It did nothing!  But we can in general use the `return` statement to return (i.e. to _pass_) information from inside a function to outside.  Consider the following update of the original `fibonacci` function. It returns a list of the terms of the Fibonacci series, which may be more useful than printing them!

```python
def return_fibonacci_series(n):
    '''Calculate the terms of the Fibonacci series 
    that are less than `n`, returning a list of the result.'''
    
    # Make a list called 'series' to store the terms
    series = []
    
    # Calculate the terms up to n
    a, b = 0, 1
    while a < n:
        series.append(a)
        a, b = b, a + b
        
    # Return the series
    return series
```
Let's check to see if this function behaves as we would expect.  We will do that by calling it with `n = 100`, and then by operating on the returned list.

```python
result = return_fibonacci_series(100)

# Print the result...
print(result)

# Reverse the result and print it, just for fun...
reversed_result = list(reversed(result))
print(reversed_result)

# Do anything you like with the Fibonacci series here!
# . . .
```

When we printed the Fibonacci series in a `for` loop, we ended up printing each new series many times.  By using the returned list of the updated Fibonacci function, we could now print the series only if it differs from the previous series! The next example illustrates how to implement this:

```python
# Variable to hold the currently-largest term
largest_term = -1

for n in range(10000):
    # Call the updated Fibonacci function that returns a list of terms
    series = return_fibonacci_series(n)
    
    # If the series contains terms (`if series` checks that `series` is not empty = [])
    if series:
        
        # If the largest term is larger than the largest term seen so far
        series_largest_term = series[-1]
        if series_largest_term > largest_term:
            
            # Print the series
            for term in series:
                print(term, end=' ')
            print()
            
            # Update the largest term
            largest_term = series_largest_term
```

So you see in this last example that the coding techniques that we have learned in this notebook enable us to write some really quite complex programmes!

---

## Modules
We have been writing small snippets of disposable code and executing them, before moving on and forgetting about them.  When it comes to writing a more elaborate programme, it is more convenient to put your code in a file.  When a file is populated with Python definitions, it becomes a [_module_][module] which can be _imported_ from other Python-speaking files such that its content may be used.

The module-oriented approach to software development has the effect of keeping your code organsied, but more importantly facilitates code-sharing.  In the world of open-source and free software, much of the code you will ever need to write has already been written and is available to use!  One rarely has to code everything from scratch. 

Popular libraries include
* [`numpy`](https://numpy.org/) for numerical computing
* [`matplotlib`](https://matplotlib.org/) for data visualisation
* [`tensorflow`](https://www.tensorflow.org/) for machine learning
* [`pandas`](https://pandas.pydata.org/) for data manipulation

These libraries of modules are there to be used at no cost. Let's look at the first two in more detail.

### The `numpy` module
If we want to do some more complicated mathematical operation (as we often do in physics), we can use a package called `"numpy"`, which is a very powerful and often-used library for numerical operations. Let's begin by importing it.

```python
import numpy as np
```

We could also just write "import numpy", but then we would have to type every time we want to use a function from numpy "numpy.name_of_function", whereas with the "as np" we save ourselves a bit of typing and just have to write "np.name_of_function".

`numpy` provides us with alternative ways of performing operations, as well as its own version of lists called "arrays".

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
`numpy` arrays can be indexed and sliced the same way as regular lists:
```python
print(arr[4])
print(arr[-1])
print(arr[0:3])
```

`numpy` arrays also have their own version of the `range()` function - `np.arange()`.

```python
print(np.arange(2, 2.8, 0.1)) #(start, stop, [step])
```
**But**, `numpy` also has some very useful commands which are not available by default in python.

One example is `np.zeros` which creates an array filled with zeros (and it will have as many zeros as the numbers you give in brackets).

```python
print(np.zeros(5))
```
If you want instead an array filled with ones:

```python
print(np.ones(3))
```
To create an array with, say, 5 linearly spaced numbers between the values 1 and 10:

```python
print(np.linspace(1, 100, 5))
```

To create an array with 5 logarithmically spaced numbers between the values 10$^1$ and 10$^{10}$:

```python
print(np.logspace(1, 10, 5))
```

Unlike lists in Python, `numpy` arrays can be manipulated very easily!! Say, for example, you have an array with some numbers in it, and you want to multiply every number in the array by a factor of 2. First we create the array:

```python
arr = np.arange(2,12)
print(arr)
```

Then we make the new array with the multiplied values:

```python
newarr = 2 * arr
print(newarr)
```
Easy!

### The `matplotlib` module
One of the strengths of python is that it is quite easy to have your data (say, your measurements) organized in arrays and then plot those in a nice viewgraph.

To do plotting in python, we use the library `matplotlib.pyplot`. Like before, we'll load the library with a convenient shortcut so that we have to do less typing further down the road:
```python
import matplotlib.pyplot as plt
```
Now let's define some data as the stuff that will go on the X axis of our plot, and some other data that will go on the Y axis.

Let's say our x values are integers between 0 and 10:

```python
x = np.arange(0, 10)
print(x)
```
And let's say our y values are the the x values to the power of two:

```python
y = x**2
print(y)
```
Now we want to plot the x and y data. First we tell python to make a new figure with the `plt.figure()` command; for now it doesn't do much, but it can become important when you are making multiple figures and you want to start a fresh plot eachtime and not overplot on the old one. After making the empty figure, we plot the x and y data with the `plt.plot` command.

```python
plt.figure()
plt.plot(x,y)
plt.show()
```

Now we can see our plot! However, right now it doesm't look very interesting  - let's add a few extra lines to change that:

```python
plt.plot(x, y, 'o', label='y') # this plots only circular markes, but no lines
plt.plot(x, 1.1*y, '-o', label='1.1y') # this plots markers and lines
plt.plot(x, 0.9*y, '--', label='0.9y') # this plots a dashed lines instead of a solid line
plt.axis([3, 10, 0, 100]) # this zooms into a certain part of the plot (x_start, x_end, y_start, y_end)
plt.xlabel('x axis') #Adds an x-axis label
plt.ylabel('y axis') #Adds a y-axis label
plt.title('My plot') #Adds a title to your plot
plt.legend(loc='best') #Adds a legend, in the location matplotlib thinks is best
```

As you can see, matplotlib automatically chooses a new colour if you plot a new thing into the same plot. You can also directly control which colour you want to use with these abbreviations:

    'b' = blue
    'g' = green
    'r' = red
    'y' = yellow
    'c' = cyan
    'm' = magenta
    'k' = black
    'w' = white

And some different markers:

    'o' for a big circle
    '.' for a small circle
    's' for a square
    '*' for a star
    '+' for a plus sign
    and many more

And there are various line styles to use:

    '-' for a solid line
    '--' for a dashed line
    ':' for a dotted line
    '-.' for a dash-dotted line

and just the marker symbol, but no symbol for the line to have only the markers.

Here is an example how to use that:

```python
plt.figure(figsize=(8,6))
plt.plot(x, 0.1*y, 'b-')
plt.plot(x, 0.2*y, 'g-o')
plt.plot(x, 0.3*y, 'y--*')
plt.plot(x, 0.4*y, 'r.')
plt.plot(x, 0.5*y, 'm-.')
plt.plot(x, 0.6*y, 'ws')
plt.plot(x, 0.7*y, 'k:+')
plt.xlabel('x axis') #Adds an x-axis label
plt.ylabel('y axis') #Adds a y-axis label
plt.title('Another plot') #Adds a title to your plot
plt.show()
```

---

## Conclusion 
We have very quickly gone from zero to sixty at coding in Python!  We have been working in a Jupyter notebook where we can run code interactively and write text to annotate what we are doing.  After saying `'Hello, World!'`, we learned how to do maths with Python and how to use strings and compound data types.  By using control flow statements, we saw that we can write quite complex programmes, which we can organise into functions and modules for convenience and shareability!

On all of these features, we were brief so that we can get on to more interesting topics quickly.  To that end, we omitted or glossed over many details and many technicalities - there is much more to learn!  But independently learning how to do something new can be a part of the fun and is certainly a part of the job.  When coding, it is normal to not immediately know how to do something.

> [!CAUTION]
In using Python, you are a part of a large global community.  This means that the internet is full of advice on how to write Python code well.  Describing your problem toa search engine more often than not brings up a solution straight away.  Make use of what other Pythonistas know about Python!
> [!END]

Good luck analysing ATLAS Open Data! We hope that this introduction to coding in Python will serve you well.

If you want to continue learning how Python is used in experimental particle physics, we recommend checking out the "Introduction to Histogramming" tab on this page.
