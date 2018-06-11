#!/usr/bin/python
# -*- coding: utf-8 -*-


#Copyright (C) 2008  Néstor Arocha Rodríguez
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

"""Dialogo de operaciones"""
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QLabel, QTreeWidget, QTreeWidgetItem, QErrorMessage
from pyrqt.iuqt4.ui.doperaciones import Ui_DialogoOperaciones
from pyrqt.categorias import GestorCategorias
from sets import ImmutableSet
import logging
LOG = logging.getLogger("__name__")

def conv_arbol_listview(padre, arbol):
    """Convierte un arbol en formato listview. Recursiva"""
    nuevarama = QTreeWidgetItem(padre, [arbol.contenido])
    for hijo in arbol.enlaces:
        conv_arbol_listview(nuevarama, hijo)

def listview_elementos_finales(listviewitem):
    """Devuelve una lista de listas con los siguientes elementos:
    -Objetolistviewitem
    -Set(etiqueta1,etiqueta2...)
    La lista solo contiene aquellos elementos que no tienen hijos(finales)
    """
    #FIXME: Requiere que listview tenga al menos un item
    from sets import Set
    if isinstance (listviewitem,QTreeWidget):
        listahijos = []
        for indice in range (listviewitem.topLevelItemCount()):
            listahijos.append(listviewitem.topLevelItem(indice))
        return formarcategoriasdesdehijos(listviewitem, listahijos)

    if not listviewitem.child(0):
        #Elemento final
        return [listviewitem, Set([listviewitem.text(0)])]

    else:
        elemento = listviewitem.child(0)
        listahijos = []
        while elemento:
            listahijos.append(elemento)
            elemento = elemento.parent().child(elemento.parent().indexOfChild(elemento)+1)
        return formarcategoriasdesdehijos(listviewitem, listahijos)

def formarcategoriasdesdehijos(listviewitem, listahijos):
    from sets import Set
    listasalida = []
    for hijo in listahijos:
        listaresultado = listview_elementos_finales(hijo)
        if len(listaresultado) == 2 and isinstance(listaresultado[1], Set):
            if isinstance(listviewitem, QTreeWidgetItem):
                listaresultado[1].add(listviewitem.text(0))
            listasalida.append(listaresultado)
        else:
            for resultado in listaresultado:
                if isinstance(listviewitem, QTreeWidgetItem):
                    resultado[1].add(listviewitem.text(0))
                listasalida.append(resultado)
    return listasalida


def tags_de_item(item):
    """Obtiene los tags de un QListViewItem, leyendo los textos de todos sus ancestros.
    Es recursiva"""
    tags = []
    if isinstance(item, QListViewItem):
        tags.append(item.text(0))
        tags = tags_de_item(item.parent()) + tags
    return tags

