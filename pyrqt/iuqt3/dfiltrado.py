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

"""Dialogo de filtrado"""


from Driza.iuqt3.ui.dfiltrado import DialogoFiltro
from qt import SIGNAL
import logging
LOG = logging.getLogger("Driza.iu.dialogs.dfiltrado")


class DFiltrado(DialogoFiltro):
    """Dialogo que permite establecer el filtro"""
    
    def __init__(self, parent, interfazdatosusuario):
        DialogoFiltro.__init__(self, parent)
        self.__conexiones()
        self.__idu = interfazdatosusuario

    def __conexiones(self):
        """Función que define las conexiones entre elementos de la interfaz y sus SLOTS"""
        self.connect(self.pushButton1, SIGNAL("clicked()"), self.accept)
        self.connect(self.pushButton2, SIGNAL("clicked()"), self.reject)
        self.connect(self.pushButton3, SIGNAL("clicked()"), self.__insertar_simbolo_GT)
        self.connect(self.pushButton4, SIGNAL("clicked()"), self.__insertar_simbolo_LT)
        self.connect(self.pushButton5, SIGNAL("clicked()"), self.__insertar_simbolo_EQ)
        self.connect(self.pushButton6, SIGNAL("clicked()"), self.__insertar_simbolo_NE)
        self.connect(self.pushButton7, SIGNAL("clicked()"), self.__insertar_simbolo_AND)
        self.connect(self.pushButton8, SIGNAL("clicked()"), self.__insertar_simbolo_OR)
        self.connect(self.pushButton9, SIGNAL("clicked()"), self.__desactivar_filtro)
        self.connect(self.pushButton10, SIGNAL("clicked()"), self.__insertar_simbolo_XOR)
        self.connect(self.pushButton11, SIGNAL("clicked()"), self.__insertar_simbolo_LE)
        self.connect(self.pushButton12, SIGNAL("clicked()"), self.__insertar_simbolo_GE)
        self.connect(self.comboBox1, SIGNAL("activated (int)"), self.__insertar_variable)

    def showEvent(self, event):
        """Redefinicion de showEvent de qt"""
        self.myUpdate()
        DialogoFiltro.showEvent(self, event)

    def accept(self):
        """Aceptación del dialogo"""
        expresion = self.textEdit1.text().latin1()
        if not expresion:
            self.__desactivar_filtro()
        else:
            try:
                self.__idu.establecer_filtro(expresion)
            except SyntaxError:
                LOG.exception("Capturada excepcion en el manejo del filtro")
            else:
                self.parent().grid.myUpdate()
                DialogoFiltro.accept(self)

    def __insertar_simbolo_GT(self): 
        """Inserta el simbolo "mayor que" """
        self.textEdit1.insert(">")
    def __insertar_simbolo_LT(self): 
        """Inserta el simbolo "menor que" """
        self.textEdit1.insert("<")
    def __insertar_simbolo_EQ(self): 
        """Inserta el simbolo "igual" """
        self.textEdit1.insert("==")
    def __insertar_simbolo_NE(self): 
        """Inserta el simbolo "distinto de" """
        self.textEdit1.insert("!=")
    def __insertar_simbolo_AND(self): 
        """Inserta el simbolo "y" (lógico) """
        self.textEdit1.insert(" and ")
    def __insertar_simbolo_OR(self): 
        """Inserta el simbolo "o" (lógico) """
        self.textEdit1.insert(" or ")
    def __insertar_simbolo_XOR(self): 
        """Inserta el simbolo "o extendido" (lógico) """
        self.textEdit1.insert("^")
    def __insertar_simbolo_GE(self): 
        """Inserta el simbolo "mayor o igual" """
        self.textEdit1.insert(">=")
    def __insertar_simbolo_LE(self): 
        """Inserta el simbolo "menor o igual" """
        self.textEdit1.insert("<=")

    def __insertar_variable(self):
        """Inserta la variable seleccionada en el comboBox1"""
        self.textEdit1.insert(self.comboBox1.currentText())

    def __desactivar_filtro(self):
        """Desactiva el filtro"""
        self.__idu.borrar_filtro()
        self.parent().grid.myUpdate()
        DialogoFiltro.accept(self)

    def __actualizarcombovars(self):
        """Actualiza la caja de variables disponibles"""
        self.comboBox1.clear()
        for var in self.__idu.lista_tit():
            self.comboBox1.insertItem(var)

    def myUpdate(self):
        """Actualizacion del dialogo"""
        self.__actualizarcombovars()


