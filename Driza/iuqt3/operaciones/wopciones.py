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

"""Clases relacionadas con los widgets de opciones"""


from qt import QHButtonGroup, QVBox, QGroupBox, QHBox, QVGroupBox, QHGroupBox, Qt, QCheckBox, QLabel, QLineEdit, \
        QRadioButton, QVBoxLayout, QSpacerItem, QSizePolicy, QComboBox, QHBoxLayout, SIGNAL
from Driza.iuqt3.widgetsqt import QGridButtonGroup


class ContenedorElementoWidgetOpciones:
    """Contiene las funciones de adición de widgets necesaria para los contenedores"""
    def __init__(self):
        """Inicializa la lista de los elementos que contiene el contenedor"""
        self.lista = []

    def procesar(self, diccionario):
        """Transforma un diccionario con el nombre y las opciones de un widget en el propio widget"""
        if diccionario:
            from Driza.listas import TIPOSWIDGETOPCIONESQT3
            objeto = TIPOSWIDGETOPCIONESQT3[diccionario["tipo"]]["clase"]
            if diccionario["tipo"] == "EntradaTexto":
                if diccionario.has_key("valorpordefecto"):
                    widget = objeto(self, diccionario["nombre"], diccionario["valorpordefecto"])
                else:
                    widget = objeto(self, diccionario["nombre"])
            elif diccionario["tipo"]=="SeleccionSimple":
                widget = objeto(self, diccionario["nombre"], diccionario["opciones"])
            elif diccionario["tipo"]=="SeleccionMultiple":
                widget = objeto(self, diccionario["nombre"], diccionario["opciones"])
            elif diccionario["tipo"]=="ListaSimple":
                widget = objeto(self, diccionario["nombre"], diccionario["opciones"])
            elif diccionario["tipo"]=="Texto":
                widget = objeto(self, diccionario["nombre"], diccionario["texto"], diccionario["valorpordefecto"])
            elif diccionario["tipo"]=="Variables":
                widget = objeto(self, diccionario["nombre"])
            elif diccionario["tipo"]=="Factores":
                widget = objeto(self, diccionario["nombre"])
        self.lista.append(widget)
        
    def opciones(self):
        """Devuelve un diccionario con las opciones y sus valores [Virtual]"""
        diccionario = {}
        for elemento in self.lista:
            diccionario.update(elemento.opciones())
        return diccionario

class WOpciones(QVBox, ContenedorElementoWidgetOpciones):
    """Cualquier widget que tenga un conjunto de opciones"""
    def __init__(self, listaopciones = None):
        QVBox.__init__(self, None, "Widget opciones")
        ContenedorElementoWidgetOpciones.__init__(self)
        self.clearWState(Qt.WState_Polished)
        self.setCaption("WidgetOpciones")
        if listaopciones == None:
            listaopciones = []
        for opcion in listaopciones:
            self.procesar(opcion)

class ElementoWidgetOpciones:
    """Clase padre de cualquier elemento que pertenezca a widgetopciones"""
    def __init__(self):
        self.diccionario = {}

    def opciones(self):
        """Devuelve las opciones del widget. Debe ser reimplementada por las clases hijas"""
        pass

    def activar(self):
        """Activa el widget. Ciertas clases hijas lo reimplementan"""
        pass

    def desactivar(self):
        """desactiva el widget. Ciertas clases hijas lo reimplementan"""
        pass

class EWOSeleccionMultiple(ElementoWidgetOpciones, QGridButtonGroup):
    """Es una lista de opciones que pueden ser seleccionada simultaneamente (Solo verdadero o falso)"""
    def __init__(self, parent, nombre, args):
        """Recibe la lista de elementos"""
        ElementoWidgetOpciones.__init__(self)
        QGridButtonGroup.__init__(self, parent)
        self.setTitle(nombre)
        for elemento in args:
            caja = QCheckBox(self)
            caja.setText(elemento)
            self.insert(caja)
            self.diccionario[elemento] = caja

    def opciones(self):
        """Devuelve las opciones seleccionadas"""
        dic = {}
        for pareja in self.diccionario.iteritems():
            if pareja[1].isChecked():
                dic[pareja[0]] = True
        return dic
    

class EWOSeleccionSimple(ElementoWidgetOpciones, QHButtonGroup):
    """Es una lista en la que solo puede ser seleccionado uno de sus elementos.
    Los elementos son escogidos con un despegable"""
    def __init__(self, parent, nombre, args):
        """Recibe la lista de elementos"""
        QHButtonGroup.__init__(self, parent, "SeleccionSimple")
        ElementoWidgetOpciones.__init__(self)
        self.nombre = nombre
        self.setTitle(nombre)
        self.setExclusive(True)
        for elemento in args:
            boton = QRadioButton(self)
            boton.setText(elemento)
            self.insert(boton)
            self.diccionario[elemento] = boton
        self.find(0).setOn(True)

    def opciones(self):
        """Devuelve las opciones seleccionadas"""
        dic = {}
        for pareja in self.diccionario.iteritems():
            if pareja[1].isChecked():
                dic[self.nombre] = pareja[0]
        return dic

    def activar(self):
        """Activa el widget"""
        for boton in self.diccionario.values():
            boton.setEnabled(True)

    def desactivar(self):
        """Desactiva el widget"""
        for boton in self.diccionario.values():
            boton.setEnabled(False)

