========
Filtrado
========

Objetivos e implementación
--------------------------

El filtrado es una función que, para un conjunto de valores de entrada, devuelve un subconjunto de estos.

Ejemplo:
    (a b c d) -> (a d)

En driza interesa que los resultados no incluyan algunos valores. Por ejemplo, si tenemos un estudio de las notas de clase, y queremos excluir a la gente que ha repetido, necesitaremos un filtro

La implementación consiste en usar una variable como filtro. Dado un registro, si la variable tiene un valor nulo, dicho registro será descartado. Por la naturaleza del lenguaje python, es suficiente con almacenar el objeto de la variable que actuará como filtro. Para desactivar los filtros, se almacenará el valor *None*
