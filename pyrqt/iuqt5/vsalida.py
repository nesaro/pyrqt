#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2018  Néstor Arocha Rodríguez

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

"""vsalida.py: Ventana que muestra los resultados de las operaciones solicitadas"""

from PyQt4 import QtCore,QtGui
from PyQt4.QtGui import QToolButton, QWidget
from pyrqt.iuqt4.ui.vsalida import Ui_VentanaSalida

class VSalida(QtGui.QMainWindow):
    """Ventana que muestra los resultados de las operaciones solicitadas. 
    Permite al usuario exportar o guardar los resultados ya obtenidos"""
    def __init__(self, parent, gestorsalida, gestortemas):
        QtGui.QMainWindow.__init__(self)
        self.ui=Ui_VentanaSalida()
        self.ui.setupUi(self)
        #VARIABLES PUBLICAS
        self.__parent = parent
        #VARIABLES PRIVADAS
        self.__gestortemas = gestortemas
        self.__gestorsalida = gestorsalida
        self.__contenido = []

        self.__inittoolbar()
        self.__conexiones()

    #FUNCIONES PUBLICAS

    def ana_res(self, objeto):
        """Añade un resultado al dialogo, para ser mostrado"""
        self.__contenido.append(objeto)

    def __myUpdate(self):
        """Actualiza el contenido de la ventana"""
        cadenasalida = ""
        i = 1
        for resultado in self.__contenido:
            cadenasalida += "<a name=" + str(i) + "></a>"
            cadenasalida += resultado.html()
            i += 1
        self.ui.textBrowser.setText(cadenasalida)
        self.ui.textBrowser.scrollToAnchor(str(len(self.__contenido)))
        self.__actualizar_lista()

    def closeEvent( self, event ):
        """Redefinicion del closeEvent de qt"""
        QWidget.closeEvent( self, event )
        if not self.__parent.vprincipal.isVisible():
            QtCore.qApp.exit(0)
        else:
            self.hide()

    def showEvent(self, ev):
        """Redefinicion del método show de VentanaSalida, 
        muestra todos los resultados almacenados"""
        self.__myUpdate()

    #FUNCIONES PRIVADAS

    def __conexiones(self):
        """Bloque de conexiones"""
        from PyQt4.QtCore import SIGNAL
        self.connect(self.ui.actionAbrir,SIGNAL("triggered()"),self.__dabrirfichero)
        self.connect(self.ui.actionGuardar,SIGNAL("triggered()"),self.__dguardarfichero)
        self.connect(self.ui.actionExportar,SIGNAL("triggered()"),self.__dexportar)
        self.connect(self.ui.actionSalir,SIGNAL("triggered()"),self.hide)
        self.connect(self.__boton1,SIGNAL("clicked()"),self.__dabrirfichero)
        self.connect(self.__boton2,SIGNAL("clicked()"),self.__dguardarfichero)
        self.connect(self.__boton3,SIGNAL("clicked()"),self.__dexportar)
        #self.connect(self.__boton4,SIGNAL("clicked()"),self.__parent.vprincipal.show)
        #self.connect(self.ui.pushButton1,SIGNAL("clicked()"),self.__borrar_elemento)

    def __inittoolbar(self):
        """Inicializa la toolbar"""
        self.__boton1=QToolButton(self.ui.toolBar)
        #TODO Pendiente Qt4
        #self.boton1.setTextLabel("Abrir fichero")
        #iconos=QIconSet()
        #iconos.setIconSize(QIconSet.Small,QSize(100,100))
        #iconos.setPixmap(self.__gestortemas.iconoabrir(),QIconSet.Small)
        #self.boton1.setOn(True)
        #self.boton1.setIconSet(iconos)
        self.__boton2=QToolButton(self.ui.toolBar)
        #self.boton2.setTextLabel("Guardar en fichero")
        #iconos=QIconSet()
        #iconos.setIconSize(QIconSet.Small,QSize(100,100))
        #iconos.setPixmap(self.__gestortemas.iconoguardar(),QIconSet.Small)
        #self.boton2.setOn(True)
        #self.boton2.setIconSet(iconos)
        self.__boton3=QToolButton(self.ui.toolBar)
        #self.boton3.setTextLabel("Exportar a html")
        #iconos=QIconSet()
        #iconos.setIconSize(QIconSet.Small,QSize(100,100))
        #iconos.setPixmap(self.__gestortemas.iconoexportar(),QIconSet.Small)
        #self.boton3.setOn(True)
        #self.boton3.setIconSet(iconos)
        self.__boton4=QToolButton(self.ui.toolBar)

    def __dabrirfichero(self):        
        """Pregunta al usuario que fichero cargar"""
        filterlist = ""
        for fmt in ["dro"]: #Candidata al fichero de listas
            filterlist = filterlist + "%s files (*.%s);;" % (fmt, fmt.lower())
        nombrefichero = QtGui.QFileDialog.getOpenFileName(filter=filterlist,
                                                          parent=self,
                                                          caption="Dialogo abrir fichero")
        filename = str(nombrefichero)
        if filename:
            try:
                self.__contenido = self.__gestorsalida.cargar(filename)
            except AttributeError: 
                QErrorMessage(self,"Error").message(u"Error en la carga de fichero, Probablemente versión anterior")
            else:
                self.__myUpdate()

    def __dguardarfichero(self):
        """Pregunta al usuario en que fichero guardar"""
        filterlist = ""
        for fmt in ["dro"]: #Candidata al fichero de listas
            filterlist = filterlist + "%s files (*.%s);;" % (fmt, fmt.lower())
        nombrefichero = QtGui.QFileDialog.getSaveFileName(filter=filterlist,
                                                          parent=self,
                                                          )
        filename = str(nombrefichero)
        if filename:
            from pyrqt.excepciones import FicheroExisteException, \
                    FicheroTipoDesconocidoException
            import re
            extension = re.compile('.*\..*')
            if not extension.match(filename):
                filename+=".dro"
            try:
                self.__gestorsalida.guardar(self.__contenido, filename)
            except FicheroExisteException as e:
                fichero = e.fichero
                codigoretorno = QtGui.QMessageBox.information(self, 'Atencion:', 'El fichero' +\
                        str(fichero) + ' ya existe' , 'Sobreescribir', \
                        'Otro nombre', 'Cancelar', 0, 1)
                if codigoretorno == 0:
                    self.__gestorsalida.guardar(self.__contenido, filename, True)
                elif codigoretorno == 1:
                    self.__dguardarfichero()
            except FicheroTipoDesconocidoException:
                QtGui.QMessageBox.warning(self, u'Atención', \
                        u'La extensión del fichero es incorrecta.\nPruebe con otra extensión')

    
    def __dexportar(self):
        """Pregunta al usuario en que fichero exportar"""
        filterlist = ""
        for fmt in ["html"]: #Candidata al fichero de listas
            filterlist = filterlist + "%s files (*.%s);;" % (fmt, fmt.lower())
        nombrefichero = QtGui.QFileDialog.getSaveFileName(self,
                                                          filterlist,
                                                          )
        filename = str(nombrefichero)
        if filename:
            self.__exportar(filename)

    def __exportar(self, fichero):
        """Exporta un fichero a html"""
        import re
        regexp = re.compile('.*\.html$')
        if not regexp.match(fichero):
            fichero += ".html"
        archivo = open(fichero, 'w')
        #Obtenido de: http://xahlee.org/perl-python/split_fullpath.html
        import os
        (nombredirectorio, nombrefichero) = os.path.split(fichero)
        (basenombrefichero, _)=os.path.splitext(nombrefichero)
        os.mkdir(nombredirectorio + "/"+ basenombrefichero)
        for resultado in self.__contenido:
            ristra = resultado.exportarhtml(nombredirectorio+"/" + basenombrefichero)
            archivo.write(ristra.encode('iso-8859-1', 'replace'))

    def __actualizar_lista(self):
        """Actualiza la lista de elementos mostrados"""
        self.ui.listWidget.clear()
        i = 0
        for elemento in self.__contenido:
            self.ui.listWidget.insertItem(i, str(elemento.titulo))
            i += 1

    def __borrar_elemento(self):
        """Borra el elemento seleccionado en la lista de elementos"""
        if self.ui.listWidget.currentItem():
            del self.__contenido[self.ui.listWidget.currentItem()]
            self.__myUpdate()
