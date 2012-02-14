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

"""Dialogo de operaciones"""

from qt import QListViewItem, SIGNAL, QLabel, QErrorMessage
from Driza.iuqt3.ui.doperaciones import DialogoOperaciones
from Driza.categorias import GestorCategorias
import logging
LOG = logging.getLogger("Driza.iuqt3.operaciones.doperaciones")

def conv_arbol_listview(padre, arbol):
    """Convierte un arbol en formato listview. Recursiva"""
    nuevarama = QListViewItem(padre, arbol.contenido)
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
    if not listviewitem.firstChild():
        #Elemento final
        return [listviewitem, Set([listviewitem.text(0).latin1()])]
    else:
        elemento = listviewitem.firstChild()
        listahijos = []
        while elemento:
            listahijos.append(elemento)
            elemento = elemento.nextSibling()
        listasalida = []
        for hijo in listahijos:
            listaresultado = listview_elementos_finales(hijo)
            if len(listaresultado) == 2 and isinstance(listaresultado[1], Set):
                if isinstance(listviewitem, QListViewItem):
                    listaresultado[1].add(listviewitem.text(0).latin1())
                listasalida.append(listaresultado)
            else:
                for resultado in listaresultado:
                    if isinstance(listviewitem, QListViewItem):
                        resultado[1].add(listviewitem.text(0).latin1())
                    listasalida.append(resultado)
        return listasalida

def tags_de_item(item):
    """Obtiene los tags de un QListViewItem, leyendo los textos de todos sus ancestros.
    Es recursiva"""
    tags = []
    if isinstance(item, QListViewItem):
        tags.append(item.text(0).latin1())
        tags = tags_de_item(item.parent()) + tags
    return tags

