#!/usr/bin/python
# -*- coding: utf-8 -*-
#

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

""" Interfaces de acceso a los datos """

import logging
LOG = logging.getLogger(__name__)

def comprobar_nombre_filtro(nombre):
    """Comprueba si el nombre no coincide con el nombre de filtro"""
    if nombre == "*filtro":
        #El nombre *filtro está reservado
        from  Driza.excepciones import VariableExisteException
        raise VariableExisteException()

class InterfazDatos:
    """
    Interfazdatos pretende ser una interfaz homogenea de acceso y modificacion
    de los datos para grid y otros elementos del programa
    La clase ofrece multiples formas de accesso a los datos internos
    """

    def __init__(self, portero):
        """Inicialización del contenedor principal"""
        self._portero = portero


    def __getitem__(self, indice): #Acceso por []
        """
        Devuelve el item segun un indice numerico, un nombre, 
        o un objeto variable
        Si el indice es un indice, se entiende que se quiere 
        acceder a un registro
        Si el indice es un nombre o el objeto variable, se entiende 
        que se quiere acceder a la columna
        """
        import types
        if indice.__class__ == types.IntType:
            return self._portero.actual().registros()[indice]
        else:
            return self.col(indice)
            
    def __setitem__(self, indice, valor): 
        """
            Modificacion por []
            Si el indice es un entero, se entiende que se 
            quiere modificar a un registro
            Si el indice es un nombre o el objeto variable, 
            se entiende que se quiere modificar a la columna
        """
        import types
        if indice.__class__ == types.IntType:
            self._portero.actual().registros[indice] = valor
        else: 
            #Añade los registros que no existen
            for registro in range(len(valor)-len(self._portero.actual().\
                    registros())):
                self.ana_reg()

            for registro in range(len(self._portero.actual().registros())):
                self._portero.actual().registros()[registro][indice] \
                        = valor[registro]

    def __delitem__(self, indice):
        """define el borrado con la función del, borra un registro"""
        import types
        if indice.__class__ == types.IntType:
            self._portero.actual().registros().__delitem__(indice)

    #FUNCIONES PUBLICAS Accesoras

    def var(self, indice = -1):
        """Devuelve la variable indicada por el indice, por defecto la última"""
        return self._portero.actual().variables()[indice] 

    def n_reg(self):
        """Devuelve el número de registros almacenados"""
        return len(self._portero.actual().registros())

    def n_var(self):
        """Devuelve el número de variables almacenadas"""
        return len(self._portero.actual().variables())

    def lista_tit_discreto(self):
        """Devuelve una lista con los titulos de las variables discretas"""
        return [x.name() for x in self._portero.actual().variables() if "discreto" in x.tags]

    def lista_tit_numerica(self):
        """Devuelve una lista con los titulos de las variables numericas"""
        return [x.name() for x in self._portero.actual().variables() if "numerico" in x.tags]

    def lista_tit(self, tipo = None):
        """
        Devuelve una lista con todos los nombres de las variables
        opcionalmente podemos filtrar segun un tipo
        """
        if not tipo:
            return self._portero.actual().variables().lista_nombres()
        lista = []
        for variable in self._portero.actual().variables():
            if variable.tipo == tipo:
                lista.append(variable.name())
        return lista
                
    def obtener_casos(self, indice):
        """Devuelve todos los casos existentes de una determinada variable"""
        #debe ser una variable discreta, si no excepcion
        lista = []
        for valor in self._portero.actual().registros():
            if valor[indice] not in lista:
                lista.append(valor[indice])
        if None in lista:
            lista.remove(None)
        lista.sort()
        return lista

    def col(self, indice):
        """Devuelve un array con todos los valores asociados a 
        la variable representada por indice.
        Para uso de las clases del programa
        """
        lista = []
        for valor in self._portero.actual().registros():
            lista.append(valor[indice])
        return lista

    def borrar_todo(self):
        """Borra todos los datos"""
        self._portero.nuevo_estado(True)

    def original(self):
        """Devuelve True o False en funcion de si el estado actual es original"""
        return self._portero.actual_original()

    #Funciones Modificadoras

    def ins_reg(self, pos, dato = None):
        """inserta un registro en la posicion pos"""
        from Driza.datos.datos import Registro
        import types
        if dato is None:
            registro = Registro(self._portero.actual().variables())
            self._portero.actual().registros().insert(pos, registro)
        elif isinstance(dato, Registro):
            self._portero.actual().registros().insert(pos, dato)
        elif dato.__class__ == types.ListType:
            registro = Registro(self._portero.actual().variables())
            registro.establecer_valores(dato)
            self._portero.actual().registros().insert(pos, registro)
        else:
            raise TypeError

    def ana_reg(self, dato=None):
        """Añade un Registro en la ultima posicion"""
        pos = self.n_reg()+1
        self.ins_reg(pos, dato)

    def ana_var(self, nombre = None, tipo = "Real", \
            valorpordefecto = "NA", descripcion = "", protegerfiltro=True):  
        """
        Añade una variable de tipo tipo al array de variables. 
        Rellena los registros con el valor por defecto
        """
        if not nombre:
            if self.n_var() == 0:
                nombre = "VAR0"
            else:
                nombreultimavariable = self.var(-1).name()
                import re
                expresion = re.compile('^VAR[0-9]*$')
                if expresion.match(nombreultimavariable):
                    numero = int(nombreultimavariable.replace("VAR", ""))+1
                else:
                    numero = self.n_var()
                nombre = "VAR" + str(numero)
                while nombre in self.lista_tit():
                    numero += 1
                    nombre = "VAR"+str(numero)

        self._ana_var_privado(nombre, tipo, valorpordefecto, descripcion, protegerfiltro)

    #Funciones protegidas

    def _ana_var_privado(self, nombre, tipo, valorpordefecto, descripcion, protegerfiltro = True):
        """Añade una variable, sin preocuparse por los registros"""
        if nombre in self.lista_tit():
            from  Driza.excepciones import VariableExisteException
            raise VariableExisteException()
        if protegerfiltro:
            comprobar_nombre_filtro(nombre)
        from Driza.listas import SL
        if not SL.TIPOSAGRUPADOR.has_key(tipo): 
            raise TypeError
        from Driza.datos.agrupadores import Agrupador
        if tipo == "Ordinal" or tipo == "Entero" or tipo == "Real":
            self._portero.actual().variables().append\
                    (Agrupador(nombre, tipo, descripcion, valorpordefecto)) 
        elif tipo == "Factor" or tipo == "Logico":
            self._portero.actual().variables().append\
                    (Agrupador(nombre, tipo, descripcion)) 

    def _obtener_indice_variable(self, variable):
        """Devuelve el indice numerico de la variable pasada"""
        return self._portero.actual().variables().obtener_indice(variable)

