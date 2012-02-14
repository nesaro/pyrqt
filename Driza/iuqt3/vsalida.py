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

"""vsalida.py: Ventana que muestra los resultados de las operaciones solicitadas"""

from Driza.iuqt3.ui.vsalida import VentanaSalida
from qt import QToolButton, QIconSet, QSize, QString, SIGNAL, QWidget, qApp, QFileDialog, QMessageBox, QErrorMessage

class VSalida(VentanaSalida):
    """Ventana que muestra los resultados de las operaciones solicitadas. 
    Permite al usuario exportar o guardar los resultados ya obtenidos"""
    def __init__(self, parent, gestorsalida, gestortemas):
        VentanaSalida.__init__(self)
        #VARIABLES PUBLICAS
        self.parent = parent
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
            cadenasalida += resultado.html().encode('iso-8859-1', 'replace')
            i += 1
        self.textBrowser1.setText(cadenasalida, "/tmp")
        self.textBrowser1.scrollToAnchor(str(len(self.__contenido)))
        self.__actualizar_lista()

    def closeEvent( self, event ):
        """Redefinicion del closeEvent de qt"""
        QWidget.closeEvent( self, event )
        if not self.parent.vprincipal.isVisible():
            qApp.exit(0)
        else:
            self.hide()

    def showEvent(self, event):
        """Redefinicion del método show de VentanaSalida, 
        muestra todos los resultados almacenados"""
        self.__myUpdate()
        VentanaSalida.showEvent(self, event)

    #FUNCIONES PRIVADAS

    def __conexiones(self):
        """Bloque de conexiones"""
        self.connect(self.archivoAbrirAction, SIGNAL("activated()"), self.__dabrirfichero)
        self.connect(self.archivoGuardarAction, SIGNAL("activated()"), self.__dguardarfichero)
        self.connect(self.archivoExportarHTMLAction, SIGNAL("activated()"), self.__dexportar)
        self.connect(self.archivoSalirAction, SIGNAL("activated()"), self.hide)
        self.connect(self.__boton1, SIGNAL("clicked()"), self.__dabrirfichero)
        self.connect(self.__boton2, SIGNAL("clicked()"), self.__dguardarfichero)
        self.connect(self.__boton3, SIGNAL("clicked()"), self.__dexportar)
        self.connect(self.__boton4, SIGNAL("clicked()"), self.parent.vprincipal.show)
        self.connect(self.pushButton1, SIGNAL("clicked()"), self.__borrar_elemento)

    def __inittoolbar(self):
        """Inicializa la toolbar"""
        self.__boton1 = QToolButton(self.Toolbar)
        self.__boton1.setTextLabel("Abrir fichero")
        iconos = QIconSet()
        iconos.setIconSize(QIconSet.Small, QSize(100, 100))
        iconos.setPixmap(self.__gestortemas.icono_abrir(), QIconSet.Small)
        self.__boton1.setOn(True)
        self.__boton1.setIconSet(iconos)
        self.__boton2 = QToolButton(self.Toolbar)
        self.__boton2.setTextLabel("Guardar en fichero")
        iconos = QIconSet()
        iconos.setIconSize(QIconSet.Small, QSize(100, 100))
        iconos.setPixmap(self.__gestortemas.icono_guardar(), QIconSet.Small)
        self.__boton2.setOn(True)
        self.__boton2.setIconSet(iconos)
        self.__boton3 = QToolButton(self.Toolbar)
        self.__boton3.setTextLabel("Exportar a html")
        iconos = QIconSet()
        iconos.setIconSize(QIconSet.Small, QSize(100, 100))
        iconos.setPixmap(self.__gestortemas.icono_exportar(), QIconSet.Small)
        self.__boton3.setOn(True)
        self.__boton3.setIconSet(iconos)
        self.__boton4 = QToolButton(self.Toolbar)
        self.__boton4.setTextLabel("Mostrar Ventana principal")
        iconos = QIconSet()
        iconos.setIconSize(QIconSet.Small, QSize(100, 100))
        iconos.setPixmap(self.__gestortemas.icono_nueva_ventana(), QIconSet.Small)
        self.__boton4.setOn(True)
        self.__boton4.setIconSet(iconos)

    def __dabrirfichero(self):        
        """Pregunta al usuario que fichero cargar"""
        filterlist = ""
        for fmt in ["dro"]: #Candidata al fichero de listas
            filterlist = filterlist + "%s files (*.%s);;" % (fmt, fmt.lower())
        nombrefichero = QFileDialog.getOpenFileName(QString.null, filterlist, self, None, "Dialogo abrir fichero", "")
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
        nombrefichero = QFileDialog.getSaveFileName(QString.null, filterlist, self)
        filename = str(nombrefichero)
        if filename:
            from Driza.excepciones import FicheroExisteException, \
                    FicheroTipoDesconocidoException
            try:
                self.__gestorsalida.guardar(self.__contenido, filename)
            except FicheroExisteException,fichero:
                codigoretorno = QMessageBox.information(self, 'Atencion:', 'El fichero' +\
                        fichero.fichero + ' ya existe' , 'Sobreescribir', \
                        'Otro nombre', 'Cancelar', 0, 1)
                if codigoretorno == 0:
                    self.__gestorsalida.guardar(self.__contenido, filename, True)
                elif codigoretorno == 1:
                    self.__dguardarfichero()
            except FicheroTipoDesconocidoException:
                QMessageBox.warning(self, u'Atención', \
                        u'La extensión del fichero es incorrecta.\nPruebe con otra extensión')

    
    def __dexportar(self):
        """Pregunta al usuario en que fichero exportar"""
        filterlist = ""
        for fmt in ["html"]: #Candidata al fichero de listas
            filterlist = filterlist + "%s files (*.%s);;" % (fmt, fmt.lower())
        nombrefichero = QFileDialog.getSaveFileName(QString.null, filterlist, self)
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
        self.listBox1.clear()
        i = 0
        for elemento in self.__contenido:
            self.listBox1.insertItem(unicode(elemento.titulo), i)
            i += 1

    def __borrar_elemento(self):
        """Borra el elemento seleccionado en la lista de elementos"""
        if self.listBox1.currentText():
            del self.__contenido[self.listBox1.currentItem()]
            self.__myUpdate()
