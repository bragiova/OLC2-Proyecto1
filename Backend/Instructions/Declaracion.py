
from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Simbolo import Simbolo
from Sym.Error import Error

class Declaracion(Instruccion):
    def __init__(self, ident, valor, tipo, linea, columna, esArray = False, numDimensiones = 0):
        super().__init__(linea, columna)
        self.ident = ident
        self.valor = valor
        self.tipo = tipo
        self.esArray = esArray
        self.numDimensiones = numDimensiones

    def ejecutar(self, env):
        valorVar = self.valor

        if isinstance(valorVar, list):
            self.esArray = True
        
        if self.tipo is None:
            self.tipo = Tipo.ANY

        if self.esArray:
            return self.ejecutarArray(env)
        else:
            if valorVar is not None:
                valorVar = self.valor.ejecutar(env)
                if isinstance(valorVar, Error): return valorVar
            else:
                if self.tipo != Tipo.ANY:
                    valorVar = self.setValorDefecto(self.tipo)
                else:
                    # self.tipo = Tipo.ANY
                    valorVar = Retorno(Tipo.ANY, None)

            if self.tipo == Tipo.ANY and self.tipo != valorVar.tipo:
                valorVar.tipo = Tipo.ANY

            if self.tipo == valorVar.tipo:
                nuevoSimbolo = Simbolo(self.ident, self.tipo, valorVar.valor, self.linea, self.columna)

                if env.existeSimbEnActual(self.ident):
                    return Error('Semántico', 'Variable ya está declarada', self.linea, self.columna)
                
                env.guardarVar(nuevoSimbolo)
            else:
                return Error('Semántico', 'El tipo de dato de la variable es distinto a la asignación', self.linea, self.columna)
        
    def ejecutarArray(self, env):
        listValArray = self.valor
        listObjArray = []
        esMismoTipo = True

        if listValArray is not None:
            for valorArray in listValArray:
                if isinstance(valorArray, list):
                    valItemList = self.getValArrayList(valorArray, env)
                    if isinstance(valItemList, Error): return valItemList

                    if valItemList is not None and valItemList.tipo != self.tipo:
                        esMismoTipo = False
                    # el valor debería de ser una lista
                    listObjArray.append(valItemList.valor)
                else:
                    valItem = valorArray.ejecutar(env)
                    if isinstance(valItem, Error): return valItem

                    if valItem is not None and valItem.tipo != self.tipo and self.tipo != Tipo.ANY:
                        esMismoTipo = False
                    # se llena la lista con objetos tipo Retorno [Retorno(Tipo.String, 'hola'), Retorno(Tipo.String, 'hola'), ...]
                    listObjArray.append(valItem)
        
        if esMismoTipo:
            array = Simbolo(self.ident, Tipo.ARREGLO, listObjArray, self.linea, self.columna, self.tipo)

            if env.existeSimbEnActual(self.ident):
                return Error('Semántico', 'Variable ya está declarada', self.linea, self.columna)
            env.guardarVar(array)
        else:
            return Error('Semántico', 'El tipo de dato del arreglo es distinto a la asignación', self.linea, self.columna)

    def setValorDefecto(self, tipo):
        if tipo == Tipo.NUMBER:
            return Retorno(Tipo.NUMBER, 0)
        elif tipo == Tipo.STRING:
            return Retorno(Tipo.STRING, "")
        elif tipo == Tipo.BOOL:
            return Retorno(Tipo.BOOL, 'false')
        elif tipo == Tipo.ANY:
            return Retorno(Tipo.ANY, None)
    
    def getValArrayList(self, listValores, env):
        result = Retorno(self.tipo, [])
        listObjArray = []

        for valorArray in listValores:
            valItem = valorArray.ejecutar(env)
            if isinstance(valItem, Error): return valItem

            # se llena la lista con objetos tipo Retornos
            listObjArray.append(valItem)

            # Si el item tiene diferente tipo que la variable, se modifica el result para validarlo después desde la llamada a la función
            if valItem is not None and valItem.tipo != self.tipo and self.tipo != Tipo.ANY:
                result.tipo = valItem.tipo
        
        result.valor = listObjArray

        return result



