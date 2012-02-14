===========
Undo y Redo
===========

Implementación
--------------

Las operaciones de inserción o extracción de variables o registros seran objetos de una clase que herede de otra clase base llamada "transaccion"
Cada operacion (transaccion) tendra un método para volver al estado anterior. Por este motivo, en algunos casos almacenara ciertos datos (que había en esa posición anteriormente, por ejemplo).

Una pila almacenará las transacciones, permitiendo al usuario a través del undo y del redo recuperar un estado anterior
