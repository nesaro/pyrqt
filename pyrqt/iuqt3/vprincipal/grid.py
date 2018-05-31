#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2006-2007   Néstor Arocha Rodríguez, Inmaculada Luengo Merino

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

"""Grid y clases asociadas"""

from qt import SIGNAL, QStringList, QString, QMessageBox, QTabWidget, \
        QWidget, QVBoxLayout, QInputDialog, QObject, QButton
from qttable import QTableItem, QTable, QComboTableItem
import logging
LOG = logging.getLogger("Driza.iu.widgets.grid")

#http://www.digitalfanatics.org/projects/qt_tutorial/chapter13.html
#http://www.handhelds.org/~zecke/apidocs/libopie/html/ocheckitem_8cpp-source.html
#Mirar tablestatistics.py de ejemplos de PyQT
#http://lists.trolltech.com/qt-interest/2005-10/thread00469-0.html

class ButtonTableItem(QTableItem):
    """Esta clase hereda de QTableItem. Modifica dos aspectos de estos:
        Por un lado inhabilita el texto que muestra normalmente
        Por otro, utiliza un botón para que al ser pulsado lanza el dialogo de casos
        """

    def __init__(self, tabla, dcasos):
        """la inicialización llama al padre"""
        QTableItem.__init__(self, tabla, QTableItem.WhenCurrent, "...") 
        self.setReplaceable(False)
        self.__dcasos = dcasos

    #FUNCIONES PUBLICAS
        
    def createEditor(self):
        """Crea un editor para interactuar con el contenido.
        En este caso es un botón, ya que permite asignar una acción al click de ratón"""
        boton = QButton(self.table().viewport(), "Ventana abierta") #El padre es viewport, es invisible
        QObject.connect(boton, SIGNAL("clicked()"), self.__editar)
        return boton

    def setContentFromEditor(self, widget):
        """Cuando el contenido de widget cambia, qt llama a esta función.
        Esta desactivada ya que el botón que actua de editor no dispone de información para devolver"""
        if isinstance(widget, QButton):
            self.setText("...")
        else:
            QTableItem.setContentFromEditor(self, widget)

    #FUNCIONES PRIVADAS
    def __editar(self):
        """Abre el dialogo de casos, pasando la columna como valor"""
        self.__dcasos.mostrar(self.row())



