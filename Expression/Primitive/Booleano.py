from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Abstract.Expression import Expression
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class Booleano(Expression):

    def __init__(self, fila, columna,  type: typeExpression, value) -> None:
        #super().__init__()
        self.type = type
        self.value = value
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        newVar = Value(self.value,False,self.type)
        if(self.value == True):
            newVar.trueLabel = self.generator.newLabel()
        elif(self.value == False):
            newVar.falseLabel = self.generator.newLabel()
        else:
            objErrores.setNewError(Error("Error: Tipo de dato erroneo", self.fila, self.columna, dt_string))   
            print("Valor erroneo para Tipo Booleano")
        return newVar