# Laboratorio-1---Clasificador de Textos

Este proyecto es la solución al **Laboratorio 1** del curso **Programación Científica**.

El objetivo es implementar un clasificador de textos desde cero en Python. El programa clasifica textos de consulta (queries) basándose en una base de conocimiento de documentos ya clasificados, utilizando las técnicas de **TF-IDF** y **Similitud del Coseno**.

## Características Principales

* **Cálculo Manual de TF-IDF:** Implementación de las fórmulas de Frecuencia de Término (TF), Frecuencia Inversa de Documento (IDF) con ajuste `1+DF(t)`, y la matriz TF-IDF completa sin usar librerías externas.
* **Preprocesamiento de Texto:** El sistema normaliza el texto (minúsculas, elimina tildes, puntuación y caracteres especiales), tokeniza y elimina *stopwords*.
* **Clasificación K-NN:** Utiliza la Similitud del Coseno para encontrar los $K$ documentos más similares (vecinos más cercanos) y asigna la categoría de la consulta mediante una votación mayoritaria.
* **Diseño Modular:** El código está organizado en funciones claras  para cada parte del proceso (carga, preprocesamiento, construcción del modelo, vectorización de queries y clasificación).

## Requisitos

Este proyecto utiliza las siguientes librerías de Python:

* `numpy`: Para operaciones vectoriales eficientes, especialmente en el cálculo de la Similitud del Coseno.
* `unidecode`: Para la eliminación de tildes y caracteres no-ASCII durante el preprocesamiento.
* `scikit-learn`: Solo para el script `extraccion_dataset.py` que genera la base de conocimiento.

## Instrucciones

Para ejecutar el clasificador se deben instalar ciertas librerias en caso de que se encuntren instaladas en su equipo:

Dentro de PowerShell

* pip install numpy
* pip install unidecode
* pip install scikit-learn

# Paso Final
Se ejecuta el archivo clasificador_taller01.py