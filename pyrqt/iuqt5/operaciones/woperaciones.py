#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Copyright (C) 2007-2008  Néstor Arocha Rodríguez

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

"""woperaciones.py: Todos los widgets de operaciones"""
from PyQt4 import QtCore,QtGui

class WidgetOperacion(QtGui.QWidget):
    """Clase base de todos los widgets de operaciones"""
    def __init__(self, name):
        if isinstance(name, str):
            name = name.encode("latin1")
        if not name:
            self.setName("WidgetOperacion")
        QtGui.QWidget.__init__(self)#,None,name,0)
        self._rejilla = QtGui.QGridLayout(self)#,1,1,11,6,"rejilla")
        self.languageChange()
        self.resize(QtCore.QSize(600,480).expandedTo(self.minimumSizeHint()))
        #TODO Pendiente portabilidad qt4
        #self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        #TODO Pendiente portabilidad qt4
        #self.setCaption(self.__tr("Form1"))
        pass

    def __tr(self,s,c = None):
        return qApp.translate("Form1",s,c)
    
    def seleccion(self):
        """Devuelve los elementos seleccionados en el selector"""
        #Debe devolver una lista de str
        seleccion = self._wseleccion.seleccion
        seleccion2 = map(str, seleccion)
        return seleccion2

    def opciones(self):
        """Devuelve las opciones escogidas en todos los widgets de opciones"""
        return self._wopciones.opciones()

class WidgetOperacionSelectorOpcion(WidgetOperacion):
    """WidgetOperacionSelectorOpcion es un widget de operaciones que tiene un solo selector 
    y un solo widget de opciones"""
    def __init__(self, name, objetowidgetselector, opcioneswidgetopciones,
                 interfazdatos):
        WidgetOperacion.__init__(self, name)
#
#        #Condiciones a probar
#        from wopciones import WOpciones
#        from seleccion import SelectorElementosEstudio
#        assert(isinstance(widgetselector,SelectorElementosEstudio))
#        assert(isinstance(widgetopciones,WOpciones))
#
        #Inicializacion de widgets
        from pyrqt.iuqt4.operaciones.wopciones import WOpciones
        self._wseleccion = objetowidgetselector(interfazdatos)
        self._wopciones = WOpciones(opcioneswidgetopciones)

        zonastacksuperior = QtGui.QStackedWidget(self)
        zonastacksuperior.setMinimumSize(QtCore.QSize(200, 200))
        zonastacksuperior.addWidget(self._wseleccion)
        zonastacksuperior.setCurrentWidget(self._wseleccion)
        zonastackinferior = QtGui.QStackedWidget(self)
        zonastackinferior.setMinimumSize(QtCore.QSize(200,200))
        zonastackinferior.addWidget(self._wopciones)
        zonastackinferior.setCurrentWidget(self._wopciones)

        self._rejilla.addWidget(zonastacksuperior,0,0)
        self._rejilla.addWidget(zonastackinferior,1,0)


