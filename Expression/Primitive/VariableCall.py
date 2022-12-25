from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class VariableCall(Expression):

    def __init__(self, fila, columna,  id:str) -> None:
        super().__init__(fila,columna)
        self.id = id
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()
        retSym:Symbol = environment.getVariable(self.id)
        
        try:


            if (retSym.type == typeExpression.LIST_INTFL):
                print("ES LISTA -> " + str(retSym.position))
                return Value(str(retSym.position),False,retSym.type)
            elif(retSym.type != typeExpression.BOOL):
                newTemp = self.generator.newTemp()
                self.generator.addGetStack(newTemp,str(retSym.position))
                return Value(newTemp,True,retSym.type)
            else:
                newTemp = self.generator.newTemp()
                self.generator.addGetStack(newTemp,str(retSym.position))
                val = Value(newTemp,True,typeExpression.BOOL)
                newTempSi = self.generator.newLabel()
                newTempNo = self.generator.newLabel()
                self.generator.addIf(newTemp,"1","==",newTempSi)
                self.generator.addGoto(newTempNo)
                val.falseLabel = newTempNo
                val.trueLabel = newTempSi
                return val
        except:
            objErrores.setNewError(Error("Error: la variable no tiene valor asignado", self.fila, self.columna, dt_string))   
            print("Error, la variable no tiene valor asignado")