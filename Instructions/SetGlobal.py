from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class SetGlobal(Instruction):

    def __init__(self, fila, columna,  variable:str, exp: Expression) -> None:
        super().__init__(fila,columna)
        self.variable = variable
        self.exp = exp
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        self.exp.generator = self.generator
        newValue: Value = self.exp.compile(environment)

        #Expresion no None
        if newValue != None:
            globalVar: Symbol = environment.searchInGlobal(self.variable)

            if globalVar != None:
                if(globalVar.type != typeExpression.BOOL):
                    self.generator.addSetStack(str(globalVar.position),newValue.getValue())
                else:
                    newLabel = self.generator.newLabel()
                    self.generator.addLabel(newValue.trueLabel)
                    self.generator.addSetStack(str(globalVar.position),'1')
                    self.generator.addGoto(newLabel)
                    self.generator.addLabel(newValue.falseLabel)
                    self.generator.addSetStack(str(globalVar.position),'0')
                    self.generator.addGoto(newLabel)
                    self.generator.addLabel(newLabel)
            else:
                objErrores.setNewError(Error("Error: la variable no existe en el entorno global", self.fila, self.columna, dt_string))   
                print("Error variable no existe en entorno global")
        else:
            objErrores.setNewError(Error("Error: la expresion a asignar es tipo None", self.fila, self.columna, dt_string))   
            print("Error, expresion de tipo Null en global")