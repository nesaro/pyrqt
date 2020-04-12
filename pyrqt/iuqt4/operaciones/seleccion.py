#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2008  Néstor Arocha Rodríguez

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

"""Clases que gestionan la selección"""

from PyQt4 import QtCore,QtGui
from PyQt4.QtGui import QWidget, QIcon
import logging
LOG = logging.getLogger("Driza.iuqt4.operaciones.seleccion")


image0_data = [
"23 20 2 1",
"# c #313031",
". c #ffffff",
".......................",
".......................",
"......##...............",
"......#.#..............",
"......#..#.............",
"......#...#............",
"......#....#...........",
"......#.....#..........",
"......#......#.........",
"......#.......#........",
"......#.......#........",
"......#......#.........",
"......#.....#..........",
"......#....#...........",
"......#...#............",
"......#..#.............",
"......#.#..............",
"......##...............",
".......................",
"......................."
]
image1_data = [
"23 20 2 1",
"# c #313031",
". c #ffffff",
".......................",
".......................",
"...............##......",
"..............#.#......",
".............#..#......",
"............#...#......",
"...........#....#......",
"..........#.....#......",
".........#......#......",
"........#.......#......",
"........#.......#......",
".........#......#......",
"..........#.....#......",
"...........#....#......",
"............#...#......",
".............#..#......",
"..............#.#......",
"...............##......",
".......................",
"......................."
]

