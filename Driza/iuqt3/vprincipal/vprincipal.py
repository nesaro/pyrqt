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

"""Ventana principal"""


from qt import SIGNAL, QMessageBox, QErrorMessage, QFileDialog, qApp, QApplication, QToolButton, QIconSet, QWidget, QSize, QAction, QTextDrag, QString, QPopupMenu
from Driza.iuqt3.ui.vprincipal import vprincipal
from Driza.iuqt3.dconfig import DConfig
from Driza.iuqt3.dbuscar import DBuscar
from Driza.iuqt3.dfiltrado import DFiltrado
from Driza.iuqt3.dayuda import DAyuda
from Driza.iuqt3.vprincipal.grid import Grid
from Driza.listas import SL
import logging
LOG = logging.getLogger("Driza.iuqt3.vprincipal.vprincipal")

class VPrincipal(vprincipal):
    """Ventana principal, hereda de vprincipal, que esta generado por el designer.
    Esta clase es padre de la mayoria de los dialogos, y es la que permite introducir los datos a el usuario"""



    def __init__(self, parent, config, portero, idu, gestorproyectos, gestortemas, gestoroperaciones): 
        """Inicializador de la ventana principal"""
        vprincipal.__init__(self, None)
        #VARIABLES PUBLICAS
        self.parent = parent
        self.__config = config
        self.__gestortemas = gestortemas
        self.__idu = idu
        #Bloque de inicialización de dialogos
        self.__dbuscar = DBuscar(self, "busqueda")
        self.__dconfig = DConfig(config, self)
        self.__dfiltro = DFiltrado(self, self.__idu)
        self.__dayuda = DAyuda(self)
        self.__portero = portero
        self.__gestorproyectos = gestorproyectos
        self.grid = Grid(self, self.__idu, self.__portero)
        self.widgetStack1.addWidget(self.grid)
        self.widgetStack1.raiseWidget(self.grid)

        # Funciones de inicializacion de componentes
        self.__init_toolbar()
        self.mostrar_undo_redo()

        self.setIcon(self.__gestortemas.icono_programa())
        self.__diccionarioarbolmenu = {}
        self.__diccionarioacciones = {}
        self.__colectorfunciones = []
        listalistasetiquetas = [operacion.etiquetas for operacion in gestoroperaciones.values()]
        from Driza import categorias
        arbol = categorias.conv_categorias_arbol("Raiz", listalistasetiquetas)
        self.__conv_arbol_menu(self.Analizar, arbol, self.__diccionarioarbolmenu)
        listaelementosmenu =  self.__lista_etiquetas_menu(self.__diccionarioarbolmenu, [])
        from sets import Set
        for operacion in gestoroperaciones.values():
            for elementofinal in listaelementosmenu:
                if Set(operacion.etiquetas) == Set(elementofinal[1]):
                    accion = QAction(self, "")
                    accion.setText(unicode(operacion.nombre))
                    accion.addTo(elementofinal[0])
                    self.__diccionarioacciones[operacion.nombre] = accion
        self.__atajos()


    #FUNCIONES PUBLICAS
    
    def abrir_proyecto(self, parent = None, filename = None):
        """ Lanza el diálogo de apertura de fichero """
        from Driza.excepciones import FicheroNoExisteException, FicheroErroneoException, FicheroTipoDesconocidoException
        if not parent: 
            parent = self
        if not self.__dproyecto_modificado(): 
            return
        if not filename:
            filtro = ""
            for fmt in SL.extensiones_fichero:
                filtro = filtro + "%s files (*.%s);;" % (fmt, fmt.lower())
            filename = QFileDialog.getOpenFileName(QString.null, filtro, self, None, "Dialogo abrir fichero", "")
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
        self.setCaption("Driza " + VERSION + " - " + nfichero)

    def showEvent(self, event):
        self.__myUpdate()
        vprincipal.showEvent(self, event)

    def closeEvent(self, event):
        """Acciones que se realizaran cuando el usuario cierre la ventana. Guarda el estado de la configuración,
        incluyendo los ficheros recientemente abiertos"""
        if not self.__dproyecto_modificado(): 
            return
        QWidget.closeEvent(self, event)
        if not self.parent.vsalida.isVisible():
            self.__config.guardar()
            qApp.exit(0)
        else:
            self.hide()
    
    def mostrar_undo_redo(self):
        """Determina que botones estan activados y cuales no del submenu de edición"""
        if self.__portero.puedo_undo():
            self.editUndoAction.setEnabled(True)
        else:
            self.editUndoAction.setEnabled(False)

        if self.__portero.puedo_redo():
            self.editRedoAction.setEnabled(True)
        else:
            self.editRedoAction.setEnabled(False)

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
        separador = "\n----------------------------------\n"
        betatesters = u"Carlos Mestre Gonzalez\n Luis de Bethencourt Guimerá"
        iconos = "Iconos del Tango Desktop Project: http://tango.freedesktop.org/"
        ristra = u"Driza %s es una interfaz estadística\n (C) Néstor Arocha Rodríguez - Tutorizado por Inmaculada luengo Merino\n Distribuido bajo licencia GPL" +\
                separador + "Betatesters:\n" + betatesters + separador +\
                u" Mantenedor del paquete .deb:\n Luis de Bethencourt Guimerá"+ separador + iconos
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
        self.__boton1 = QToolButton(self.Toolbar)
        self.__boton1.setTextLabel("ABRIR")
        iconos = QIconSet()
        iconos.setIconSize(QIconSet.Small, QSize(100, 100))
        iconos.setPixmap(self.__gestortemas.icono_abrir(), QIconSet.Small)
