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

"""Clases que gestionan la selección"""

from qt import QWidget, QPixmap, QHBoxLayout, QVBoxLayout, QWidgetStack, QSizePolicy, \
        QPushButton, QSize, QSpacerItem, QLabel, QListBox, Qt, SIGNAL

IMAGE1DATA = [
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
IMAGE2DATA = [
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

class SelectorElementosEstudio(QWidget):
    """Clase padre de los selectores. Los selectores permiten elegir una 
    o más variables, o una variable y un valor de esa variable, etc
    Las clases hijas deben suministrar cajadisponible,addelemento
    SelectorElementosEstudios tiene siempre una caja donde aparecen los resultados a la derecha, y provee los botones de adicion y sustracción de elementos
    """
    def __init__(self, interfazdato, cajadisponible):
        """Caja disponible son los elementos que aparecen a la izquierda en el selector"""
        #VARIABLES PUBLICAS
        QWidget.__init__(self, None, "selector", 0)

        image1 = QPixmap(IMAGE1DATA)
        image2 = QPixmap(IMAGE2DATA)

        selectorsimplelayout = QHBoxLayout(self, 11, 6, "WSelectorSimpleLayout")
        layout2 = QVBoxLayout(None, 0, 6, "layout2")
        widgetstack1 = QWidgetStack(self, "staaack")
        widgetstack1.addWidget(cajadisponible)
        widgetstack1.raiseWidget(cajadisponible)
        widgetstack1.setSizePolicy(QSizePolicy(\
                QSizePolicy.Expanding, QSizePolicy.Expanding, \
                0, 0, widgetstack1.sizePolicy().hasHeightForWidth()))
        self._cajadisponible = cajadisponible
        layout2.addWidget(widgetstack1)
        selectorsimplelayout.addLayout(layout2)
        
        layout1 = QVBoxLayout(None, 0, 6, "layout1")
        
        self.__pushbutton1 = QPushButton(self, "pushButton1")
        self.__pushbutton1.setMaximumSize(QSize(30, 30))
        self.__pushbutton1.setPixmap(image1)
        layout1.addWidget(self.__pushbutton1)
        spacer1 = QSpacerItem(30, 122, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout1.addItem(spacer1)
        
        self.__pushbutton2 = QPushButton(self,"pushButton2")
        self.__pushbutton2.setMaximumSize(QSize(30, 30))
        self.__pushbutton2.setPixmap(image2)
        self.__pushbutton2.setAccel("Del")
        layout1.addWidget(self.__pushbutton2)
        selectorsimplelayout.addLayout(layout1)
        
        layout3 = QVBoxLayout(None, 0, 6, "layout3")
        
        self._textlabel2 = QLabel(self, "textLabel2")
        layout3.addWidget(self._textlabel2)
        
        self._cajaseleccion = QListBox(self,"cajaseleccion")
        self._cajaseleccion.setMinimumSize(QSize(0, 60))
        layout3.addWidget(self._cajaseleccion)
        selectorsimplelayout.addLayout(layout3)
        self._cajaseleccion.setSizePolicy(QSizePolicy(\
                QSizePolicy.Expanding,QSizePolicy.Expanding, 0, 0, \
                self._cajaseleccion.sizePolicy().hasHeightForWidth()))
        
        self.setCaption("Form1")
        self._textlabel2.setText(u"Selección")
        
        self.resize(QSize(294, 240).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)
        self.__conexiones()
        #Miembros !qt

        self.seleccion = []
        self._dato = interfazdato

    def showEvent(self, event):
        """Redefinicion showEvent"""
        self._actualizar_cajas()
        QWidget.showEvent(self, event)

    def _actualizar_cajas(self):
        """Actualiza el contenido de las cajas"""
        self._cajaseleccion.clear()
        for valor in self.seleccion:
            self._cajaseleccion.insertItem(str(valor))
        self._actualizar_caja_disponible()


    def __conexiones(self):
        """Establece las conexiones entre elementos"""
        self.connect(self.__pushbutton1, SIGNAL("clicked()"), self._anadir_elemento)
        self.connect(self.__pushbutton2, SIGNAL("clicked()"), self.__borrar_elemento)


    def __borrar_elemento(self):
        """Borra el elemento seleccionado en lacaja de seleccion"""
        if self._cajaseleccion.currentText():
            del self.seleccion[self._cajaseleccion.currentItem()]
            self._actualizar_cajas()
    

class SelectorVariable(SelectorElementosEstudio):
    """Este selector posee dos cajas y dos botones, 
    que son pasados en la inicialización. Una de las cajas almacena todas 
    las posibilidades,mientras que la otra almacena la seleccion"""
    def __init__(self, dato):
        """Clase de inicialización, almacena los componentes"""
        from Driza.iuqt3.operaciones.componenteseleccion import WidgetSeleccionCaja
        SelectorElementosEstudio.__init__(self, dato, WidgetSeleccionCaja("Variables"))

    def _anadir_elemento(self):
        """Añade un elemento de la seleccion de la cajadisponible"""
        if self._cajadisponible.caja.currentText():
            self.seleccion.append(self._cajadisponible.caja.currentText().latin1())
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
    """Este selector posee tres cajas y dos botones, que son pasados en la inicialización.
    Una de las cajas almacena todas las posibilidades, mientras que la otra almacena la seleccion"""

    def __init__(self, dato):
        """Clase de inicialización, almacena los componentes"""
        from Driza.iuqt3.operaciones.componenteseleccion import WidgetSeleccionCajaCaja
        SelectorElementosEstudio.__init__(self, dato, WidgetSeleccionCajaCaja("Variable1", "Variable2"))

    def _anadir_elemento(self):
        """Añade un elemento de la seleccion de la cajadisponible"""
        if self._cajadisponible.caja1.currentText() and \
                self._cajadisponible.caja2.currentText():
            lista = [self._cajadisponible.caja1.currentText().latin1(), 
                    self._cajadisponible.caja2.currentText().latin1()]
            self.seleccion.append(lista)
            self._actualizar_cajas()

    def _actualizar_caja_disponible(self):
        """Actualiza la caja de elementos disponibles"""
        lista = []
        for var in self._dato.lista_tit():
            if not var in self.seleccion:
                lista.append(var)
        self._cajadisponible.caja1.lista = lista
        self._cajadisponible.caja2.lista = lista
        self._cajadisponible.caja1.myUpdate()
        self._cajadisponible.caja2.myUpdate()


class SelectorDiscriminadorSimple(SelectorElementosEstudio):
    """Permite escoger varias parejas variable-valor"""
    def __init__(self, dato):
        """Clase de inicialización, almacena los componentes"""
        from Driza.iuqt3.operaciones.componenteseleccion import WidgetSeleccionCajaCaja
        SelectorElementosEstudio.__init__(self, dato, WidgetSeleccionCajaCaja("Variable", "Caso"))
        self._textlabel2.setText("<b>Caso de la variable</b>")
        self.connect(self._cajadisponible.caja1, SIGNAL("selectionChanged()"), self.__actualizar_caja_2)

    def _anadir_elemento(self):
        """Añade un elemento de la seleccion de la cajadisponible"""
        if self._cajadisponible.caja1.currentText() and \
                self._cajadisponible.caja2.currentText():
            lista = [self._cajadisponible.caja1.currentText().latin1(), 
                    self._cajadisponible.caja2.currentText().latin1()]
            self.seleccion.append(lista)
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


    def __actualizar_caja_2(self):
        """Actualiza la segunda caja"""
        listacasos = [str(x) for x in self._dato.obtener_casos(self._cajadisponible.caja1.currentText().latin1())]
        self._cajadisponible.caja2.lista = listacasos
        self._cajadisponible.caja2.myUpdate()

class SelectorDiscriminadorDoble(SelectorElementosEstudio):
    """Permite escoger varias parejas de valores para una variable dada"""
    def __init__(self, dato):
        from Driza.iuqt3.operaciones.componenteseleccion import WidgetSeleccionCajaComboCombo
        SelectorElementosEstudio.__init__(self, dato, WidgetSeleccionCajaComboCombo("Variable"))
        self.connect(self._cajadisponible.caja, SIGNAL("selectionChanged()"), self.__actualizar_combos)

    def _anadir_elemento(self):
        """Añade un elemento"""
        if self._cajadisponible.caja.currentText():
            lista = [self._cajadisponible.caja.currentText,
                    self._cajadisponible.combo1.currentText, 
                    self._cajadisponible.combo2.currentText]
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
        from Driza.iuqt3.operaciones.componenteseleccion import WidgetSeleccionCajaCajaCajaComboCombo
        widget = WidgetSeleccionCajaCajaCajaComboCombo("Variable", "Caso", "Variable4")
        SelectorElementosEstudio.__init__(self, dato, widget)
        self._textlabel2.setText("<b>Caso de la variable</b>")
        self.connect(self._cajadisponible.zona1.caja1, SIGNAL("selectionChanged()"), self.__updatecaja2)
        self.connect(self._cajadisponible.zona2.caja, SIGNAL("selectionChanged()"), self.__actualizar_combos)

    def _anadir_elemento(self):
        """Añade un elemento de la seleccion de la cajadisponible"""
        zona1caja1 = self._cajadisponible.zona1.caja1.currentText()
        zona1caja2 = self._cajadisponible.zona1.caja2.currentText()
        zona2caja = self._cajadisponible.zona2.caja.currentText()
        zona2combo1 = self._cajadisponible.zona2.combo1.currentText()
        zona2combo2 = self._cajadisponible.zona2.combo2.currentText()
        if zona1caja1 and zona1caja2 and zona2caja:
            array1 = [zona1caja1.latin1(), zona1caja2.latin1()]
            array2 = [zona2caja.latin1(), zona2combo1.latin1(), zona2combo2.latin1()]
            self.seleccion.append([array1, array2])
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
        from Driza.iuqt3.operaciones.componenteseleccion import WidgetSeleccionCajaComboComboCaja
        SelectorElementosEstudio.__init__(self, dato, WidgetSeleccionCajaComboComboCaja("Discriminador", "Variable"))
        self.connect(self._cajadisponible.zona1.caja, SIGNAL("selectionChanged()"), self.__actualizar_combos)

    def _anadir_elemento(self):
        """Añade un elemento de la seleccion de la cajadisponible"""
        zona1caja = self._cajadisponible.zona1.caja.currentText()
        zona2caja = self._cajadisponible.zona2.caja.currentText()
        zona1combo1 = self._cajadisponible.zona1.combo1.currentText()
        zona1combo2 = self._cajadisponible.zona1.combo2.currentText()
        if zona1caja and zona2caja:
            if zona1combo1 != zona1combo2:
                array1 = [zona1caja.latin1(), zona1combo1.latin1(), zona1combo2.latin1()]
                array2 = zona2caja.latin1()
                self.seleccion.append([array1, array2])
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
        from Driza.iuqt3.operaciones.componenteseleccion import WidgetSeleccionCajaComboComboCajaCaja
        widget = WidgetSeleccionCajaComboComboCajaCaja("Discriminador", "Variable1", "Variable2")
        SelectorElementosEstudio.__init__(self, dato, widget)
        self.connect(self._cajadisponible.zona1.caja, SIGNAL("selectionChanged()"), self.__actualizar_combos)

    def _anadir_elemento(self):
        """Añade un elemento de la seleccion de la cajadisponible"""
        zona1caja = self._cajadisponible.zona1.caja.currentText()
        zona2caja1 = self._cajadisponible.zona2.caja1.currentText()
        zona2caja2 = self._cajadisponible.zona2.caja2.currentText()
        zona1combo1 = self._cajadisponible.zona1.combo1.currentText()
        zona1combo2 = self._cajadisponible.zona1.combo2.currentText()
        if zona1caja and zona2caja1 and zona2caja2:
            array1 = [zona1caja.latin1(), zona1combo1.latin1(), zona1combo2.latin1()]
            array2 = [zona2caja1.latin1(), zona2caja2.latin1()]
            self.seleccion.append([array1, array2])
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