class  Grid(QTabWidget):
    """La tabla que manejara los registros y las variables"""

    #Funciones de inicializacion
    def __init__(self, padre, interfazdatos, porterodatos):
        from Driza.datos.conversion import AgenteConversion
        self.__portero = porterodatos
        QTabWidget.__init__(self, padre, "Grid")
        self.setTabPosition(QTabWidget.Bottom)
        self.tab = QWidget(self, "tab")
        tabLayout = QVBoxLayout(self.tab, 11, 6, "tabLayout")
        self.table1 = QTable(self.tab, "table1")
        tabLayout.addWidget(self.table1)
        self.insertTab(self.tab,  QString.fromLatin1("&Registros"))
        self.tab_2 = QWidget(self, "tab_2")
        tabLayout_2 = QVBoxLayout(self.tab_2, 11, 6, "tabLayout_2")
        self.table2 = QTable(self.tab_2, "table2")
        tabLayout_2.addWidget(self.table2)
        self.insertTab(self.tab_2, QString.fromLatin1("&Variables"))
        from Driza.iuqt3.vprincipal.dcasos import DCasos
        self.dcasos = DCasos(self.table1, interfazdatos)
        self.modoetiqueta = False # Variable que guarda si estamos en modo etiqueta o normal

        self.__nreg = 10 
        self.__nvar = 10
        self.__idu = interfazdatos
        self.__init_t_reg()
        self.__init_t_var()
        self.__conexiones()
        self.__agenteconversion = AgenteConversion(self.__idu)
        

    def __init_t_reg(self):
        """Inicializa la tabla de datos"""
        self.table1.setNumCols(16) 
        self.table1.setNumRows(64)
        for i in range(self.table1.horizontalHeader().count()):
            self.table1.horizontalHeader().setLabel(i+1, '')


    def __init_t_var(self):
        """Inicializa la tabla de variables"""
        self.table2.setSelectionMode(QTable.MultiRow)
        self.table2.setNumRows(self.__nvar)
        self.table2.setNumCols(5)
        titulos = self.table2.horizontalHeader()
        titulos.setLabel (0, "Nombre")
        titulos.setLabel (1, "Tipo")
        titulos.setLabel (2, "Valor por defecto")
        titulos.setLabel (3, u"Etiqueta")
        titulos.setLabel (4, u"Etiquetas de valor")

    def __conexiones(self):
        """Conexiones"""
        self.connect(self.table1, SIGNAL("valueChanged(int, int)"), self.__modificacion_t_reg)
        self.connect(self.table2, SIGNAL("valueChanged(int, int)"), self.__modificacion_t_var)

    def myUpdate(self):
        """Actualizacion de contenido"""
        LOG.debug("Actualizando contenido del grid")
        self.__mostrar_t_reg()
        self.__mostrar_t_var()

    def showEvent(self, event):
        """Redefinición del show de la clase base"""
        self.myUpdate()
        QTabWidget.showEvent(self, event)
        
    def borrar_seleccion(self, borrardatos=False):
        """Esta funcion borra la seleccion de la tabla. 
        El parametro opcional determina si se ha deborrar tambien los datos"""
        tablaactual = self.currentPageIndex()
        if tablaactual == 0:
            tabla = self.table1
        else:
            tabla = self.table2
        if borrardatos:
            lista = []
            for seleccion in range(tabla.numSelections()):
                for fila in range(tabla.selection(seleccion).topRow(), tabla.selection(seleccion).bottomRow()+1):
                    lista.append(fila)
            lista.sort()
            lista.reverse()
            for fila in lista:
                if tablaactual == 0:
                    if fila < self.__idu.n_reg():
                        del self.__idu[fila]
                else:
                    if fila < self.__idu.n_var():
                        self.__idu.delVar(fila)

        for seleccion in range(tabla.numSelections()):
            tabla.removeSelection(seleccion)

    def lista_seleccion(self, tabla=0):
        """Devuelve una lista con los registros que han sido seleccionados"""
        tabla = self.table1
        listasalida = []
        if tabla.numSelections():
            toprow = tabla.numRows()
            bottomrow = 0
            leftcol = tabla.numCols()
            rightcol = 0
            for seleccion in range(tabla.numSelections()):
                misel = tabla.selection(seleccion)
                if misel.topRow() < toprow: 
                    toprow = misel.topRow()
                if misel.bottomRow()> bottomrow: 
                    bottomrow = misel.bottomRow()
                if misel.leftCol()< leftcol: 
                    leftcol = misel.leftCol()
                if misel.rightCol()> rightcol: 
                    rightcol = misel.rightCol()
                LOG.debug("Limites totales de seleccion:("+str(toprow)+","+str(leftcol)+")")
                LOG.debug("Limites totales de seleccion:("+str(bottomrow)+","+str(rightcol)+")")
            if bottomrow >= self.__idu.n_reg(): 
                bottomrow = self.__idu.n_reg() - 1
            if rightcol >= self.__idu.n_var(): 
                rightcol = self.__idu.n_var() - 1
            for fila in range(toprow, bottomrow+1):
                nuevafila = []
                for columna in range(leftcol, rightcol+1):
                    if self.__idu[fila][columna].valido() and tabla.isSelected(fila, columna):
                        nuevafila.append(repr(self.__idu[fila][columna]))
                    else:
                        nuevafila.append(None)
                LOG.debug("Fila añadida a la seleccion de copiado: "+str(nuevafila))
                listasalida.append(nuevafila)
        return listasalida

    def insertar_reg(self):
        """Inserta un registro en la posicion actual"""
        assert(self.currentPageIndex() == 0) #Estamos en la tabla de registros
        tabla = self.table1
        pos = tabla.currentRow()
        self.__idu.ins_reg(pos)
        self.myUpdate() #TODO: Optimizar redibujado

    def verificar_seleccion_registros(self):
        """Verifica que la seleccion solamente consta de registros."""
        tabla = self.table1
        for indiceseleccion in range(tabla.numSelections()):
            seleccion = tabla.selection(indiceseleccion)
            if seleccion.leftCol()!=0 or seleccion.rightCol() < self.__idu.n_var()-1:
                LOG.debug("Seleccionincorrecta:"+str(seleccion.leftCol())+","+str(seleccion.rightCol()))
                from Driza.excepciones import SeleccionIncorrectaException
                raise SeleccionIncorrectaException

    def mostrar_t_reg(self):
        """Muestra el tab de casos"""
        self.showPage(self.tab)

    def mostrar_t_var(self):
        """Muestra el tab de variables"""
        self.showPage(self.tab_2)

    #Metodos privados

    def __mostrar_t_var(self):  
        """ Representa la variable pos en la tabla de variables. Las propiedades de la variable las lee de los datos.
        Si no se indica posicion, se entiende que se quiere rellenar toda la tabla
        """
        LOG.debug("Actualizando tabla de variables completa")
        if self.__nvar > (self.table2.numRows()-self.__idu.n_var()):
            self.table2.setNumRows(self.__idu.n_var()+self.__nvar)
        for fila in range(self.__idu.n_var(), self.table2.numRows()):
            for columna in range(self.table2.numCols()):
                self.table2.clearCell(fila, columna)
        for indicevar in range(self.__idu.n_var()):
            self.__mostrar_var(indicevar)
        self.__mostrar_titulo_t_reg()

    def __mostrar_var(self, pos):
        """Muestra una unica variable (fila) en la tabla segun el listado de variables"""
        variable = self.__idu.var(pos)
        self.table2.setText(pos, 0, str(variable.name()))
        self.table2.setItem(pos, 1, self.__combotableitem())    
        self.table2.item(pos, 1).setCurrentItem(variable.tipo)
        self.table2.setText(pos, 3, str(variable.descripcion))
        self.table2.setText(pos, 2, str(variable.valorpordefecto))
        self.table2.setItem(pos, 4, self.__botontableitem())    

    def __mostrar_t_reg(self):
        """ Rellena la tabla de datos con los registros actuales
        """
        if self.__nreg > (self.table1.numRows() - self.__idu.n_reg()):
            self.table1.setNumRows(self.__idu.n_reg() + self.__nreg)
        for i in range(self.__idu.n_reg()):
            self.__mostrar_reg(i)
        self.__mostrar_titulo_t_reg()
        for i in range(self.__idu.n_reg(), self.table1.numRows()):
            for j in range(self.table1.numCols()):
                self.table1.clearCell(i, j)
        for i in range(self.table1.numRows()):
            for j in range(self.__idu.n_var(), self.table1.numCols()):
                self.table1.clearCell(i, j)
        self.__mostrar_lateral_t_reg()

    def __mostrar_reg(self, pos):
        """Muestra un solo dato"""
        if self.modoetiqueta:
            for i in range(self.__idu.n_var()):
                if hasattr(self.__idu[pos][i], "etiqueta"):
                    self.table1.setText(pos, i, self.__idu[pos][i].etiqueta())
                else:
                    self.table1.setText(pos, i, str(self.__idu[pos][i]))
        else:
            for i in range(self.__idu.n_var()):
                self.table1.setText(pos, i, str(self.__idu[pos][i]))

    def __mostrar_columna_t_reg(self, pos):
        """Muestra una columna de la tabla de registros"""
        for i in range(self.__idu.n_reg()):
            self.table1.setText(i, pos, str(self.__idu[i][pos]))


    def __mostrar_titulo_t_reg(self, pos=None):
        """Actualiza los titulos de la tabla de datos segun las variables"""
        titulos = self.table1.horizontalHeader()
        if pos:
            titulos.setLabel(pos, self.__idu.var(pos).name())
        else:
            i = 0
            for _ in range(self.__idu.n_var()):
                self.table1.horizontalHeader().setLabel(i, self.__idu.var(i).name())
                i += 1

            for _ in range(self.__idu.n_var(), self.table1.horizontalHeader().count()):
                self.table1.horizontalHeader().setLabel(i, '')
                i += 1

    def __mostrar_lateral_t_reg(self):
        """Muestra los numeros laterales. Sirve para el filtrado"""
        lateral = self.table1.verticalHeader()
        #lista=self.__idu.getCol(self.__gestorfiltro.variable,filtrado=False)
        for i in range(self.__idu.n_reg()):
        #    if self.__gestorfiltro.variable and not lista[i]:
        #        lateral.setLabel(i,"--"+str(i))
        #    else:
            lateral.setLabel(i, str(i+1))

    def __combotableitem(self):
        """Devuelve un nuevo objeto tipo combotableitem con la lista de tipos"""
        lista = QStringList()
        from Driza.listas import SL
        for tipo in SL.nombrevariables:
            lista.append(tipo)
        return QComboTableItem(self.table2, lista)
    
    def __botontableitem(self):
        """Devuelve un nuevo objeto tipo combotableitem con la lista de tipos"""
        return ButtonTableItem(self.table2, self.dcasos)

        
    def __modificacion_t_var(self, fila, columna):
        """Funcion a que conecta con la introduccion de nuevos datos en la tabla de variables"""
        if columna == 1 and (self.table2.text(fila, columna).latin1() == self.__idu.var(fila).tipo):
            return # Se ha solicitado un cambio de tipo al propio tipo
        self.__portero.guardar_estado()
        if fila >= self.__idu.n_var(): #Es una nueva variable
            #Variables intermedias (creadas con los valores por defecto)
            for valorintermedio in range (self.__idu.n_var(), fila):
                self.__insertar_variable()
                self.__mostrar_var(valorintermedio)
            self.__insertar_variable()
        #Variable modificada
        variable = self.__idu.var(fila)
        if columna == 1:   # El usuario quiere cambiar el tipo
            textoencuestion = self.table2.text(fila, columna).latin1() 
            #preguntar el tipo de conversion
            metododeseado = self.__preguntar_conversion(variable, textoencuestion)
            if metododeseado:
                variable, columna = self.__agenteconversion(variable, textoencuestion, metododeseado) #Pareja variable-list
                self.__idu.establecer_var(fila, variable, columna)
                self.__mostrar_t_reg()  
        else: #Restos de campos (Texto)
            from Driza.excepciones import VariableExisteException
            try:
                self.__idu.modificar_var(variable, columna, str(self.table2.text(fila, columna).latin1()))
            except VariableExisteException:
                QMessageBox.warning(self, u'Atención', u'El nombre de variable ya existe')
            except NameError:
                QMessageBox.warning(self, u'Atención', u'Nombre de variable Erróneo')

        self.__mostrar_var(fila)
        #En todos los casos, actualizamos el titulo de la tabla de datos
        self.__mostrar_titulo_t_reg()

    def __actualizar_reg_interfazdatos(self, row, col, valor):
        """actualiza un dato en interfazdatos,recogiendo la excepcion en caso de error """
        LOG.debug("Actualizando datos de la interfaz:" + str(row) + "," + str(col))
        try:
            self.__idu[row][col] = valor
        except ValueError:
            QMessageBox.warning(self, 'Atención', u'El dato no es válido')
    
    def __insertar_registro(self):
        """Inserta un registro genérico, y ademas comprueba que no nos estamos acercando al final de la tabla"""
        self.__idu.ana_reg()
        if self.__nreg > (self.table1.numRows() - self.__idu.n_reg()):
            self.table1.setNumRows(self.table1.numRows() + 1)

    def __insertar_variable(self):
        """Inserta una variable genérica, y ademas comprueba que 
        no nos acercamos a ninguno de los limites de las tablas"""
        self.__idu.ana_var()
        if self.__nvar > (self.table2.numRows() - self.__idu.n_var()):
            self.table2.setNumRows(self.table2.numRows() + 1)
            self.table1.setNumCols(self.table1.numCols() + 1)

    def __modificacion_t_reg(self, fila, columna):
        """Actualiza los datos del objeto dato a partir de un cambio en la tabla de datos"""
        if (fila < self.__idu.n_reg())\
                and (columna < self.__idu.n_var())\
                and (self.table1.text(fila, columna).latin1() == str(self.__idu[fila][columna])):
            return #No hay cambio efectivo #FIXME: No detecta reales
        LOG.debug("Cambiado registro en la tabla")
        valor = self.table1.text(fila, columna).latin1()
        self.__portero.guardar_estado()
        if columna >= self.__idu.n_var():
            LOG.debug("Creando nueva variable por demanda en la modificaicon de un registro")
            #Estamos trabajando sobre una variable inexistente
            for i in range(self.__idu.n_var(), columna + 1):
                self.__insertar_variable()
                self.__mostrar_columna_t_reg(i)
            self.__mostrar_t_var() #actualizamos la tabla de variables
        if fila >= self.__idu.n_reg():
            #no existen registros intermedios
            LOG.debug("Creando nuevo registro por demanda en la modificaicon de un registro")
            for i in range (self.__idu.n_reg(), fila):
                self.__insertar_registro()
                self.__mostrar_reg(i)  
            self.__idu.ana_reg() #El último se separa, tenemos que verificar si el usuario ha escrito correctamente
        self.__actualizar_reg_interfazdatos(fila, columna, valor)
        self.__mostrar_reg(fila)
        #Comprobacion de que sobra el numero correcto de celdas
        if self.__nreg > (self.table1.numRows() - self.__idu.n_reg()):
            self.table1.setNumRows(self.__idu.n_reg() + self.__nreg)
        self.parent().parent().parent().mostrar_undo_redo()

    
    def __preguntar_conversion(self, variable, objetivo):
        """Pregunta cual de los metodos disponibles para la conversion desea escoger el usuario"""
        lista = []
        if variable.diccionarioconversion.has_key("Agrupador"):
            #Conversión a todos los tipos
            lista += variable.diccionarioconversion["Agrupador"]
        for tipo in variable.diccionarioconversion.iterkeys():
            if tipo == objetivo:
                lista += variable.diccionarioconversion[tipo]
        #Elaborar una lista y preguntar al usuario
        qlista = QStringList()
        for elemento in lista:
            qlista.append(elemento)
        cadena = QInputDialog.getItem("Elige!", u"Elige una función de conversion", qlista, 0, False, self, "Dialogo")
        #devolver el nombre de la funcion
        if cadena[1]:
            return cadena[0].latin1()
        else:
            return ""
