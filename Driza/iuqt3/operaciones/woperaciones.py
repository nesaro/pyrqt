#!/usr/bin/python
# -*- coding: utf-8 -*-
#

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

"""woperaciones.py: Todos los widgets de operaciones"""

from qt import QWidget, QGridLayout, Qt, QSize, QWidgetStack

class WidgetOperacion(QWidget):
    """Clase base de todos los widgets de operaciones"""
    def __init__(self, name):
        if isinstance(name, unicode):
            name = name.encode("latin1")
        if not name:
            self.setName("WidgetOperacion")
        QWidget.__init__(self, None, name, 0)
        self._rejilla = QGridLayout(self, 1, 1, 11, 6, "rejilla")
        self.setCaption("Form1")
        self.resize(QSize(600, 480).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

    def seleccion(self):
        """Devuelve los elementos seleccionados en el selector"""
        return self._wseleccion.seleccion

    def opciones(self):
        """Devuelve las opciones escogidas en todos los widgets de opciones"""
        return self._wopciones.opciones()

class WidgetOperacionSelectorOpcion(WidgetOperacion):
    """WidgetOperacionSelectorOpcion es un widget de operaciones que tiene un solo selector 
    y un solo widget de opciones"""
    def __init__(self, name, objetowidgetselector, opcioneswidgetopciones, interfazdatos):
        WidgetOperacion.__init__(self, name)
        #Inicializacion de widgets
        from Driza.iuqt3.operaciones.wopciones import WOpciones
        self._wseleccion = objetowidgetselector(interfazdatos)
        self._wopciones = WOpciones(opcioneswidgetopciones)

        zonastacksuperior = QWidgetStack(self, "stacksuperior")
        zonastacksuperior.setMinimumSize(QSize(200, 200))
        zonastacksuperior.addWidget(self._wseleccion)
        zonastacksuperior.raiseWidget(self._wseleccion)
        zonastackinferior = QWidgetStack(self, "stackinferior")
        zonastackinferior.setMinimumSize(QSize(200, 200))
        zonastackinferior.addWidget(self._wopciones)
        zonastackinferior.raiseWidget(self._wopciones)

        self._rejilla.addWidget(zonastacksuperior, 0, 0)
        self._rejilla.addWidget(zonastackinferior, 1, 0)