class EWOListaSimple(ElementoWidgetOpciones, QGroupBox):
    """Es una lista de opciones en la que solo puede ser seleccionado uno de sus elementos.
    Todos los elementos son mostrados simultaneamente"""
    def __init__(self, parent, nombre, lista):
        """el ultimo parametro es la lista de posibles valores"""
        ElementoWidgetOpciones.__init__(self)
        QGroupBox.__init__(self, parent, "ListaSimple")
        self.nombre = nombre
        self.setTitle(nombre)
        self.setColumnLayout(0, Qt.Vertical)
        self.layout().setSpacing(6)
        self.layout().setMargin(11)
        llayout = QVBoxLayout(self.layout())
        llayout.setAlignment(Qt.AlignTop)
        layout12 = QHBoxLayout(None, 0, 6, "layout12")
        label = QLabel(self, "label")
        layout12.addWidget(label)
        spacer7 = QSpacerItem(51, 31, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout12.addItem(spacer7)
        
        self.combo1 = QComboBox(0, self, "comboBox1")
        layout12.addWidget(self.combo1)
        spacer8 = QSpacerItem(131, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout12.addItem(spacer8)
        llayout.addLayout(layout12)


        for elemento in lista:
            self.combo1.insertItem(elemento)    

    def opciones(self):
        """Devuelve las opciones seleccionadas"""
        dic = {self.nombre:self.combo1.currentText().latin1()}
        return dic
    
class EWOEntradaTexto(ElementoWidgetOpciones, QHBox):
    """Es una entrada de texto, con un nombre, que devuelve un valor insertado por el usuario"""
    def __init__(self, parent, nombre, valorpordefecto = ""):
        ElementoWidgetOpciones.__init__(self)
        QHBox.__init__(self, parent, "EntradaTexto")
        self.__etiqueta = QLabel(nombre, self)
        self.__entrada = QLineEdit(self, "Linea")
        self.__entrada.setText(valorpordefecto)
        self.nombre = nombre

    def opciones(self):
        """Devuelve las opciones seleccionadas"""
        if self.__entrada.text():
            return {self.nombre:self.__entrada.text().latin1()}
        else:
            return {}

    def activar(self):
        """Activa el widget"""
        self.__entrada.setEnabled(True)

    def desactivar(self):
        """Desactiva el widget"""
        self.__entrada.setEnabled(False)

class EWOGrupoWidgetOpciones(ElementoWidgetOpciones, QVGroupBox, ContenedorElementoWidgetOpciones):
    """Contiene a un conjunto de opciones, todas ellas activables por un QCheckBox"""
    def __init__(self, parent, nombre):
        ElementoWidgetOpciones.__init__(self)
        QVGroupBox.__init__(self, parent, "ContenedorOpcional")
        ContenedorElementoWidgetOpciones.__init__(self)
        self.nombre = nombre
        self.checkbox = QCheckBox(self, "checkBox1")
        self.checkbox.setText(nombre)
        self.setTitle(nombre)
        self.__conexiones()

    def __conexiones(self):
        """Bloque de conexiones"""
        self.connect(self.checkbox, SIGNAL("toggled(bool)"), self.__cambiar_estado)

    def procesar(self, diccionario):
        """Acciones a relizar cuando se nos pasa un diccionario con widgets"""
        ContenedorElementoWidgetOpciones.procesar(self, diccionario)
        self.__cambiar_estado()

    def __cambiar_estado(self):
        """Acciones a realizar cuando se detecta un cambio de estado en el widget"""
        valor = self.checkbox.isChecked()

        for widget in self.lista:
            if valor: 
                widget.activar()
            else: 
                widget.desactivar()

    def opciones(self):
        """Devuelve las opciones seleccionadas"""
        if self.checkbox.isChecked():
            diccionario = {}
            diccionario.update({self.nombre:ContenedorElementoWidgetOpciones.opciones(self)})
            return diccionario
        else:
            return {}

class EWOListaFactores(ElementoWidgetOpciones, QHGroupBox):
    """Lista de variables Factores del programa"""
    def __init__(self, parent, nombre, datos):
        ElementoWidgetOpciones.__init__(self)
        QHGroupBox.__init__(self, parent, "Lista factores")
        self.setTitle(nombre)
        self.nombre = nombre
        from Driza.iuqt3.widgetsqt import WidgetListaComboBoxFact
        self.variables = WidgetListaComboBoxFact(self, datos) #Por defecto sin factores

    def opciones(self):
        """Devuelve las opciones seleccionadas"""
        return {self.nombre:self.variables.currentText().latin1()}

class EWOListaVariables(ElementoWidgetOpciones, QHGroupBox):
    """Widget que permite elegir un elemento de la lista de todas las variables que no son factores"""
    def __init__(self, parent, nombre, datos):
        ElementoWidgetOpciones.__init__(self)
        QHGroupBox.__init__(self, parent, "Texto")
        self.setTitle(nombre)
        self.nombre = nombre
        from Driza.iuqt3.widgetsqt import WidgetListaComboBoxVars
        self.variables = WidgetListaComboBoxVars(self, datos, factores=False) #Por defecto sin factores

    def opciones(self):
        """Devuelve las opciones seleccionadas"""
        return {self.nombre:self.variables.currentText().latin1()}

class EWOEtiqueta(ElementoWidgetOpciones, QHGroupBox):
    """Muestra la etiqueta texto, y tiene el nombre nombre"""
    def __init__(self, parent, nombre, texto):
        ElementoWidgetOpciones.__init__(self)
        QHGroupBox.__init__(self, parent, "Texto")
        self.setTitle(nombre)
        self.label = QLabel(texto, self)