class InterfazDatosUsuario(InterfazDatos):
    """La interfaz de datos especializada para la interfaz de usuario
    Incluye funciones de generación de datos a partir de expresiones
    Funciones relacionadas con los estados undo/redo"""
    def __init__(self, portero, gestorpaquetes):
        InterfazDatos.__init__(self, portero)
        self.__gestorpaquetes = gestorpaquetes

    #Funciones publicas

    def ana_var_expresion(self, nombre, tipo, valorpordefecto, descripcion, expresion, \
            vigilarfiltro = True, permitirsobreescritura = False, solofiltrados = False):  
        """
        Añade una variable de tipo tipo al array de variables. 
        Rellena los registros con el valor por defecto, 
        salvo que se indique una expresion
        """
        listaresultante = self.__interpreta_expresion(expresion)
        if solofiltrados:
            assert(permitirsobreescritura == True) 
            #Si se trabaja solo sobre filtrados, es porque se permite sobreescritura
        if not permitirsobreescritura or not (nombre in self.lista_tit()):
            self._ana_var_privado(nombre, tipo, valorpordefecto, descripcion, vigilarfiltro)
            for i in range(self.n_reg()):
                self._portero.actual().registros()[i][nombre] = (listaresultante[i])
        elif permitirsobreescritura and (nombre in self.lista_tit()):
            variable = self.var(nombre)
            if variable.tipo != tipo:
                raise TypeError
            self.modificar_var(variable, "valorpordefecto", valorpordefecto)
            self.modificar_var(variable, "descripcion", descripcion)
            posicion = self._obtener_indice_variable(nombre)
            if solofiltrados:
                indicefiltro = self._obtener_indice_variable("*filtro")
                for i in range(self.n_reg()):
                    if self._portero.actual().registros()[i][indicefiltro]:
                        self._portero.actual().registros()[i][posicion] = listaresultante[i]
            else:
                for i in range(self.n_reg()):
                    self._portero.actual().registros()[i][posicion] = listaresultante[i]

    def establecer_original(self):
        """Establece la flag original"""
        self._portero.establecer_actual_original()

    def borrar_var(self, indice):
        """Borra una variable y su contenido asociado"""
        for reg in self._portero.actual().registros():
            if reg.has_key(indice):
                del reg[indice]
        try:
            del self._portero.actual().variables()[indice] 
        except IndexError:
            #Si no encuentra el elemento, no pasa nada
            pass

    def modificar_var(self, variable, indice, valor):
        """
        Modifica una variable existente. 
        Es necesario para verificar que el nombre no esta ya ocupado
        Variable es el objeto variable, no el indice
        """
        if indice == 0 or indice == "nombre":
            if valor in self.lista_tit():
                from  Driza.excepciones import VariableExisteException
                raise VariableExisteException()
            comprobar_nombre_filtro(valor)
            variable.set_name(valor)
        elif indice == 2 or indice == "valorpordefecto":
            variable.valorpordefecto = valor
        elif indice == 3 or indice == "descripcion":
            variable.descripcion = valor

    def setVar(self, indice, variable, columna = None):
        """
        Sobreescribe la variable asociada al indice.
        Hace una conversión de tipos según la representación interna de estos
        Si se le pasa la columna, entonces sobreescribira todos 
        los registros asociados a la variable
        """
        #Debe comprobar la correctitud del array y lanzar 
        #una excepcion si no vale
        LOG.debug("Columna pasada a setVar: "+str(columna))
        array = []
        if variable.name() in self.lista_tit() \
                and self.var(indice).name() != variable.name():
            #Comprobamos que no se trata de un cambio de atributo 
            #de la variable
            from  Driza.excepciones import VariableExisteException
            raise VariableExisteException()
        comprobar_nombre_filtro(variable.name())
        if not columna:
            #Conversion directa (Inestable)
            for elemento in self.col(indice):
                array.append(repr(elemento))
            self._portero.actual().variables()[indice] = variable
            for registro in self._portero.actual().registros():
                registro[indice] = variable.nuevo_item(array[indice])
        else:
            #Nos pasan la columna con los datos
            assert(len(columna) == self.n_reg())
            self._portero.actual().variables()[indice] = variable
            i = 0
            for registro in self._portero.actual().registros():
                registro[indice] = variable.nuevo_item(columna[i])
                i += 1
            #TODO: Continuar con el caso de la columna

    def establecer_filtro(self, expresion):
        """Establece el valor del filtro y lo activa"""
        LOG.debug("Se solicita aplicar el filtro:"+expresion)
        listaresultante = self.__interpreta_expresion(expresion)
        if not "*filtro" in self.lista_tit():
            self.ana_var("*filtro", "Logico", False, "None", False)
            i = 0
            for registro in self._portero.actual().registros():
                registro[-1] = self.var(-1).nuevo_item(listaresultante[i])
                i += 1
        else:
            indicefiltro = self._obtener_indice_variable("*filtro")
            i = 0
            for registro in self._portero.actual().registros():
                registro[indicefiltro] = self.var(indicefiltro).nuevo_item(listaresultante[i])
                i += 1
        #Calcular el valor para cada registro e introducirlo


    def borrar_filtro(self):
        """Borra/Desactiva el filtro"""
        if "*filtro" in self.lista_tit():
            self.borrar_var("*filtro")

    #Funciones Privadas

    def __interpreta_expresion(self, expresion):
        """Interpreta una expresion y devuelve una lista con los resultados"""
        LOG.debug("Interpretando expresion: "+expresion)
        listavars = []
        #Copia de la lista, ya que vamos a hacer un reverse
        listavars += self._portero.actual().variables() 
        #Evaluamos las variables con el nombre más grande para 
        #evitar los casos en los que una variable contenga a otra
        listavars.sort(lambda x, y: len(x.name()) > len(y.name()))
        listavars.reverse() 
        listaindicevariables = [] 
        for var in listavars:
            numero = self._obtener_indice_variable(var)
            if expresion.find(var.name()) !=- 1:
                listaindicevariables.append(numero)
                expresion = expresion.replace(var.name(), "self.__getitem__(i)["+repr(numero)+"]")

        #lista = self.__gestorpaquetes.listafunciones()
        #cosatmp = self.__gestorpaquetes
        ##Recorremos la lista de funciones, y hacemos la sustitucion (Con prefijo)
        #for funcion in lista: 
        #    texto = string.split(funcion,".")
        #    ristra = "cosatmp[\""+texto[0]+"\"][\""+texto[1]+"\"]"
        #    expresion = expresion.replace(funcion, ristra)

        lista = self.__gestorpaquetes.lista_funciones(False)
        gestorpaquetes = self.__gestorpaquetes
        #Recorremos la lista de funciones, y hacemos la sustitucion (Sin prefijo)
        for funcion in lista: 
            ristra = "gestorpaquetes[\""+funcion+"\"]"
            expresion = expresion.replace(funcion, ristra)
        lista = []
        LOG.debug("Resultado expresion: "+expresion)
        for i in range(self.n_reg()):
            valido = True
            for j in listaindicevariables:
                if not self.__getitem__(i)[j].valido():
                    valido = False
            if valido:
                lista.append(eval(expresion))
            else:
                lista.append(None)
        LOG.debug("Lista resultante de la expresion: "+str(lista))
        return lista


