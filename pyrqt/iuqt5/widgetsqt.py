#!/usr/bin/python
# -*- coding: utf-8 -*-


#Copyright (C) 2007-2008  Néstor Arocha Rodrguez
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

from PyQt4 import QtCore,QtGui
"""Todas aquellas clases que heredan directamente de algun widget de Qt y que pretenden aumentar su funcionalidad"""

class WidgetLista:
    """Clase base de los widgets que se gestionan una lista"""

    def __init__(self,lista=None):
    	self.seleccion=None
    	if lista:
    		self.lista=lista
    	else:
    		self.lista=[]

    def aplicarlista(self):
    	for variable in self.lista:
    		self.insertItem(0,variable)

    def obtenerseleccion(self):
    	"""Extrae la seleccion del ListBox"""
    	pass

    def aplicarseleccion(self):
    	"""Selecciona el elemento self.seleccion"""
    	pass

    def myUpdate(self):
    	self.obtenerseleccion()
    	self.clear()
    	self.aplicarlista()
    	self.aplicarseleccion()


class WidgetListaListBox(QtGui.QListWidget,WidgetLista):
    """ListBox que establece sus valores a partir de funciones auxiliares que trabajan sobre listas"""
    def __init__(self,parent,lista=None):
    	WidgetLista.__init__(self,lista)
    	QtGui.QListWidget.__init__(self,parent)


    def showEvent(self,ev):
    	self.myUpdate()
    	QtGui.QListWidget.showEvent(self,ev)



class WidgetListaComboBox(QtGui.QComboBox,WidgetLista):
    """QComboBox que establece sus valores a partir de funciones auxiliares que trabajan sobre listas"""
    #TODO: Falta conservar la seleccion con el show
    def __init__(self,parent):
    	QtGui.QComboBox.__init__(self,parent)
    	WidgetLista.__init__(self)

    def showEvent(self,ev):
    	self.myUpdate()
    	QtGui.QComboBox.showEvent(self,ev)


#Clases derivadas

class WidgetListaComboBoxVars(WidgetListaComboBox):
    """ComboBoxLista modificado que devuelve siempre una lista de variables actualizadas"""
    def __init__(self,parent,datos,factores=True):
    	WidgetListaComboBox.__init__(self,parent)
    	self.__datos=datos
    	self.__factores=factores
    	
    def aplicarlista(self):
    	"""Redefine el show de QComboBox, añadiendo el listado de variables"""
    	self.lista=self.__datos.arrTit(factores=self.__factores)
    	ComboBoxLista.aplicarlista(self)



class WidgetListaComboBoxFact(WidgetListaComboBox):
    """ComboBox modificado que devuelve siempre una lista de Factores actualizados"""
    def __init__(self,parent,datos):
    	self.__datos=datos
    	WidgetListaComboBox.__init__(self,parent)
    	
    def aplicarlista(self):
    	"""Redefine el show de QComboBox, añadiendo el listado de variables"""
    	self.lista=self.__datos.arrTit(tipo="Factor")
    	ComboBoxLista.aplicarlista(self)

#ClasesCompuestas


class QGridButtonGroup(QtGui.QButtonGroup):
    """Reimplementación de QButtonGroup que organiza los botones de forma que ocupen lo menos posible
    	Actualmente solo añade un QGridLayout de 2 columnas
    """
    def __init__(self,parent,nombre):
    	QtGui.QButtonGroup.__init__(self,parent,"SeleccionMultiple")
    	self.setGeometry(QRect(110,80,170,121))
    	self.setColumnLayout(0,Qt.Vertical)
    	self.layout().setSpacing(6)
    	self.layout().setMargin(11)
    	self.layout=QGridLayout(self.layout(),2)
    	self.x=0
    	self.y=0

    def insert(self,boton):
    	QtGui.QButtonGroup.insert(self,boton)
    	self.layout.addWidget(boton,self.x,self.y)
    	if self.y==0:
    		self.y=1
    	else:
    		self.x+=1
    		self.y=0

