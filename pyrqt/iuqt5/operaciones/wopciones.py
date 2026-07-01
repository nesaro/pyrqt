#!/usr/bin/python
# -*- coding: utf-8 -*-


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

from pyrqt.iuqt4.widgetsqt import QGridButtonGroup
from PyQt4 import QtCore,QtGui

"""Clases relacionadas con los widgets de opciones"""

class ContenedorElementoWidgetOpciones:
    """Contiene las funciones de adición de widgets necesaria para los contenedores"""
    def __init__(self):
            """Inicializa la lista de los elementos que contiene el contenedor"""
            self.lista=[]

    def parse(self, diccionario):
        """Transforma un diccionario con el nombre y las opciones de un widget en el propio widget"""
        if diccionario:
            if diccionario["tipo"]=="EntradaTexto":
                if diccionario["valorpordefecto"]:
                    self.addETS(diccionario["nombre"],diccionario["valorpordefecto"])
                else:
                    self.addETS(diccionario["nombre"])
            elif diccionario["tipo"]=="SeleccionSimple":
                self.addSSB(diccionario["nombre"],diccionario["opciones"])
            elif diccionario["tipo"]=="SeleccionMultiple":
                self.addSMB(diccionario["nombre"],diccionario["opciones"])
            elif diccionario["tipo"]=="ListaSimple":
                self.addLS(diccionario["nombre"],diccionario["opciones"])
            elif diccionario["tipo"]=="Texto":
                self.addT(diccionario["nombre"],diccionario["texto"],diccionario["valorpordefecto"])
            elif diccionario["tipo"]=="Variables":
                self.addV(diccionario["nombre"])
            elif diccionario["tipo"]=="Factores":
                self.addLF(diccionario["nombre"])
        
    def addSMB(self,nombre,args):
        """"Añade un widget de seleccion multiple booleana al contenedor"""
        widget=EWOSeleccionMultiple(self,nombre,args)
        self.lista.append(widget)

    def addSSB(self,nombre,args):
        widget=EWOSeleccionSimple(self,nombre,args)
        self.lista.append(widget)

    def addLS(self,nombre,args):
        widget=EWOListaSimple(self,nombre,args)
        self.lista.append(widget)

    def addCO(self,nombre):
        """Añade un Contenedor Opcional"""
        widget=EWOGrupoWidgetOpciones(self,nombre)
        self.lista.append(widget)

    def addETS(self,nombre,valorpordefecto=""):
        """Añade un Contenedor Opcional"""
        widget=EWOEntradaTexto(self,nombre,valorpordefecto)
        self.lista.append(widget)

    def addLF(self,nombre):
        """Añade una lista de factores"""
        widget=EWOListaFactores(self,nombre,self._dato)
        self.lista.append(widget)

    def addT(self,nombre,args):
        widget=EWOEtiqueta(self,nombre,args)
        self.lista.append(widget)

    def addV(self,nombre):
        widget=EWOListaVariables(self,nombre,self._dato)
        self.lista.append(widget)

    def opciones(self):
        """Devuelve un diccionario con las opciones y sus valores [Virtual]"""
        diccionario={}
        for elemento in self.lista:
            diccionario.update(elemento.opciones())
        return diccionario

class WOpciones(QtGui.QWidget, ContenedorElementoWidgetOpciones):
    """Cualquier widget que tenga un conjunto de opciones"""
    def __init__(self, interfazdatos):
        QtGui.QWidget.__init__(self)#,None,"Widget opciones")
        #QtGui.QFrame.__init__(self)#,None,"Widget opciones")
        ContenedorElementoWidgetOpciones.__init__(self)
        #TODO Pendiente portabilidad qt4
        #self.clearWState(Qt.WState_Polished)
        #self.setCaption("WidgetOpciones")
        self._dato=interfazdatos

class ElementoWidgetOpciones:
    """Clase padre de cualquier elemento que pertenezca a widgetopciones"""
    def __init__(self):
        self.diccionario={}

    def opciones(self):
        pass

    def activar(self):
        pass

    def desactivar(self):
        pass

class EWOSeleccionMultiple(ElementoWidgetOpciones,QGridButtonGroup):
    """Es una lista de opciones que pueden ser seleccionada simultaneamente (Solo verdadero o falso)"""
    def __init__(self,parent,nombre,args):
        """Recibe la lista de elementos"""
        ElementoWidgetOpciones.__init__(self)
        QGridButtonGroup.__init__(self,parent,"SeleccionMultiple")
        self.setTitle(nombre)
        for elemento in args:
            caja=QCheckBox(self)
            caja.setText(elemento)
            self.insert(caja)
            self.diccionario[elemento]=caja

    def opciones(self):
        dic={}
        for pareja in self.diccionario.iteritems():
            if pareja[1].isChecked():
                dic[pareja[0]]=True
        return dic
    

class EWOSeleccionSimple(ElementoWidgetOpciones,QtGui.QButtonGroup): #Era qHbuttongrup
    """Es una lista en la que solo puede ser seleccionado uno de sus elementos.
    Los elementos son escogidos con un despegable"""
    def __init__(self,parent,nombre,args):
        """Recibe la lista de elementos"""
        QtGui.QHButtonGroup.__init__(self,parent,"SeleccionSimple")
        ElementoWidgetOpciones.__init__(self)
        self.nombre=nombre
        self.setTitle(nombre)
        self.setExclusive(True)
        for elemento in args:
            boton=QRadioButton(self)
            boton.setText(elemento)
            self.insert(boton)
            self.diccionario[elemento]=boton
        self.find(0).setOn(True)
    def opciones(self):
        dic={}
        for pareja in self.diccionario.iteritems():
            if pareja[1].isChecked():
                dic[self.nombre]=pareja[0]
        return dic

    def activar(self):
        for boton in self.diccionario.values():
            boton.setEnabled(True)

    def desactivar(self):
        for boton in self.diccionario.values():
            boton.setEnabled(False)