class InterfazDatosR(InterfazDatos):
    """La interfaz de datos con R """
    def resolver_etiqueta(self, variable, caso):
        """Devuelve la etiqueta sie xiste, si no devuelve el caso tal cual"""
        variable = self.var(variable)
        if variable.etiquetas.has_key(caso):
            return variable.etiquetas[caso]
        elif variable.etiquetas.has_key(str(caso)):
            return variable.etiquetas[str(caso)]
        else:
            return caso

    def formato_R(self):
        """Devuelve una copia de los datos actuales en el formato data de R"""
        #TODO: Falta el control de filtrado
        import rpy
        diccionario = {}
        for variable in self._portero.actual().variables:
            if variable.tipo != "Factor":
                lista = map(float, self.__getitem__(variable))
            else:
                lista = map(str, self.__getitem__(variable))
            diccionario[variable.name()] = lista
        return rpy.r.data_frame(diccionario)

    def query(self, vars, *condiciones):
        """El query es una peticion de datos que sera enviada a R. 
        Hace prácticamente lo mismo que col, salvo que en este 
        caso la lista de datos es devuelta directamente en formato float, 
        y acepta condiciones de filtrado
        """
        if not isinstance(vars, list):
            vars = [ vars ] 
        for var in vars:
            if not "numerico" in self.var(var).tags:
                raise TypeError
        #TODO assert la variable de filtrado es distinta de la 
        #de alguna condicion
        #TODO assert la variable es distinta a la 
        #de alguna condicion
        from Driza.datos.condiciones import procesa_condicion
        mifuncion = lambda f: procesa_condicion(self, f)
        listacondiciones = map(mifuncion, condiciones)
        lista = []
        for register in self._portero.actual().registros():
            isvalid = True
            listacampoactual = []
            for var in vars:
                listacampoactual.append(register[var])
                if not register[var].valido():
                    isvalid = False
            if "*filtro" in self.lista_tit():
                indicefiltro = self._obtener_indice_variable("*filtro")
                from types import NoneType
                if isinstance(register[indicefiltro].valor, NoneType):
                    isvalid = False
                elif not register[indicefiltro]:
                    isvalid = False
            for condicion in listacondiciones:
                if not condicion(register): 
                    #Tiene que verificar todas las condiciones
                    isvalid = False 
            if isvalid:
                if len(vars) > 1:
                    listafinal = map(to_R,listacampoactual)
                    lista.append(listafinal)
                else:
                    lista.append(listacampoactual[0].to_R())
        return lista

