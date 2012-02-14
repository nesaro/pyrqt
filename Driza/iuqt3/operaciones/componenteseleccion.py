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

"""Clases que componen los widgets de seleccion"""

from qt import QHBox, QVBox, QLabel

class WidgetSeleccionCaja(QVBox):
    """El elemento de seleccion más sencillo.
    Solo contiene una caja"""
    def __init__(self, nombre, parent = None):
        from Driza.iuqt3.widgetsqt import WidgetListaListBox
        QVBox.__init__(self, parent)
        self.label = QLabel(self)
        self.label.setText(nombre)
        self.caja = WidgetListaListBox(self)

class WidgetSeleccionCajaCaja(QVBox):
    """Dos ListBoxLista en disposición vertical"""
    def __init__(self, nombre1, nombre2, parent = None):
        QVBox.__init__(self, parent)
        self.caja1 = WidgetSeleccionCaja(nombre1, self).caja
        self.caja2 = WidgetSeleccionCaja(nombre2, self).caja

class WidgetSeleccionCajaComboCombo(QVBox):
    """Tiene un listbox y dos combobox"""
    def __init__(self, nombre, parent=None):
        QVBox.__init__(self, parent)
        self.caja = WidgetSeleccionCaja(nombre, self).caja
        from Driza.iuqt3.widgetsqt import WidgetListaComboBox
        self.combo1 = WidgetListaComboBox(self)
        self.combo2 = WidgetListaComboBox(self)

class WidgetSeleccionCajaCajaCajaComboCombo(QHBox):
    """Widget con dos zonas"""
    def __init__(self, nombre1, nombre2, nombre3):
        QHBox.__init__(self, None)
        self.zona1 = WidgetSeleccionCajaCaja(nombre1, nombre2, self)
        self.zona2 = WidgetSeleccionCajaComboCombo(nombre3, self)

class WidgetSeleccionCajaComboComboCajaCaja(QHBox):
    """Widget con dos zonas"""
    def __init__(self, nombre1, nombre2, nombre3):
        QHBox.__init__(self, None)
        self.zona1 = WidgetSeleccionCajaComboCombo(nombre1, self)
        self.zona2 = WidgetSeleccionCajaCaja(nombre2, nombre3, self)

class WidgetSeleccionCajaComboComboCaja(QHBox):
    """Widget con dos zonas"""
    def __init__(self, nombre1, nombre2):
        QHBox.__init__(self, None)
        self.zona1 = WidgetSeleccionCajaComboCombo(nombre1, self)
        self.zona2 = WidgetSeleccionCaja(nombre2, self)

