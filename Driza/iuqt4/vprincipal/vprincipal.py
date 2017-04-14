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

"""Ventana principal"""

from PyQt4 import QtCore,QtGui
from PyQt4.QtGui import QMessageBox,QIcon
from Driza.iuqt4.ui.vprincipal import Ui_VentanaPrincipal
from Driza.iuqt4.dconfig import DConfig
from Driza.iuqt4.dbuscar import DBuscar
from Driza.iuqt4.operaciones.doperaciones import DOperaciones
#from Driza.iu.dimportartexto import DImportarTexto
from Driza.iuqt4.dfiltrado import DFiltrado
from Driza.iuqt4.vsalida import VSalida
from grid import Grid
from Driza import gestores
from Driza import operaciones
from Driza.listas import SL
from Driza.datos import datos
from Driza.datos import interfaces
import string
import logging
LOG = logging.getLogger(__name__)

class VPrincipal(QtGui.QMainWindow):
    """Ventana principal, hereda de vprincipal, que esta generado por el designer. 
    Esta clase es padre de la mayoria de los dialogos, y es la que permite introducir los datos a el usuario"""

    def __init__(self, parent, config, portero, idu, gestorproyectos, gestortemas, gestoroperaciones): 
        """Inicializador de la ventana principal"""
        QtGui.QMainWindow.__init__(self,None)
        self.ui=Ui_VentanaPrincipal()
        self.ui.setupUi(self)
        self.stackedWidget=self.ui.stackedWidget
        gestorsalida = gestores.GestorSalida()
        vsalida = VSalida(self,gestorsalida,gestortemas)
        idf = interfaces.InterfazDatosFicheros(portero)
        idr = interfaces.InterfazDatosR(portero)
        #VARIABLES PUBLICAS
        self.parent = parent
        self.__config = config
        self.__gestortemas = gestortemas
        self.__idu = idu
        #Bloque de inicialización de dialogos
        self.__dbuscar = DBuscar(self,"busqueda")
        self.__dconfig = DConfig(config,self)
        self.__dfiltro = DFiltrado(self,self.__idu)
        #self.__dimportartexto=DImportarTexto(self,idf)
        self.__portero = portero
        self.__gestorproyectos = gestorproyectos
        self.grid = Grid(self, self.__idu, self.__portero)
        self.stackedWidget.addWidget(self.grid)
        self.stackedWidget.setCurrentWidget(self.grid)
        # Funciones de inicializacion de componentes
        self.__init_toolbar()
        self.mostrar_undo_redo()

        #self.setIcon(self.__gestortemas.iconoprograma())
        self.__diccionarioarbolmenu = {}
        self.__diccionarioacciones = {}
        self.__colectorfunciones = []
        listalistasetiquetas = [operacion.etiquetas for operacion in gestoroperaciones.values()]
        from Driza import categorias
        arbol = categorias.conv_categorias_arbol("Raiz", listalistasetiquetas)
        LOG.debug("Arbol generado:"+str(arbol))
        self.__conv_arbol_menu(self.ui.menuAnalizar , arbol, self.__diccionarioarbolmenu)
        listaelementosmenu =  self.__lista_etiquetas_menu(self.__diccionarioarbolmenu, [])
        from sets import Set
        for operacion in gestoroperaciones.values():
            LOG.debug("Operacion procesada para generar el menu")
            for elementofinal in listaelementosmenu:
                LOG.debug("Elemento final procesado para generar el menu")
                if Set(operacion.etiquetas) == Set(elementofinal[1]):
                    LOG.debug("Elemento final encontrado, generando hoja")
                    accion = QtGui.QAction(self)
                    accion.setText(unicode(operacion.nombre))
                    elementofinal[0].addAction(accion)
                    self.__diccionarioacciones[operacion.nombre] = accion
        #self.__atajos()

    #FUNCIONES PUBLICAS
    
    def abrir_proyecto(self, parent = None, filename = None):
        """ Lanza el diálogo de apertura de fichero """
        from Driza.excepciones import FicheroNoExisteException, FicheroErroneoException,FicheroTipoDesconocidoException
        if not parent: 
            parent = self
        if not self.__dproyecto_modificado(): 
            return
        if not filename:
            filtro = ""
            for fmt in SL.extensiones_fichero:
                filtro = filtro + "%s files (*.%s);;" % (fmt, string.lower(fmt))
            from PyQt4.QtGui import QFileDialog
            from PyQt4.QtCore import QString
            filename = QFileDialog.getOpenFileName(self, "Dialogo abrir fichero", "", filtro)
            filename = str(filename)
        if filename:
            try:
                self.__gestorproyectos.cargar(filename)
            except FicheroErroneoException:
                QMessageBox.warning(parent, u'Atención', 'El fichero no ha podido ser leido')
            except FicheroTipoDesconocidoException:
                QMessageBox.warning(parent, u'Atención', 'El fichero no ha podido ser leido')
            except FicheroNoExisteException:
                QMessageBox.warning(parent, u'Atención', 'El fichero no ha podido ser leido')
            except AttributeError:
                QErrorMessage(parent, "Error").message(u"Parece que ha intentado cargar un fichero de una versión anterior. Lo siento")
                LOG.exception("excepcion capturada")
            else:
                self.__myUpdate()
                self.grid.myUpdate()
                return True
        return False

    def __myUpdate(self):
        """Acciones de actualizacion"""
        from Driza import VERSION
        if self.__gestorproyectos.fichero:
            nfichero = self.__gestorproyectos.fichero
        else:
            nfichero = "Nuevo fichero"
        self.setWindowTitle("Driza " + VERSION + " - " + nfichero)

    def showEvent(self, ev):
        self.__myUpdate()
        QtGui.QMainWindow.showEvent(self, ev)

    def closeEvent(self, ev):
        """Acciones que se realizaran cuando el usuario cierre la ventana. Guarda el estado de la configuración, 
        incluyendo los ficheros recientemente abiertos"""
        if not self.__dproyecto_modificado(): 
            return
        if not self.parent.vsalida.isVisible():
            self.__config.guardar()
            QtGui.qApp.exit(0)
        else:
            self.hide()
    
    def mostrar_undo_redo(self):
        """Determina que botones estan activados y cuales no del submenu de edición"""
        if self.__portero.puedo_undo():
            self.ui.actionDeshacer.setEnabled(True)
        else:
            self.ui.actionDeshacer.setEnabled(False)

        if self.__portero.puedo_redo():
            self.ui.actionRehacer.setEnabled(True)
        else:
            self.ui.actionRehacer.setEnabled(False)

    #FUNCIONES PRIVADAS

    def __importar(self):
        """Importa los datos de un fichero"""
        if not self.__dproyecto_modificado(): 
            return
        self.parent.dimportartexto.show()

    def __dproyecto_modificado(self):
        """Pregunta en caso de que haya sido modificado el proyecto si desea ser guardado"""
        if not self.__idu.original():
            returncode = QMessageBox.information(self, 'Atencion:', 'El proyecto actual ha sido modificado, desea guardarlo?', 'Guardarlo', 'No guardarlo', 'Volver', 0, 1)
            if returncode == 0:
                self.__guardar()
            elif returncode == 2:
                return False
        return True


    def __dacerca_de(self):
        """Mensaje acerca de"""
        from Driza import VERSION
        separador = "<hr>"
        ristra ="<html>"
        betatesters = u"Carlos Mestre Gonzalez <br> Luis de Bethencourt Guimerá"
        iconos = "Iconos del Tango Desktop Project: http://tango.freedesktop.org/"
        ristra += u"Driza %s es una interfaz estadística <br> (C) Néstor Arocha Rodríguez - Tutorizado por Inmaculada luengo Merino<br> Distribuido bajo licencia GPL" +\
                separador + "Betatesters:\n" + betatesters + separador + iconos + "</html>"
        QMessageBox.about(self, "Acerca de Driza", ristra % (VERSION))
    
    def __undo(self):
        """Deshace el último cambio"""
        self.__portero.undo()
        self.grid.myUpdate()
        self.mostrar_undo_redo()
    
    def __redo(self):
        """Rehace el último cambio"""
        self.__portero.redo()
        self.grid.myUpdate()
        self.mostrar_undo_redo()

    def __init_toolbar(self):
        """Inicializa la toolbar"""
        #self.setIconSize(QtCore.QSize(64,64))
        #self.ui.toolBar.setIconSize(QtCore.QSize(64,64))
        self.__boton1 = QtGui.QToolButton(self.ui.toolBar)
        self.ui.toolBar.addWidget(self.__boton1)
        self.__boton1.setText("ABRIR")
        icono=QIcon()
        icono.addPixmap(self.__gestortemas.icono_abrir())
        self.__boton1.setIcon(icono)
        self.__boton2 = QtGui.QToolButton(self.ui.toolBar)
        self.__boton2.setText("GUARDAR")
        icono = QIcon()
        icono.addPixmap(self.__gestortemas.icono_guardar())
        self.__boton2.setIcon(icono)
        self.ui.toolBar.addWidget(self.__boton2)

    def conexiones(self):
        """Funcion llamada en el constructor que almacena todas las conexiones accion-funcion"""
        from PyQt4.QtCore import SIGNAL
        self.connect(self.ui.actionSalir,SIGNAL("triggered()"),self.__salir_programa)
        self.connect(self.ui.actionNuevo_proyecto,SIGNAL("triggered()"),self.__nuevo)
        self.connect(self.ui.actionAbrir_Proyecto,SIGNAL("triggered()"),self.abrir_proyecto)
        self.connect(self.ui.actionGuardar_como,SIGNAL("triggered()"),self.__guardar_como)
        self.connect(self.ui.actionGuardar,SIGNAL("triggered()"),self.__guardar)
        self.connect(self.ui.actionImportar,SIGNAL("triggered()"),self.__importar)
        self.connect(self.ui.actionConfiguraci_n,SIGNAL("triggered()"),self.__dconfig.show)
        self.connect(self.ui.actionFiltrar,SIGNAL("triggered()"),self.__dfiltro.show)
        self.connect(self.ui.actionCrear_nuevas_variables,SIGNAL("triggered()"),self.parent.dcrevar.show)
        self.connect(self.ui.actionBuscar,SIGNAL("triggered()"),self.__dbuscar.show)
        self.connect(self.ui.actionCopiar,SIGNAL("triggered()"),self.__copiar)
        self.connect(self.ui.actionCotar,SIGNAL("triggered()"),self.__cortar)
        self.connect(self.ui.actionPegar,SIGNAL("triggered()"),self.__pegar)
        self.connect(self.ui.actionDeshacer,SIGNAL("triggered()"),self.__undo)
        self.connect(self.ui.actionRehacer,SIGNAL("triggered()"),self.__redo)
        self.connect(self.ui.actionBorrar,SIGNAL("triggered()"),self.__borrar)
        self.connect(self.ui.actionAcerca, SIGNAL("triggered()"), self.__dacerca_de)
        self.connect(self.__boton1, SIGNAL("clicked()"), self.abrir_proyecto)
        self.connect(self.__boton2, SIGNAL("clicked()"), self.__guardar)
        #self.__conexionesanalizar()
        for (key, valor) in self.__diccionarioacciones.items():
            self.__colectorfunciones.append(lambda k=key: self.parent.doperaciones.mostrar(k))
            self.connect(valor, SIGNAL("activated()"), self.__colectorfunciones[-1])



    def __copiar(self):
        """Funcion que copia y borra la seleccion"""
        try:
            self.__copiar_privado()
        except AssertionError:
            QMessageBox.warning(self, u'Atención', 'Las operaciones de copiado, cortado y pegado no han sido implementadas')
        else:
            self.grid.borrar_seleccion() 

   #http://www.google.com/codesearch?hl=en&q=+%22qtable%22+%22cut%22+%22paste%22+show:z9otKZeV6U8:R6dK3Cx-dYg:Gh37-3Ie27E&sa=N&cd=48&ct=rc&cs_p=http://mde.abo.fi/confluence/download/attachments/1011/coral-0.9.1.tar.gz&cs_f=coral-0.9.1/coral/modeler/property/propertyeditor.py#a0 
    def __cortar(self):
        """Copia, borra la seleccion y su contenido"""
        from Driza.excepciones import SeleccionIncorrectaException
        try:
            self.grid.verificar_seleccion_registros()
            self.__portero.guardar_estado()
            self.__copiar_privado()
        except SeleccionIncorrectaException:
            QMessageBox.warning(self, u'Atención', 'Solo se permite cortar registros')
        except AssertionError:
            QMessageBox.warning(self, u'Atención', 'Las operaciones de copiado, cortado y pegado no han sido implementadas')
        else:
            self.grid.borrar_seleccion(borrardatos=True)
            self.grid.myUpdate()


    def __pegar(self):
        """Funcion que envuelve a __pegar recogiendo sus excepciones"""
        #TODO Capturar otras excepciones
        try:
            self.__pegar_privado()
        except AssertionError:
            QErrorMessage(self, "Error").message(u"Error desconocido")
            LOG.exception("excepcion capturada en el pegado")


    def __pegar_privado(self):
        """Pega lo que haya sido copiado"""
        clipboard = QApplication.clipboard()
        registro = clipboard.text().latin1()
        lista = eval(registro)
        pos = self.grid.table1.currentRow()
        lista.reverse() #Escribimos los registros al reves para que queden ordenados
        if pos > self.__idu.numReg():
            for x in range(self.__idu.numReg(),pos):
                self.__idu.appReg()
        #Hacemos el pegado efectivo
        for registro in lista:
            self.__idu.insReg(pos,registro)
        self.grid.myUpdate()

    def __salir_programa(self):
        """Funcion de salida del programa. Guarda la configuracion"""
        if not self.__dproyecto_modificado(): 
            return
        self.__config.guardar()
        QtGui.qApp.exit(0)


    def __nuevo(self):
        """Accion realizada cuando el usuario clickea en Nuevo"""
        if not self.__dproyecto_modificado(): 
            return
        self.__idu.borrar_todo()
        self.__gestorproyectos.fichero = None
        self.__myUpdate()
        self.grid.myUpdate()


    
    def __guardar(self):
        """Funcion de guardado del fichero. Si el fichero no es conocido se llama a guardarcomo"""
        if self.__gestorproyectos.fichero:
            self.__gestorproyectos.guardar(sobreescribir = True)
            self.__idu.establecer_original()
        else:
            self.__guardar_como()

    def __guardar_como(self):
        """Abre un diálogo pidiendo el nombre de archivo y guarda en dicho archivo"""
        filtro = ""
        for fmt in SL.extensiones_fichero:
            filtro = filtro+ "%s files (*.%s);;" % (fmt, string.lower(fmt))
        from PyQt4.QtGui import QFileDialog
        fn = QFileDialog.getSaveFileName(self,"Dialogo guardarFichero","",filtro)
        filename = str(fn)
        if filename:
            from Driza.excepciones import FicheroExisteException,FicheroTipoDesconocidoException
            import re
            extension = re.compile('.*\..*')
            if not extension.match(filename):
                filename += ".driza"
            try:
                self.__gestorproyectos.guardar(filename)
            except FicheroExisteException, fichero:
                returncode = QMessageBox.information(self, 'Atencion:', 'El fichero' + fichero.fichero + ' ya existe' , 'Sobreescribir', 'Otro nombre', 'Cancelar', 0, 1)
                if returncode == 0:
                    self.__gestorproyectos.guardar(filename, True)
                    self.__idu.establecer_original()
                    self.__myUpdate()
                elif returncode == 1:
                    self.__guardarcomo()
            except FicheroTipoDesconocidoException:
                QMessageBox.warning(self, u'Atención', u'La extensión del fichero es incorrecta.\nPruebe con otra extensión')
                self.__gestorproyectos.fichero = None
            else:
                self.__idu.establecer_original()
                self.__myUpdate()

                    
    def __copiar_privado(self):
        """Esta funcion pega el contenido del clipboard en la tabla actual"""
        tablaactual = self.grid.currentPageIndex()
        assert(tablaactual == 0) #TODO Cambiar por una excepcion más concreta
        lista = self.grid.lista_seleccion()
        cadena = repr(lista)
        clipboard = QApplication.clipboard()
        clipboard.setData(QTextDrag(cadena))
            

    def __borrar(self):
        """Borra la seleccion"""
        self.grid.borrar_seleccion(borrardatos = True)
        self.grid.myUpdate()

    def __conv_arbol_menu(self, padre, arbol, diccionario):
        """Convierte un arbol a formato menu.  Recursiva"""
        from PyQt4.QtCore import QString
        for hijo in arbol.enlaces:
            nuevarama = QtGui.QMenu(QString(str(hijo.contenido)),self)
            padre.addMenu(nuevarama)
            diccionario[str(hijo.contenido)] = {"objeto":nuevarama}
            self.__conv_arbol_menu(nuevarama, hijo, diccionario[str(hijo.contenido)])

    def __lista_etiquetas_menu(self, diccionario, etiquetasanteriores):
        """Devuelve una lista con parejas qpopup, listatags"""
        lista = []
        for (indice, valor) in diccionario.items():
            if isinstance(valor, dict):
                nuevasetiquetas = etiquetasanteriores[:]
                nuevasetiquetas.append(indice)
                for resultado in self.__lista_etiquetas_menu(valor, nuevasetiquetas):
                    lista.append(resultado)
            else:
                lista.append([valor, etiquetasanteriores])
        return lista


