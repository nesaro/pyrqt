#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007  Néstor Arocha Rodrguez, Inmaculada Luengo Merino
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

"""Todas aquellas clases que heredan directamente de algun widget de Qt y que pretenden aumentar su funcionalidad"""

from qt import Qt, QButtonGroup, QGridLayout, QComboBox, QListBox, QRect

class WidgetLista:
    """Clase base de los widgets que se gestionan una lista"""

    def __init__(self, lista = None):
        if lista:
            self.lista = lista
        else:
            self.lista = []

    def aplicar_lista(self):
        """transfiere los contenidos de la lista al widget"""
        for variable in self.lista:
            self.insertItem(variable)

    def myUpdate(self):
        """Actualizacion del contenido de la ventana"""
        self.clear()
        self.aplicar_lista()


class WidgetListaListBox(QListBox, WidgetLista):
    """ListBox que establece sus valores a partir de funciones auxiliares que trabajan sobre listas"""
    def __init__(self, parent, lista = None):
        WidgetLista.__init__(self, lista)
        QListBox.__init__(self, parent, "listBoxlista")


    def showEvent(self, event):
        """Redefine el showEvent de qt"""
        self.myUpdate()
        QListBox.showEvent(self, event)


class WidgetListaComboBox(QComboBox, WidgetLista):
    """QComboBox que establece sus valores a partir de funciones auxiliares que trabajan sobre listas"""
    #TODO: Falta conservar la seleccion con el show
    def __init__(self, parent):
        QComboBox.__init__(self, parent, "comboboxlista")
        WidgetLista.__init__(self)

    def showEvent(self, event):
        """Redefine el showEvent de qt"""
        self.myUpdate()
        QComboBox.showEvent(self, event)


#Clases derivadas

class WidgetListaComboBoxVars(WidgetListaComboBox):
    """ComboBoxLista modificado que devuelve siempre una lista de variables actualizadas"""
    def __init__(self, parent, datos, factores=True):
        WidgetListaComboBox.__init__(self, parent)
        self.__idu = datos
        self.__factores = factores
        
    def aplicar_lista(self):
        """Redefine el show de QComboBox, añadiendo el listado de variables"""
        self.lista = self.__idu.lista_tit(factores = self.__factores)
        WidgetListaComboBox.aplicar_lista(self)



class WidgetListaComboBoxFact(WidgetListaComboBox):
    """ComboBox modificado que devuelve siempre una lista de Factores actualizados"""
    def __init__(self, parent, datos):
        self.__idu = datos
        WidgetListaComboBox.__init__(self, parent)
        
    def aplicarlista(self):
        """Redefine el show de QComboBox, añadiendo el listado de variables"""
        self.lista = self.__idu.lista_tit(tipo = "Factor")
        WidgetListaComboBox.aplicar_lista(self)

#ClasesCompuestas


class QGridButtonGroup(QButtonGroup):
    """Reimplementación de QButtonGroup que organiza los botones de forma que ocupen lo menos posible
        Actualmente solo añade un QGridLayout de 2 columnas
    """
    def __init__(self, parent):
        QButtonGroup.__init__(self, parent, "SeleccionMultiple")
        self.setGeometry(QRect(110, 80, 170, 121))
        self.setColumnLayout(0, Qt.Vertical)
        self.layout().setSpacing(6)
        self.layout().setMargin(11)
        self.layout = QGridLayout(self.layout(), 2)
        self.__row = 0
        self.__col = 0

    def insert(self, boton):
        """Añade un boton. Redefine la clase base"""
        QButtonGroup.insert(self, boton)
        self.layout.addWidget(boton, self.__row, self.__col)
        if self.__col == 0:
            self.__col = 1
        else:
            self.__row += 1
            self.__col = 0

