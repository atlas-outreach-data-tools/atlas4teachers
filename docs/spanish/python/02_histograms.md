# Introducción a la histogramación
En física de partículas, analizar la enorme cantidad de datos requiere código informático en lugar de inspección manual. Esta guía cubrirá las técnicas básicas de histogramación para ayudarlo a visualizar datos de análisis de física de alta energía (HEP), específicamente la cantidad de leptones por evento en datos de bosones Z de 13 TeV.

Este recurso lo guiará a través de algunas técnicas informáticas básicas que se usan comúnmente en análisis de física de alta energía (HEP). Aprenderá a:

1. Interactuar con archivos de datos ATLAS
2. Crear, completar, dibujar y normalizar histogramas
    
## Paso 0: Configuración
El software que utilizaremos para analizar nuestros datos ATLAS se llama *uproot* y *hist*. Con `uproot`, podemos procesar grandes conjuntos de datos, realizar análisis estadísticos y visualizar nuestros datos utilizando *hist*. Los datos se almacenan en un formato llamado .root

```python
#Importamos las librerias
import uproot
import matplotlib.pyplot as plt
import numpy as np

print('✅ Librerias importadas')
```

## Paso 1: Carga de datos

Los datos de física se almacenan habitualmente en archivos `[algo].root`. Estos archivos utilizan una estructura TTree:
- El TTree organiza las mediciones en ramas, cada una de las cuales representa una variable (p. ej., energía, momento).
- Cada rama almacena la variable medida para cada evento en el conjunto de datos.