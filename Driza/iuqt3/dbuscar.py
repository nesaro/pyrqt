#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007  Néstor Arocha Rodríguez, Inmaculada Luengo Merino 

#This file is part of Driza.
#
#Driza is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#Driza is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Driza; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""Dialogo de búsqueda de texto"""

from Driza.iuqt3.ui.dbuscar import DialogoBuscar
from qt import QMessageBox, SIGNAL
import logging
LOG = logging.getLogger("Driza.iuqt3.dbuscar")

class DBuscar(DialogoBuscar):
    """Dialogo de busqueda 
    Busca cadenas de texto introducidas por el usuario en la tabla que este activa """

    def __init__(self, parent = None, name = None):
        """Inicializacion, llama a la funcion que define las conexiones"""
        DialogoBuscar.__init__(self, parent, name, 0, 0)
        self.__conexiones()

    #FUNCIONES PRIVADAS

    def __buscar(self):
        """ Funcion busca la cadena de texto introducida por el usuario en la tabla que este activa, seleccionando el primer registro válido que encuentre"""
        if not self.lineEdit1.text().latin1():
            return
        if self.parent().grid.currentPageIndex() == 0: 
            tablaactual = self.parent().grid.table1
        else: 
            tablaactual = self.parent().grid.table2
        fila = tablaactual.currentRow()
        columna = tablaactual.currentColumn()
        textoabuscar = self.lineEdit1.text().latin1()
        LOG.debug("Busqueda de " + textoabuscar)
        resultado = self.__buscarinterno(tablaactual, textoabuscar, fila, columna)
        if resultado:
            LOG.debug("Resultado encontrado en la primera columna")
            tablaactual.clearSelection()
            tablaactual.setCurrentCell(resultado[0], resultado[1])
            self.accept()
            return
        codigoretorno = QMessageBox.warning(self, 'Atencion', 'No he encontrado nada', '¿Continuar desde el principio?', 'Salir', '', 0, 1)
        if codigoretorno == 1:
            self.reject()
            return
        resultado = self.__buscarinterno(tablaactual, textoabuscar)
        if resultado:
            tablaactual.clearSelection()
            tablaactual.setCurrentCell(resultado[0], resultado[1])
            self.accept()
            return
        codigoretorno = QMessageBox.warning(self, 'Atencion', 'No he encontrado nada', 'Otra busqueda', 'Salir', '', 0, 1)
        if codigoretorno == 1:
            self.reject()
        else:
            self.lineEdit1.clear()
        return

    def __buscarinterno(self, tabla, texto, iniciox = 0, inicioy = 0):
        """Procedimiento interno que hace la busqueda efectiva"""
        n_fil = tabla.numRows()
        n_col = tabla.numCols()
        #Primera columna 
        for i in range(iniciox,n_fil):
            if (cmp(tabla.text(i,inicioy).latin1(), texto) == 0):
                return [i, inicioy]
        #Resto de columnas
        for j in range (inicioy+1, n_col):
            for i in range(n_fil):
                if (cmp(tabla.text(i,j).latin1(), texto) == 0):
                    return [i, j]
        return False


    def __conexiones(self):
        """Función que define las conexiones entre elementos de la interfaz y sus SLOTS"""
        self.connect(self.pushButton1, SIGNAL("clicked()"), self.__buscar)