class DOperaciones(QtGui.QDialog):
    """Dialogo  de operaciones. Muestra las operaciones disponibles
    Y ademas muestra el woperaciones de la operación actualmente seleccionada
    """

    def __init__(self, parent, idu, gestoroperaciones, vsalida):
        self.__widgets = {}
        self.__init_dic_widgets()
        self.__gestorcategorias = GestorCategorias
        QtGui.QDialog.__init__(self, parent)
        self.ui=Ui_DialogoOperaciones()
        self.ui.setupUi(self)
        self.__idu = idu
        self.__gestoroperaciones = gestoroperaciones
        self.__init_widgets_operaciones()
        self.__init_arbol()
        self.__conexiones()
        self.__vsalida = vsalida
        self.ui.treeWidget.setRootIsDecorated(True)
        #self.ui.treeWidget.addColumn("Operaciones")
        self.__operacion = None #Guarda la operacion actual
        self.__init_widgets_categorias()
        self.__init_dic_widgets_otros()

    def accept(self):
        """Acepta el dialogo. Coge la operacion con la que esta trabajando 
        el usuario e inicia el procedimiento de calculo"""
        from pyrqt.excepciones import OpcionesIncorrectaException
        import rpy
        nombre = unicode(self.ui.treeWidget.currentItem().text(0))
        widget = self.__widgets["operaciones"][nombre]
        try:
            resultado = self.__gestoroperaciones[nombre].procedimiento(widget.seleccion(), widget.opciones())
        except OpcionesIncorrectaException:
            errormessage = QErrorMessage(self)
            errormessage.showMessage(u"Las opciones no son correctas")
        #except IndexError:
        #    errormessage = QErrorMessage(self)
        #    errormessage.showMessage(u"Seleccion incorrecta")
        #    LOG.exception("excepcion capturada")
        except KeyError:
            QErrorMessage(self,"error").message(u"Hay elementos de la salida sin definir(o mal definidos) en la operación")
            LOG.exception("Excepción Generada por un módulo de operaciones")
        except rpy.RException:
            QErrorMessage(self, "error").message(u"R devolvio un error")
            log.exception("Excepción de RPY")
        except AssertionError:
            QErrorMessage(self, "error").message(u"Error desconocido")
        else:
            self.__vsalida.ana_res(resultado) #Añadir a la salida el resultado
            self.__vsalida.hide() #TODO averiguar como hacer para que recupere el foco sin ocultar la ventana
            self.__vsalida.show()

    def mostrar(self, operacion):
        """Muestra el dialogo con la operacion pasada"""
        self.__operacion = operacion
        LOG.debug("Mostrando operacion:" + operacion)
        self.show()

    def showEvent(self, ev):
        """Redefinición showEvent"""
        self.__myUpdate()

    #MIEMBROS PRIVADOS

    def __cambiar_elemento(self):
        """Procedimiento que actualiza el widget en función de la selección del arbol"""
        LOG.debug("__cambiar_elemento: BEGIN")
        self.__operacion = unicode(self.ui.treeWidget.currentItem().text(0),'iso-8859-1')
        self.__mostrar_widget()

    def __conexiones(self):
        """Bloque de conexiones"""
        from PyQt4.QtCore import SIGNAL
        self.connect(self.ui.treeWidget,SIGNAL("itemSelectionChanged()"),self.__cambiar_elemento)
        self.connect(self.ui.pushButton2,SIGNAL("clicked()"),self.reject)
        self.connect(self.ui.pushButton1,SIGNAL("clicked()"),self.accept)


    def __init_arbol(self):
        """Inicializa el arbol con todas las operaciones conocidas
        """
        self.ui.treeWidget.clear()
        listalistasetiquetas = [operacion.etiquetas for operacion in self.__gestoroperaciones.values()]
        from pyrqt import categorias
        from sets import Set
        arbol = categorias.conv_categorias_arbol("Raiz", listalistasetiquetas)
        #toplevel = QTreeWidgetItem(["Operaciones"])
        #self.ui.treeWidget.addTopLevelItem(toplevel)
        for hijo in arbol.enlaces:
            conv_arbol_listview(self.ui.treeWidget, hijo)
        #FIXME No todos las operaciones van en elementos finales. conv_arbol_listview esta mal
        listaelementosfinales = listview_elementos_finales(self.ui.treeWidget)
        for operacion in self.__gestoroperaciones.values():
            for elementofinal in listaelementosfinales:
                if Set(operacion.etiquetas) == Set(map(str,elementofinal[1])):
                    QTreeWidgetItem(elementofinal[0], [operacion.nombre])

    def __init_dic_widgets(self):
        """Inicializa los diccionarios de widgets, que permiten el acceso posterior a estos"""
        self.__widgets["categorias"] = {}
        self.__widgets["operaciones"] = {}
        self.__widgets["otros"] = {}

    def __init_dic_widgets_otros(self):
        """Inicializa el diccionario de widgets en la categoria otros"""
        noimplementado = QLabel(None)
        noimplementado.setText("No implementado")
        condicionesincorrectas = QLabel(None)
        condicionesincorrectas.setText("No se dan las condiciones adecuadas")
        self.__widgets["otros"]["condicionesincorrectas"] = condicionesincorrectas
        self.__widgets["otros"]["noimplementado"] = noimplementado
        self.ui.stackedWidget.addWidget(noimplementado)
        self.ui.stackedWidget.addWidget(condicionesincorrectas)
    def __init_widgets_categorias(self):
        """Inicializa los widgets de cada categoria"""
        for categoria, values in self.__gestorcategorias.categorias.items():
            tmpset = ImmutableSet(values)
            label = QLabel(None)
            #label.setAlignment(QLabel.AlignLeft)
            label.setText(categoria)
            self.__widgets["categorias"][tmpset] = label
            self.ui.stackedWidget.addWidget(label)

    def __init_widgets_operaciones(self):
        """Añade los widgets en el widgetstack y en el diccionario de widgets"""
        for titulo, operacion in self.__gestoroperaciones.items():
            widget = self.__render_widget(titulo, operacion.widget)
            self.__widgets["operaciones"][titulo] = widget
            self.ui.stackedWidget.addWidget(widget)

    def __myUpdate(self):
        """Es llamado por showEvent, garantiza la actualización de los elementos"""
        self.__mostrar_arbol()
        self.__mostrar_widget()

    def __render_widget(self, nombre, diccionariowidget):
        """Renderiza un widget a partir de una descripcion en dicccionario"""
        from pyrqt.listas import SL
        if not SL.TIPOSWIDGETOPERACIONESQT4.has_key(diccionariowidget["tipo"]):
            raise NameError
        from pyrqt.iuqt4.operaciones.woperaciones import WidgetOperacionSelectorOpcion
        widget = WidgetOperacionSelectorOpcion(nombre, \
                SL.TIPOSWIDGETOPERACIONESQT4[diccionariowidget["tipo"]]["seleccion"], \
                diccionariowidget["opciones"], self.__idu)
        return widget

    def __mostrar_arbol(self):
        """Muestra el arbol segun el contenido de gestoroperaciones"""
        #FIXME No deberia ser rellenado más de una vez
        currentitemcandidatelist = self.ui.treeWidget.findItems(self.__operacion,Qt.MatchContains and Qt.MatchRecursive)
        if currentitemcandidatelist != []:
            currentitem = currentitemcandidatelist[0]
            self.ui.treeWidget.scrollToItem(currentitem)
            self.ui.treeWidget.setCurrentItem(currentitem)

    def __mostrar_widget(self):
        """Muestra el widget asociado a la seleccion actual"""
        if not self.ui.treeWidget.currentItem(): 
            return
        nombre = unicode(self.ui.treeWidget.currentItem().text(0))
        LOG.debug("__mostrar_widget nombre:" + nombre)
        if self.__gestoroperaciones.has_key(nombre):
            if self.__gestoroperaciones.funcionchequeocondiciones(nombre):
                self.ui.stackedWidget.setCurrentWidget(self.__widgets["operaciones"][nombre])
            else:
                self.ui.stackedWidget.setCurrentWidget(self.__widgets["otros"]["condicionesincorrectas"])
        elif any(nombre in x for x in self.__gestorcategorias.categorias.values()):
            category_set = [x for x in self.__gestorcategorias.categorias.values() if nombre in x][0]
            category_set = ImmutableSet(category_set)
            self.ui.stackedWidget.setCurrentWidget(self.__widgets['categorias'][category_set])
        else:
            self.ui.stackedWidget.setCurrentWidget(self.__widgets["otros"]["noimplementado"])
