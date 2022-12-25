from Enum.typeExpression import typeExpression
from Environment.Symbol import Symbol

class Environment:
    errores = []
    variable= {}
    funciones = {}
    structs = {}

    def __init__(self,father, nameAmbito) -> None:
        self.father = father
        self.nameAmbito = nameAmbito
        self.variable= {}
        self.funciones = {}
        self.structs = {}
        self.size=0
        self.labelBrk = ""
        self.labelCont = ""
        self.hijo = None
        self.labelRtn = ""


        if(father!= None):
            self.size = father.size
            self.labelBrk = self.father.labelBrk
            self.labelCont = self.father.labelCont
            self.labelRtn = self.father.labelRtn

    def saveVariable(self,id:str,type:typeExpression, fila, columna,heap_in, struct_type=''):
        env = self
        if self.variable.get(id)!=None:
            self.errores.append("La variable "+id+" ya existe")
            return
        elif id[-1] == '#':
            id = id[0:-1]
            tempVarAux = Symbol(id,type,self.size,fila,columna,"Funcion")
            self.size +=1
            self.variable[id] = tempVarAux
            Environment.variable = self.variable
            return tempVarAux
        else:
            tempVar = Symbol(id,type,self.size,fila,columna,self.nameAmbito)
            self.size = self.size+1
            self.variable[id]=tempVar
            return tempVar



    def existVariable(self,id:str):
        env = self
        if(self.variable.get(id)!=None):
            self.errores.append("La variable "+id+" ya existe")
            return True
        
        return False

    def getVariable(self,id:str) -> Symbol:
        tempEnv = self
        while(tempEnv!=None):
            if(tempEnv.variable.get(id)!=None):
                return tempEnv.variable.get(id)
            tempEnv = tempEnv.father
        self.errores.append("La variable "+id+" no existe")
        return

    def searchInGlobal(self,id:str) -> Symbol:
        tempEnv = self
        exactSymbol : Symbol

        #Busca GLOBAL
        while(tempEnv!=None):
            exactSymbol = tempEnv
            tempEnv = tempEnv.father
        
        #Busca en GLOBAL
        if(exactSymbol.variable.get(id)!=None):
                return exactSymbol.variable.get(id)
        return None

    def saveFuncion(self, id_funcion, funcion, fila, columna):
        if(self.funciones.get(id_funcion)!=None):
            self.errores.append("La Funcion " + id_funcion + " ya existe")
            return
        tempVar = Symbol(id_funcion,funcion,self.size, fila, columna, self.nameAmbito)
        self.size = self.size+1
        self.funciones[id_funcion]=tempVar
        return tempVar

    def getSimbolos(self):
        ent = self
        if ent != None:
            s = ent.variable
            return s
        return None

    def getFuncion(self, id_funcion) -> Symbol:
        tempEnv = self
        print(id_funcion)
        while tempEnv != None:
            if tempEnv.funciones.get(id_funcion) != None:
                print("si entre aqui")
                return tempEnv.funciones[id_funcion]
            tempEnv = tempEnv.father
        self.errores.append("La funcion " + id_funcion + " No existe")
        return
