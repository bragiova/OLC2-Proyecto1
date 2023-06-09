
from Sym.Error import Error

class TablaSimbolos:
    def __init__(self, envAnterior = None):
        self.tablaS = {}
        self.envAnterior = envAnterior
    
    # Se guardan las variables en la tabla de símbolos
    def guardarVar(self, simbolo):
        self.tablaS[simbolo.getId()] = simbolo

    # Se guardan las funciones en la tabla de símbolos
    def guardarFuncion(self, simbolo):
        self.tablaS[simbolo.getId()] = simbolo

    # Se obtiene un símbolo almacenado en la tabla de símbolos
    def getSimbolo(self, id):
        envActual = self
        while envActual != None:
            if id in envActual.tablaS:
                return envActual.tablaS[id]
            else:
                envActual = envActual.envAnterior
        return None
    
    # Se actualiza el valor de un símbolo en la tabla de símbolos
    def updateTabla(self, simbolo):
        envActual = self
        while envActual != None:
            if simbolo.getId() in envActual.tablaS:
                envActual.tablaS[simbolo.getId()].setValor(simbolo.getValor())
            else:
                envActual = envActual.envAnterior
        return Error("Semántico", "Variable no encontrada", simbolo.getLinea(), simbolo.getColumna())
    
    def existeSimbEnActual(self,identificador):
        entorno = self
        existe = entorno.tablaS.get(identificador)
        if existe is not None:
            return True
        else:
            return False

