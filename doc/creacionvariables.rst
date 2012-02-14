=====================
Creacion de variables
=====================

La creación de variables es una operación equivalente a una expresión en una hoja de calculo. 
Partiendo de dos o más variables, y por medio de un conjunto de operadores compatibles, generamos una nueva variable. Cada registro tendrá como valor el resultado de aplicar la expresion a las variables fuente. Matemáticamente:

f(x,y)=z


Los operadores
--------------
El usuario podría usar cualquiera de los operadores lógicos y aritméticos que ofrece python. En esta lista estaría por ejemplo
Operadores aritméticos:
 +
 -
 *
 /

Operadores Logicos
 and
 or


El problema de los tipos
------------------------

¿Cómo sería el resultado de una expresión tipo "fecha"and"entero"? Existe ciertas combinaciones de tipos y operaciones que carecen de sentido. Por ello, y hasta que aborde el diseño con mayor profundidad, la interfaz impondrá las siguientes restricciones:
 -Si el resultado es de tipo x, solo podrán participar variables de tipo x en la expresión, salvo en el caso de los float que podrá actuar tambien el tipo entero
 -Los operadores lógicos solo podrán ser usados con tipos lógicos

