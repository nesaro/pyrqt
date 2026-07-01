#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2008  Néstor Arocha Rodríguez

#This file is part of pyrqt.
#
#pyrqt is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#pyrqt is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pyrqt; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""Clases que componen los widgets de seleccion"""

from PyQt4 import QtCore,QtGui

#TODO: Todos los widgets deben heredar QWidget como WidgetSeleccionCaja

class WidgetSeleccionCaja(QtGui.QWidget):
    """El elemento de seleccion más sencillo.
    Solo contiene una caja"""
    def __init__(self, nombre, parent = None):
        from pyrqt.iuqt4.widgetsqt import WidgetListaListBox
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        self.label = QtGui.QLabel(self)
        self.label.setText(nombre)
        self.caja=WidgetListaListBox(self)
        layout.addWidget(self.label)
        layout.addWidget(self.caja)

class WidgetSeleccionCajaCaja(QtGui.QWidget):
    """Dos ListBoxLista en disposición vertical"""
    def __init__(self, nombre1, nombre2, parent = None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        self.caja1 = WidgetSeleccionCaja(nombre1, parent)
        self.caja2 = WidgetSeleccionCaja(nombre2, parent)
        layout.addWidget(self.caja1)
        layout.addWidget(self.caja2)

#AQUI, hay que cambiar el padre de estas clases por algun derivado de QWidget
class WidgetSeleccionCajaComboCombo(QtGui.QFrame):
    """Tiene un listbox y dos combobox"""
    def __init__(self, nombre, parent=None):
        QtGui.QFrame.__init__(self,parent)
        self.caja=WidgetSeleccionCaja(nombre, self)
        from pyrqt.iuqt4.widgetsqt import WidgetListaComboBox
        self.combo1=WidgetListaComboBox(self)
        self.combo2=WidgetListaComboBox(self)

class WidgetSeleccionCajaCajaCajaComboCombo(QtGui.QHBoxLayout):
    """Widget con dos zonas"""
    def __init__(self, nombre1, nombre2, nombre3):
        QtGui.QHBoxLayout.__init__(self,None)
        self.zona1 = WidgetSeleccionCajaCaja(nombre1,nombre2,self)
        self.zona2 = WidgetSeleccionCajaComboCombo(nombre1,self)

class WidgetSeleccionCajaComboComboCajaCaja(QtGui.QHBoxLayout):
    """Widget con dos zonas"""
    def __init__(self, nombre1, nombre2, nombre3):
        QtGui.QHBoxLayout.__init__(self, None)
        self.zona1 = WidgetSeleccionCajaComboCombo(nombre1, self)
        self.zona2 = WidgetSeleccionCajaCaja(nombre2, nombre3,self)

class WidgetSeleccionCajaComboComboCaja(QtGui.QFrame): 
    """Widget con dos zonas"""
    def __init__(self, nombre1, nombre2):
        #QtGui.QHBoxLayout.__init__(self,None)
        QtGui.QFrame.__init__(self, None)
        self.zona1=WidgetSeleccionCajaComboCombo(nombre1, self)
        self.zona2=WidgetSeleccionCaja(nombre2, self)