#        iconos.setPixmap("images/flechaabajo.png", QIconSet.Automatic, QIconSet.Normal, QIconSet.Off)
        self.__boton1.setOn(True)
        self.__boton1.setIconSet(iconos)
        self.__boton2 = QToolButton(self.Toolbar)
        self.__boton2.setTextLabel("GUARDAR")
        iconos = QIconSet()
        iconos.setIconSize(QIconSet.Small, QSize(100, 100))
        iconos.setPixmap(self.__gestortemas.icono_guardar(), QIconSet.Small)
        self.__boton2.setOn(True)
        self.__boton2.setIconSet(iconos)
        self.__boton3 = QToolButton(self.Toolbar)
        self.__boton3.setTextLabel("Ventana Salida")
        iconos = QIconSet()
        iconos.setIconSize(QIconSet.Small, QSize(100, 100))
        iconos.setPixmap(self.__gestortemas.icono_nueva_ventana(), QIconSet.Small)
        self.__boton3.setOn(True)
        self.__boton3.setIconSet(iconos)
        self.__boton4 = QToolButton(self.Toolbar)
        self.__boton4.setTextLabel("Mostrar etiquetas")
        self.__boton4.setToggleButton(True)
        iconos = QIconSet()
        iconos.setIconSize(QIconSet.Small, QSize(100, 100))
        iconos.setPixmap(self.__gestortemas.icono_etiquetas(), QIconSet.Small)
        self.__boton4.setIconSet(iconos)

    def conexiones(self):
        """Funcion llamada en el constructor que almacena todas las conexiones accion-funcion"""
        self.connect(self.archivoSalirAction, SIGNAL("activated()"), self.__salir_programa)
        self.connect(self.fileNewAction, SIGNAL("activated()"), self.__nuevo)
        self.connect(self.fileOpenAction, SIGNAL("activated()"), self.abrir_proyecto)
        self.connect(self.fileSaveAsAction, SIGNAL("activated()"), self.__guardar_como)
        self.connect(self.fileSaveAction, SIGNAL("activated()"), self.__guardar)
        self.connect(self.archivoImportarAction, SIGNAL("activated()"), self.__importar)
        self.connect(self.archivoConfiguracinAction, SIGNAL("activated()"), self.__dconfig.show)
        self.connect(self.datosFiltrarAction, SIGNAL("activated()"), self.__dfiltro.show)
        self.connect(self.modificarCrear_nuevas_variablesAction, SIGNAL("activated()"), self.parent.dcrevar.show)
        self.connect(self.editFindAction, SIGNAL("activated()"), self.__dbuscar.show)
        self.connect(self.editCopyAction, SIGNAL("activated()"), self.__copiar)
        self.connect(self.editCutAction, SIGNAL("activated()"), self.__cortar)
        self.connect(self.editPasteAction, SIGNAL("activated()"), self.__pegar)
        self.connect(self.editUndoAction, SIGNAL("activated()"), self.__undo)
        self.connect(self.editRedoAction, SIGNAL("activated()"), self.__redo)
        self.connect(self.edicinBorrarAction, SIGNAL("activated()"), self.__borrar)
        self.connect(self.edicinInsertarAction, SIGNAL("activated()"), self.__insertar_registro)
        self.connect(self.acerca_deAcerca_deAction, SIGNAL("activated()"), self.__dacerca_de)
        self.connect(self.__boton1, SIGNAL("clicked()"), self.abrir_proyecto)
        self.connect(self.__boton2, SIGNAL("clicked()"), self.__guardar)
        self.connect(self.__boton3, SIGNAL("clicked()"), self.parent.vsalida.show)
        self.connect(self.__boton4, SIGNAL("clicked()"), self.__alternar_etiquetas)
        self.connect(self.ayudaAyudaAction, SIGNAL("activated()"), self.__mostrar_dayuda)
        self.connect(self.PopupMenuEditor_3, SIGNAL("aboutToShow()"), self.__actualizar_recientes)
        for (key, valor) in self.__diccionarioacciones.items():
            self.__colectorfunciones.append(lambda k=key: self.parent.doperaciones.mostrar(k))
            self.connect(valor, SIGNAL("activated()"), self.__colectorfunciones[-1])

    def __atajos(self):
        """Establece los atajos"""
        self.ayudaAyudaAction.setAccel("F1")
        self.acciontab1 = QAction(self, "tabcasos")
        self.connect(self.acciontab1, SIGNAL("activated()"), self.grid.mostrar_t_reg)
        self.acciontab1.setAccel("F2")
        self.acciontab2 = QAction(self, "tabvars")
        self.connect(self.acciontab2, SIGNAL("activated()"), self.grid.mostrar_t_var)
        self.acciontab2.setAccel("F3")
        if self.__diccionarioacciones.has_key("Descriptivo"):
            self.__diccionarioacciones["Descriptivo"].setAccel("F4")
        self.__boton3.setAccel("F5") #Ventana salida
        self.archivoConfiguracinAction.setAccel("F10")
        self.acerca_deAcerca_deAction.setAccel("F12")
        self.archivoSalirAction.setAccel("Ctrl+Q")

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
        posrow = self.grid.table1.currentRow()
        poscol = self.grid.table1.currentColumn()
        if len(lista[0]) == self.__idu.n_var():
            poscol = 0 #Copia de registro completo
        else:
            #No permitimos pegar si el pegado implica variables nuevas
            assert(poscol + len(lista[0]) <= self.__idu.n_var())
        self.__portero.guardar_estado() #Guardamos el estado

        #Creamos nuevos registros hasta la posicion del cursor
        if posrow > self.__idu.n_reg():
            for _ in range(self.__idu.n_reg(), posrow):
                self.__idu.ana_reg()
        #Hacemos el pegado efectivo
        i = posrow
        for registro in lista:
            if i >= self.__idu.n_reg(): 
                self.__idu.ana_reg()
            j = poscol
            for campo in registro:
                if campo != None:
                    self.__idu[i][j] = campo
                j += 1
            i += 1
        self.grid.myUpdate()

    def __salir_programa(self):
        """Funcion de salida del programa. Guarda la configuracion"""
        if not self.__dproyecto_modificado(): 
            return
        self.__config.guardar()
        qApp.exit(0)


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
            filtro = filtro+ "%s files (*.%s);;" % (fmt, fmt.lower())
        filename = QFileDialog.getSaveFileName(QString.null, filtro, self)
        filename = str(filename)
        if filename:
            from Driza.excepciones import FicheroExisteException, FicheroTipoDesconocidoException
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
            
    def __mostrar_dayuda(self):
        self.__dayuda.mostrar("vprincipal")

    def __borrar(self):
        """Borra la seleccion"""
        self.grid.borrar_seleccion(borrardatos = True)
        self.grid.myUpdate()

    def __insertar_registro(self):
        """Inserta un registro, devolviendo un mensaje si ha habido un error"""
        try:
            self.grid.insertar_reg()
        except AssertionError:
            QMessageBox.warning(self, u'Atención', u'Error en la inserción')
            LOG.exception("excepcion capturada al insertar")

    def __alternar_etiquetas(self):
        """Alterna el modo etiqueta"""
        LOG.debug("Cambiado el modo etiqueta")
        self.grid.modoetiqueta = not self.grid.modoetiqueta
        self.grid.myUpdate()

    def __actualizar_recientes(self):
        """Actualiza la lista de ficheros recientemente abiertos"""
        self.PopupMenuEditor_3.clear()
        for i in range(len(self.__config.configuracion["lfichero"]) - 1):
            self.__colectorfunciones.append(lambda nombre=self.__config.configuracion["lfichero"][i]: self.abrir_proyecto(self, nombre))
            accion = QAction(self, self.__config.configuracion["lfichero"][i])
            accion.setText(self.__config.configuracion["lfichero"][i])
            accion.addTo(self.PopupMenuEditor_3)
            self.connect(accion, SIGNAL("activated()"), self.__colectorfunciones[-1])

    def __conv_arbol_menu(self, padre, arbol, diccionario):
        """Convierte un arbol a formato menu.  Recursiva"""
        for hijo in arbol.enlaces:
            nuevarama = QPopupMenu(self)
            padre.insertItem(QString(str(hijo.contenido)), nuevarama)
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

