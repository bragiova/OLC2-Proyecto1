from Abstract.Expresion import Expresion
from Abstract.Retorno import *
from Sym.Error import Error

class AccesoArray(Expresion):
    def __init__(self, ident, listIndices, linea, columna):
        super().__init__(linea, columna)
        self.ident = ident
        self.listIndices = listIndices

    def ejecutar(self, env):
        # se obtiene la variable de tipo arreglo
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
                    
                    for i, indice in enumerate(listValIndices):
                        # se actualiza el item que se está verificando, si en dado caso es de más de una dimensión
                        if isinstance(listItemArray, list):
                            if indice.valor > len(listItemArray) - 1:
                                return Error('Semántico', 'El índice está fuera de rango', self.linea, self.columna)
                            
                            listItemArray = listItemArray[indice.valor]
                        else:
                            if indice.valor > len(listItemArray.valor) - 1:
                                return Error('Semántico', 'El índice está fuera de rango', self.linea, self.columna)
                            
                            listItemArray = listItemArray.valor[indice.valor]
                    
                    # Una vez encontrado el item, se retorna
                    # La verificación de si es instancia de lista es solo cuando se pide el arreglo que está dentro de otro arreglo
                    if isinstance(listItemArray, Retorno) or isinstance(listItemArray, list):
                        return listItemArray

                else:
                    return Error('Semántico', 'No se encontraron índices válidos para el arreglo', self.linea, self.columna)
            else:
                return Error('Semántico', 'La variable no es de tipo Arreglo', self.linea, self.columna)
        else:
            return Error('Semántico', 'No se encontró la variable', self.linea, self.columna)