class DOperaciones(DialogoOperaciones):
    """Dialogo  de operaciones. Muestra las operaciones disponibles
    Y ademas muestra el woperaciones de la operación actualmente seleccionada
    """

    def __init__(self, parent, idu, gestoroperaciones, vsalida):
        self.__diccionariowidgets = {}
        self.__init_dic_widgets()
        self.__gestorcategorias = GestorCategorias()
        DialogoOperaciones.__init__(self, parent, "Dialogo casos", 0, 0)
        self.__idu = idu
        self.__gestoroperaciones = gestoroperaciones
        self.__init_widgets_operaciones()
        self.__init_arbol()
        self.__conexiones()
        self.__vsalida = vsalida
        self.listView2.setRootIsDecorated(True)
        self.listView2.addColumn("Operaciones")
        self.__operacion = None #Guarda la operacion actual
        self.__init_widgets_categorias()
        self.__init_dic_widgets_otros()

    def accept(self):
        """Acepta el dialogo. Coge la operacion con la que esta trabajando 
        el usuario e inicia el procedimiento de calculo"""
        from Driza.excepciones import OpcionesIncorrectaException
        from rpy import RException
        nombre = unicode(self.listView2.currentItem().text(0).latin1(),'iso-8859-1')
        widget = self.__diccionariowidgets["operaciones"][nombre]
        try:
            resultado = self.__gestoroperaciones[nombre].procedimiento(widget.seleccion(), widget.opciones())
        except OpcionesIncorrectaException:
            QErrorMessage(self, "error").message(u"Las opciones no son correctas")
        except IndexError:
            QErrorMessage(self, "error").message(u"Seleccion Incorrecta")
            LOG.exception("excepcion capturada")
        except KeyError:
            mensaje = u"Hay elementos de la salida sin definir(o mal definidos) en la operación"
            QErrorMessage(self, "error").message(mensaje)
            LOG.exception("Excepción Generada por un módulo de operaciones")
        except RException:
            QErrorMessage(self, "error").message(u"R devolvio un error")
            LOG.exception("Excepción de RPY")
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
        DialogoOperaciones.showEvent(self, ev)

    #MIEMBROS PRIVADOS

    def __cambiar_elemento(self):
        """Procedimiento que actualiza el widget en función de la selección del arbol"""
        self.__operacion = unicode(self.listView2.currentItem().text(0).latin1(), 'iso-8859-1')
        self.__mostrar_widget()

    def __conexiones(self):
        """Bloque de conexiones"""
        self.connect(self.listView2, SIGNAL("selectionChanged ()"), self.__cambiar_elemento)
        self.connect(self.pushButton2, SIGNAL("clicked()"), self.reject)
        self.connect(self.pushButton1, SIGNAL("clicked()"), self.accept)


    def __init_arbol(self):
        """Inicializa el arbol con todas las operaciones conocidas
        """
        self.listView2.clear()
        listalistasetiquetas = [operacion.etiquetas for operacion in self.__gestoroperaciones.values()]
        from Driza import categorias
        from sets import Set
        arbol = categorias.conv_categorias_arbol("Raiz", listalistasetiquetas)
        for hijo in arbol.enlaces:
            conv_arbol_listview(self.listView2, hijo)
        #FIXME No todos las operaciones van en elementos finales. conv_arbol_listview esta mal
        listaelementosfinales = listview_elementos_finales(self.listView2)
        for operacion in self.__gestoroperaciones.values():
            for elementofinal in listaelementosfinales:
                if Set(operacion.etiquetas) == elementofinal[1]:
                    QListViewItem(elementofinal[0], operacion.nombre)

    def __init_dic_widgets(self):
        """Inicializa los diccionarios de widgets, que permiten el acceso posterior a estos"""
        self.__diccionariowidgets["categorias"] = {}
        self.__diccionariowidgets["operaciones"] = {}
        self.__diccionariowidgets["otros"] = {}

    def __init_dic_widgets_otros(self):
        """Inicializa el diccionario de widgets en la categoria otros"""
        noimplementado = QLabel(None, "No implementado")
        noimplementado.setText("No implementado")
        condicionesincorrectas = QLabel(None, "No se dan las condiciones adecuadas")
        condicionesincorrectas.setText("No se dan las condiciones adecuadas")
        self.__diccionariowidgets["otros"]["condicionesincorrectas"] = condicionesincorrectas
        self.__diccionariowidgets["otros"]["noimplementado"] = noimplementado
        self.widgetStack1.addWidget(noimplementado)
        self.widgetStack1.addWidget(condicionesincorrectas)
    
    def __init_widgets_categorias(self):
        """Inicializa los widgets de cada categoria"""
        from sets import ImmutableSet
        for categoria in self.__gestorcategorias.listacategorias:
            tmpset = ImmutableSet(categoria.etiquetas)
            label = QLabel(None, "")
            label.setAlignment(QLabel.WordBreak)
            label.setText(categoria.descripcion)
            self.__diccionariowidgets["categorias"][tmpset] = label
            self.widgetStack1.addWidget(label)

    def __init_widgets_operaciones(self):
        """Añade los widgets en el widgetstack y en el diccionario de widgets"""
        for titulo, operacion in self.__gestoroperaciones.items():
            widget = self.__render_widget(titulo, operacion.widget)
            self.__diccionariowidgets["operaciones"][titulo] = widget
            self.widgetStack1.addWidget(widget)

    def __myUpdate(self):
        """Es llamado por showEvent, garantiza la actualización de los elementos"""
        self.__mostrar_arbol()
        self.__mostrar_widget()

    def __render_widget(self, nombre, diccionariowidget):
        """Renderiza un widget a partir de una descripcion en dicccionario"""
        from Driza.listas import TIPOSWIDGETOPERACIONESQT3
        if not TIPOSWIDGETOPERACIONESQT3.has_key(diccionariowidget["tipo"]):
            raise NameError
        from Driza.iuqt3.operaciones.woperaciones import WidgetOperacionSelectorOpcion
        widget = WidgetOperacionSelectorOpcion(nombre, \
                TIPOSWIDGETOPERACIONESQT3[diccionariowidget["tipo"]]["seleccion"], \
                diccionariowidget["opciones"], self.__idu)
        return widget

    def __mostrar_arbol(self):
        """Muestra el arbol segun el contenido de gestoroperaciones"""
        self.listView2.ensureItemVisible(self.listView2.findItem(self.__operacion, 0))
        self.listView2.setCurrentItem(self.listView2.findItem(self.__operacion, 0))

    def __mostrar_widget(self):
        """Muestra el widget asociado a la seleccion actual"""
        from sets import Set, ImmutableSet
        nombre = unicode(self.listView2.currentItem().text(0).latin1(),'iso-8859-1')
        listaetiquetas = self.__tags()
        LOG.debug('mostrando widget:' + nombre)
        if self.__gestoroperaciones.has_key(nombre) and \
                Set(listaetiquetas[:-1]) == Set(self.__gestoroperaciones[nombre].etiquetas): 
            if self.__gestoroperaciones.funcionchequeocondiciones(nombre):
                self.widgetStack1.raiseWidget(self.__diccionariowidgets["operaciones"][nombre])
            else:
                self.widgetStack1.raiseWidget(self.__diccionariowidgets["otros"]["condicionesincorrectas"])
        elif self.__gestorcategorias.obtener_categoria_aprox(listaetiquetas) != False:
            labelaprox = ImmutableSet(self.__gestorcategorias.obtener_categoria_aprox(listaetiquetas).etiquetas)
            self.widgetStack1.raiseWidget(self.__diccionariowidgets["categorias"][labelaprox])
        else:
            LOG.debug("No encontro widget apropiado para la categoria")
            self.widgetStack1.raiseWidget(self.__diccionariowidgets["otros"]["noimplementado"])

    def __tags(self):
        """Devuelve las tags asociadas al item actual"""
        return tags_de_item(self.listView2.currentItem())