class InterfazDatosFicheros(InterfazDatos):
    """La interfaz de datos con los ficheros"""
    def cargar_texto(self, fichero, **opciones):
        """Carga los datos de un fichero de texto"""
        import os
        if not os.path.exists(fichero):
            from Driza.excepciones import FicheroNoExisteException
            raise FicheroNoExisteException(fichero)
        from rpy import r
        datos = r.read_table(fichero, sep = opciones["delimitadoratrib"], \
                header = opciones["cabeceras"], na_strings="NA", dec=".", \
                strip_white = False)
        for nombre, columna in datos.items():
            import types
            milista = []
            if type(columna[0]) == types.IntType:
                self.ana_var(nombre, "Entero")
                for registro in columna:
                    if registro == -2147483648: #Valor nulo
                        resultado = None
                    else: 
                        resultado = int(registro)
                    milista.append(resultado)
            elif type(columna[0]) == types.StringType:
                #Es un Factor
                self.ana_var(nombre, "Factor")
                milista = columna
            elif type(columna[0]) == types.FloatType:
                self.ana_var(nombre, "Real")
                milista = columna
            else: 
                raise TypeError #R Devuelve un tipo desconocido
            for i in range(self.n_reg(), len(milista)):
                self.ana_reg()
            for i in range(self.n_reg()):
                self._portero.actual().registros()[i][nombre] = milista[i]