class EWOListaSimple(ElementoWidgetOpciones,QtGui.QGroupBox):
    """Es una lista de opciones en la que solo puede ser seleccionado uno de sus elementos.
    Todos los elementos son mostrados simultaneamente"""
    def __init__(self,parent,nombre,lista):
        """el ultimo parametro es la lista de posibles valores"""
        ElementoWidgetOpciones.__init__(self)
        QtGui.QGroupBox.__init__(self,parent,"ListaSimple")
        self.nombre=nombre
        self.setTitle(nombre)
        self.setColumnLayout(0,Qt.Vertical)
        self.layout().setSpacing(6)
        self.layout().setMargin(11)
        llayout = QVBoxLayout(self.layout())
        llayout.setAlignment(Qt.AlignTop)
        #Pegado del original

        layout12 = QHBoxLayout(None,0,6,"layout12")
        
        self.textLabel1_2 = QLabel(self,"textLabel1_2")
        layout12.addWidget(self.textLabel1_2)
        spacer7 = QSpacerItem(51,31,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout12.addItem(spacer7)
        
        self.comboBox1 = QComboBox(0,self,"comboBox1")
        layout12.addWidget(self.comboBox1)
        spacer8 = QSpacerItem(131,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout12.addItem(spacer8)
        llayout.addLayout(layout12)


        for elemento in lista:
            self.comboBox1.insertItem(elemento)    

    def opciones(self):
        dic={self.nombre:self.comboBox1.currentText().latin1()}
        return dic
    
class EWOEntradaTexto(ElementoWidgetOpciones,QtGui.QHBoxLayout):
    """Es una entrada de texto, con un nombre, que devuelve un valor insertado por el usuario"""
    def __init__(self,parent,nombre,valorpordefecto=""):
        ElementoWidgetOpciones.__init__(self)
        QtGui.QHBoxLayout.__init__(self,parent,"EntradaTexto")
        self.__etiqueta=QLabel(nombre,self)
        self.__entrada=QLineEdit(self,"Linea")
        self.__entrada.setText(valorpordefecto)
        self.nombre=nombre

    def opciones(self):
        if self.__entrada.text():
            return {self.nombre:self.__entrada.text().latin1()}
        else:
            return {}

    def activar(self):
        self.__entrada.setEnabled(True)

    def desactivar(self):
        self.__entrada.setEnabled(False)

class EWOGrupoWidgetOpciones(ElementoWidgetOpciones,QtGui.QGroupBox,ContenedorElementoWidgetOpciones): #era qvgroupbox
    """Contiene a un conjunto de opciones, todas ellas activables por un QCheckBox"""
    def __init__(self,parent,nombre):
        ElementoWidgetOpciones.__init__(self)
        QtGui.QGroupBox.__init__(self,parent,"ContenedorOpcional")
        ContenedorElementoWidgetOpciones.__init__(self)
        self.nombre=nombre
        self.checkbox=QCheckBox(self,"checkBox1")
        self.checkbox.setText(nombre)
        self.setTitle(nombre)
        self.__conexiones()

    def __conexiones(self):
        self.connect(self.checkbox,SIGNAL("toggled(bool)"),self.__cambiarestado)

    def parse(self,diccionario):
        ContenedorElementoWidgetOpciones.parse(self,diccionario)
        self.__cambiarestado()

    def __cambiarestado(self):
        valor=self.checkbox.isChecked()

        for x in self.lista:
            if valor: x.activar()
            else: x.desactivar()

    def opciones(self):
        if self.checkbox.isChecked():
            diccionario={}
            diccionario.update({self.nombre:ContenedorElementoWidgetOpciones.opciones(self)})
            return diccionario
        else:
            return {}

class EWOListaFactores(ElementoWidgetOpciones,QtGui.QGroupBox): #era hgroupbox
    """Lista de variables Factores del programa"""
    def __init__(self,parent,nombre,datos):
        ElementoWidgetOpciones.__init__(self)
        QtGui.QGroupBox.__init__(self,parent,"Lista factores")
        self.setTitle(nombre)
        self.nombre = nombre
        from pyrqt.widgets.widgetsqt import WidgetListaComboBoxFact
        self.variables=WidgetListaComboBoxFact(self,datos) #Por defecto sin factores

    def opciones(self):
        return {self.nombre:self.variables.currentText().latin1()}

class EWOListaVariables(ElementoWidgetOpciones,QtGui.QGroupBox): #Era QHgroupBox
    """Widget que permite elegir un elemento de la lista de todas las variables que no son factores"""
    def __init__(self,parent,nombre,datos):
        ElementoWidgetOpciones.__init__(self)
        QtGui.QGroupBox.__init__(self,parent,"Texto")
        self.setTitle(nombre)
        self.nombre = nombre
        from pyrqt.widgets.widgetsqt import WidgetListaComboBoxVars
        self.variables=WidgetListaComboBoxVars(self,datos,factores=False) #Por defecto sin factores

    def opciones(self):
        return {self.nombre:self.variables.currentText().latin1()}

class EWOEtiqueta(ElementoWidgetOpciones,QtGui.QGroupBox): #Era  QHgroupBox
    """Muestra la etiqueta texto, y tiene el nombre nombre"""
    def __init__(self, parent, nombre, texto):
        ElementoWidgetOpciones.__init__(self)
        QtGui.QGroupBox.__init__(self,parent,"Texto")
        self.setTitle(nombre)
        self.label=QLabel(texto,self)

