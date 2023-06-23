from Abstract.Instruccion import Instruccion
from Abstract.Retorno import *
from Sym.Error import Error
from Sym.Simbolo import Simbolo

class AsignacionArray(Instruccion):
    def __init__(self, ident, listIndices, expresion, linea, columna):
        super().__init__(linea, columna)
        self.ident = ident
        self.listIndices = listIndices
        self.expresion = expresion

    def ejecutar(self, env):
        simbArray = env.getSimbolo(self.ident)

        if simbArray is not None:
            if simbArray.getTipo() == Tipo.ARREGLO:
                listValIndices = []

                # se recorre el arreglo de índices enviado, para poder encontrar el item
                for indice in self.listIndices:
                    valIndice = indice.ejecutar(env)
                    if isinstance(valIndice, Error): return valIndice

                    # guardo los valores de cada índice, debería de ser una lista de objetos Retorno
                    if valIndice is not None:
                        listValIndices.append(valIndice)
                
                if len(listValIndices) > 0:
                    # se obtiene el valor del símbolo, que deberían de ser los items del arreglo
                    listItemArray = simbArray.getValor()
                    valExpre = self.expresion.ejecutar(env)
                    if isinstance(valExpre, Error): return valExpre
                    
                    actualItem = listItemArray
                    for i, indice in enumerate(listValIndices):
                        if i < len(listValIndices) -1:
                        # se actualiza el item que se está verificando, si en dado caso es de más de una dimensión
                            if isinstance(actualItem, list):
                                if indice.valor > len(actualItem) - 1:
                                    return Error('Semántico', 'El índice está fuera de rango', self.linea, self.columna)
                            
                                actualItem = actualItem[indice.valor]
                            else:
                                if indice.valor > len(actualItem.valor) - 1:
                                    return Error('Semántico', 'El índice está fuera de rango', self.linea, self.columna)

                                actualItem = actualItem.valor[indice.valor]
                        else:
                            break
                    
                    indexFin = listValIndices[len(listValIndices) - 1]
                    if isinstance(actualItem, list):
                        actualItem[indexFin.valor].valor = valExpre.valor
                    else:
                        actualItem.valor[indexFin.valor].valor = valExpre.valor
            
            simbActualizado = Simbolo(simbArray.getId(), simbArray.getTipo(), listItemArray, self.linea, self.columna)
            env.updateTabla(simbActualizado)
                    
                