class SelectorElementosEstudio(QtGui.QWidget):
    """Clase padre de los selectores. Los selectores permiten elegir una 
    o más variables, o una variable y un valor de esa variable, etc
    Las clases hijas deben suministrar cajadisponible,add_element
    SelectorElementosEstudios tiene siempre una caja donde aparecen los resultados a la derecha, y provee los botones de adicion y sustracción de elementos
    """
    def __init__(self, interfazdato, cajadisponible):
        """Caja disponible son los elementos que aparecen a la izquierda en el selector"""
        #VARIABLES PUBLICAS
        QtGui.QWidget.__init__(self, None)

        image0 = QtGui.QPixmap(image0_data)
        image1 = QtGui.QPixmap(image1_data)

        WSelectorSimpleLayout = QtGui.QHBoxLayout(self)#,11,6)
        layout2 = QtGui.QVBoxLayout(None)#,0,6,"layout2")
        widgetStack1= QtGui.QStackedWidget(self)
        widgetStack1.addWidget(cajadisponible)
        widgetStack1.setCurrentWidget(cajadisponible)
        #TODO Pendiente portabilidad qt4
        #widgetStack1.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding,0,0,widgetStack1.sizePolicy().hasHeightForWidth()))
        self._cajadisponible = cajadisponible
        layout2.addWidget(widgetStack1)
        WSelectorSimpleLayout.addLayout(layout2)
        
        layout1 = QtGui.QVBoxLayout(None)#,0,6,"layout1")
        
        self.__pushButton1 = QtGui.QPushButton(self)
        self.__pushButton1.setMaximumSize(QtCore.QSize(30,30))
        #TODO Pendiente portabilidad qt4
        self.__pushButton1.setIcon(QIcon(image0))
        layout1.addWidget(self.__pushButton1)
        spacer1 = QtGui.QSpacerItem(30,122,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        layout1.addItem(spacer1)
        
        self.pushButton2 = QtGui.QPushButton(self)
        self.pushButton2.setMaximumSize(QtCore.QSize(30,30))
        #TODO Pendiente portabilidad qt4
        #self.pushButton2.setPixmap(image1)
        #self.pushButton2.setAccel("Del")
        layout1.addWidget(self.pushButton2)
        WSelectorSimpleLayout.addLayout(layout1)
        
        layout3 = QtGui.QVBoxLayout(None)#,0,6,"layout3")
        
        self._textLabel2 = QtGui.QLabel(self)
        layout3.addWidget(self._textLabel2)
        
        self._cajaseleccion = QtGui.QListWidget(self)
        self._cajaseleccion.setMinimumSize(QtCore.QSize(0,60))
        layout3.addWidget(self._cajaseleccion)
        WSelectorSimpleLayout.addLayout(layout3)
        #TODO Pendiente portabilidad qt4
        #self._cajaseleccion.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self._cajaseleccion.sizePolicy().hasHeightForWidth()))
        
        #TODO Pendiente portabilidad qt4
        self.setWindowTitle("Form1")
        self._textLabel2.setText(u"Selección")
        
        self.resize(QtCore.QSize(294,240).expandedTo(self.minimumSizeHint()))
        #TODO Pendiente portabilidad qt4
        #self.clearWState(Qt.WState_Polished)
        self.__conexiones()
        #Miembros !qt

        self.seleccion = []
        self._dato = interfazdato

    def showEvent(self, ev):
        """Redefinicion showEvent"""
        self._actualizar_cajas()
        QWidget.showEvent(self, ev)

    def _actualizar_cajas(self):
        """Actualiza el contenido de las cajas"""
        self._cajaseleccion.clear()
        for valor in self.seleccion:
            self._cajaseleccion.insertItem(0, str(valor))
        self._actualizar_caja_disponible()


    def __conexiones(self):
        """Establece las conexiones entre elementos"""
        from PyQt4.QtCore import SIGNAL
        self.connect(self.__pushButton1,SIGNAL("clicked()"),self._add_element)
        self.connect(self.pushButton2,SIGNAL("clicked()"),self.__borrar_elemento)


    def __borrar_elemento(self):
        """Borra el elemento seleccionado en lacaja de seleccion"""
        if self._cajaseleccion.currentItem():
            del self.seleccion[self._cajaseleccion.currentItem()] #FIXME
            self._actualizar_cajas()

    def _add_element(self):
        pass
    

class SelectorVariable(SelectorElementosEstudio):
    """Este selector posee dos cajas y dos botones, que son pasados en la inicialización. Una de las cajas almacena todas las posibilidades,mientras que la otra almacena la seleccion"""
    def __init__(self, dato):
        """Clase de inicialización, almacena los componentes"""
        from .componenteseleccion import WidgetSeleccionCaja
        SelectorElementosEstudio.__init__(self, dato, WidgetSeleccionCaja("Variables"))

    def _add_element(self):
        """Añade un elemento de la seleccion de la cajadisponible"""
        if self._cajadisponible.caja.currentItem():
            self.seleccion.append(self._cajadisponible.caja.currentItem().text())
            self._actualizar_cajas()

    def _actualizar_caja_disponible(self):
        """Actualiza la caja de elementos disponibles"""
        lista = []
        for var in self._dato.lista_tit():
            if not var in self.seleccion:
                lista.append(var)
        self._cajadisponible.caja.lista = lista
        self._cajadisponible.caja.myUpdate()


class SelectorVariableVariable(SelectorElementosEstudio):
    """Este selector posee tres cajas y dos botones, que son pasados en la inicialización. Una de las cajas almacena todas las posibilidades,mientras que la otra almacena la seleccion"""

    def __init__(self,dato):
        """Clase de inicialización, almacena los componentes"""
        from .componenteseleccion import WidgetSeleccionCajaCaja
        SelectorElementosEstudio.__init__(self,dato,WidgetSeleccionCajaCaja("Variable1","Variable2"))

    def _add_element(self):
        """Añade un elemento de la seleccion de la cajadisponible"""
        LOG.debug("_add_element: cajadisponible:" + str(self._cajadisponible.__class__))
        LOG.debug("_add_element: caja1:" + str(self._cajadisponible.caja1.__class__))
        if self._cajadisponible.caja1.currentText() and self._cajadisponible.caja2.currentText():
            self.seleccion.append([self._cajadisponible.caja1.currentText().latin1(),self._cajadisponible.caja2.currentText().latin1()])
            self._actualizar_cajas()

    def _actualizar_caja_disponible(self):
        """Actualiza la caja de elementos disponibles"""
        lista = []
        for var in self._dato.lista_tit():
            if not var in self.seleccion:
                lista.append(var)
        LOG.debug("_actualizar_caja_disponible: caja1:" + str(self._cajadisponible.caja1.__class__))
        self._cajadisponible.caja1.lista = lista
        self._cajadisponible.caja2.lista = lista


class SelectorDiscriminadorSimple(SelectorElementosEstudio):
    """Permite escoger varias parejas variable-valor"""
    def __init__(self, dato):
        """Clase de inicialización, almacena los componentes"""
        from componenteseleccion import WidgetSeleccionCajaCaja
        SelectorElementosEstudio.__init__(self, dato, WidgetSeleccionCajaCaja("Variable", "Caso"))
        self._textLabel2.setText("<b>Caso de la variable</b>")
        self.connect(self._cajadisponible.caja1,SIGNAL("selectionChanged()"),self.__actualizar_caja_2)

    def _add_element(self):
        """Añade un elemento de la seleccion de la cajadisponible"""
        if self._cajadisponible.caja1.currentText() and \
                self._cajadisponible.caja2.currentText():
            self.seleccion.append([self._cajadisponible.caja1.currentText().latin1(),self._cajadisponible.caja2.currentText().latin1()])
            self._actualizar_cajas()

    def _actualizar_caja_disponible(self):
        """Actualiza la caja de elementos disponibles"""
        lista = []
        for var in self._dato.lista_titDiscreto():
            if not var in self.seleccion:
                lista.append(var)
        self._cajadisponible.caja1.lista = lista
        self.__actualizar_caja_2()
        self._cajadisponible.caja1.myUpdate()


    def __updatecaja2(self):
        listacasos=[str(x) for x in self._dato.getCasos(self._cajadisponible.caja1.currentText().latin1())]
        self._cajadisponible.caja2.lista=listacasos
        self._cajadisponible.caja2.myUpdate()

class SelectorDiscriminadorDoble(SelectorElementosEstudio):
    """Permite escoger varias parejas de valores para una variable dada"""
    def __init__(self,dato):
        from componenteseleccion import WidgetSeleccionComboCombo
        SelectorElementosEstudio.__init__(self,dato,WidgetSeleccionComboCombo("Variable"))
        self.connect(self._cajadisponible.caja,SIGNAL("selectionChanged()"),self.__actualizar_combos)

    def _add_element(self):
        if self._cajadisponible.caja.currentText():
            lista=[self._cajadisponible.caja.currentText,self._cajadisponible.combo1.currentText,self._cajadisponible.combo2.currentText]
            self.seleccion.append(lista)
            self._actualizar_cajas()

    def _actualizar_caja_disponible(self):
        """Actualiza la caja de elementos disponibles"""
        lista = []
        for var in self._dato.lista_titDiscreto():
            if not var in self.seleccion:
                lista.append(var)
        self._cajadisponible.caja.lista = lista
        self.__actualizar_combos()
        self._cajadisponible.caja.myUpdate()

    def __actualizar_combos(self):
        """Actualiza los combos con los casos de la variable"""
        listacasos = [str(x) for x in self._dato.obtener_casos(self._cajadisponible.caja.currentText().latin1())]
        self._cajadisponible.combo1.lista = listacasos
        self._cajadisponible.combo2.lista = listacasos
        self._cajadisponible.combo1.myUpdate()
        self._cajadisponible.combo2.myUpdate()


class SelectorVariableDiscriminadorSimple(SelectorElementosEstudio):
    """Permite escoger varias parejas variable-valor en vez de solamente variables. Utilizadas en las proporciones"""
    def __init__(self, dato):
        """Clase de inicialización, almacena los componentes"""
        from componenteseleccion import WidgetSeleccionCajaCajaCajaComboCombo
        SelectorElementosEstudio.__init__(self,dato,WidgetSeleccionCajaCajaCajaComboCombo("Variable","Caso","Variable4"))
        self._textLabel2.setText("<b>Caso de la variable</b>")
        self.connect(self._cajadisponible.zona1.caja1,SIGNAL("selectionChanged()"),self.__updatecaja2)
        self.connect(self._cajadisponible.zona2.caja,SIGNAL("selectionChanged()"),self.__actualizar_combos)

    def _add_element(self):
        """Añade un elemento de la seleccion de la cajadisponible"""
        if self._cajadisponible.zona1.caja1.currentText() and self._cajadisponible.zona1.caja2.currentText() and self._cajadisponible.zona2.caja.currentText():
            array1=[self._cajadisponible.zona1.caja1.currentText().latin1(),self._cajadisponible.zona1.caja2.currentText().latin1()]
            array2=[self._cajadisponible.zona2.caja.currentText().latin1(),self._cajadisponible.zona2.combo1.currentText().latin1(),self._cajadisponible.zona2.combo2.currentText().latin1()]
            self.seleccion.append([array1,array2])
            self._actualizar_cajas()

    def _actualizar_caja_disponible(self):
        """Actualiza la caja de elementos disponibles"""
        lista = []
        for var in self._dato.lista_tit():
            if not var in self.seleccion:
                lista.append(var)
        self._cajadisponible.zona1.caja1.lista = lista
        self._cajadisponible.zona2.caja.lista = lista
        self.__updatecaja2()
        self._cajadisponible.zona1.caja1.myUpdate()
        self._cajadisponible.zona2.caja.myUpdate()


    def __actualizar_caja_2(self):
        """Actualiza la segunda caja"""
        listacasos = [str(x) for x in self._dato.obtener_casos(self._cajadisponible.zona1.caja1.currentText().latin1())]
        self._cajadisponible.zona1.caja2.lista = listacasos
        self._cajadisponible.zona1.caja2.myUpdate()

    def __actualizar_combos(self):
        """Actualiza los combos con los casos de la variable"""
        listacasos = [str(x) for x in self._dato.obtener_casos(self._cajadisponible.zona2.caja.currentText().latin1())]
        self._cajadisponible.zona2.combo1.lista = listacasos
        self._cajadisponible.zona2.combo2.lista = listacasos
        self._cajadisponible.zona2.combo1.myUpdate()
        self._cajadisponible.zona2.combo2.myUpdate()

class SelectorVariableDiscriminadorDoble(SelectorElementosEstudio):
    """Esta clase..."""
    def __init__(self, dato):
        from .componenteseleccion import WidgetSeleccionCajaComboComboCaja
        from PyQt4.QtCore import SIGNAL
        SelectorElementosEstudio.__init__(self,dato,WidgetSeleccionCajaComboComboCaja("Discriminador","Variable"))
        self.connect(self._cajadisponible.zona1.caja,SIGNAL("selectionChanged()"),self.__actualizar_combos)

    def _add_element(self):
        """Añade un elemento de la seleccion de la cajadisponible"""
        if self._cajadisponible.zona1.caja.currentText() and self._cajadisponible.zona2.caja.currentText():
            if self._cajadisponible.zona1.combo1.currentText()!=self._cajadisponible.zona1.combo2.currentText():
                array1=[self._cajadisponible.zona1.caja.currentText().latin1(),self._cajadisponible.zona1.combo1.currentText().latin1(),self._cajadisponible.zona1.combo2.currentText().latin1()]
                array2=self._cajadisponible.zona2.caja.currentText().latin1()
                self.seleccion.append([array1,array2])
                self._actualizar_cajas()

    def _actualizar_caja_disponible(self):
        """Actualiza la caja de elementos disponibles"""
        lista = []
        for var in self._dato.lista_tit_discreto():
            if not var in self.seleccion:
                lista.append(var)
        self._cajadisponible.zona1.caja.lista = lista
        self._cajadisponible.zona2.caja.lista = self._dato.lista_tit_numerica()
        self._cajadisponible.zona1.caja.myUpdate()
        self._cajadisponible.zona2.caja.myUpdate()


    def __actualizar_combos(self):
        """Actualiza los combos con los casos de la variable"""
        listacasos = [str(x) for x in self._dato.obtener_casos(self._cajadisponible.zona1.caja.currentText().latin1())]
        self._cajadisponible.zona1.combo1.lista = listacasos
        self._cajadisponible.zona1.combo2.lista = listacasos
        self._cajadisponible.zona1.combo1.myUpdate()
        self._cajadisponible.zona1.combo2.myUpdate()


class SelectorVariableVariableDiscriminadorDoble(SelectorElementosEstudio):
    """Esta clase..."""
    def __init__(self, dato):
        from componenteseleccion import WidgetSeleccionCajaComboComboCaja
        SelectorElementosEstudio.__init__(self,dato,WidgetSeleccionCajaComboComboCajaCaja("Discriminador","Variable1","Variable2"))
        self.connect(self._cajadisponible.zona1.caja,SIGNAL("selectionChanged()"),self.__actualizar_combos)

    def _add_element(self):
        """Añade un elemento de la seleccion de la cajadisponible"""
        if self._cajadisponible.zona1.caja.currentText() and self._cajadisponible.zona2.caja1.currentText() and self._cajadisponible.zona2.caja2.currentText():
            array1=[self._cajadisponible.zona1.caja.currentText().latin1(),self._cajadisponible.zona1.combo1.currentText().latin1(),self._cajadisponible.zona1.combo2.currentText().latin1()]
            array2=[self._cajadisponible.zona2.caja1.currentText().latin1(),self._cajadisponible.zona2.caja2.currentText().latin1()]
            self.seleccion.append([array1,array2])
            self._actualizar_cajas()

    def _actualizar_caja_disponible(self):
        """Actualiza la caja de elementos disponibles"""
        lista = []
        for var in self._dato.lista_tit_discreto():
            if not var in self.seleccion:
                lista.append(var)
        self._cajadisponible.zona1.caja.lista = lista
        self._cajadisponible.zona2.caja1.lista = self._dato.lista_tit_numerica()
        self._cajadisponible.zona2.caja2.lista = self._dato.lista_tit_numerica()
        self._cajadisponible.zona1.caja.myUpdate()
        self._cajadisponible.zona2.caja1.myUpdate()
        self._cajadisponible.zona2.caja2.myUpdate()


    def __actualizar_combos(self):
        """Actualiza los combos con los casos de la variable"""
        listacasos = [str(x) for x in self._dato.obtener_casos(self._cajadisponible.zona1.caja.currentText().latin1())]
        self._cajadisponible.zona1.combo1.lista = listacasos
        self._cajadisponible.zona1.combo2.lista = listacasos
        self._cajadisponible.zona1.combo1.myUpdate()
        self._cajadisponible.zona1.combo2.myUpdate()

