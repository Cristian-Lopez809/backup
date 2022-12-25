from Environment.ListErrores import ListErrores
from Environment.Error import Error
from datetime import datetime
from Environment.SymbolsTable import SymbolsTable
from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class Return(Instruction):
    def __init__(self, fila, columna, expression:Expression) -> None:
        super().__init__(fila,columna)
        self.fila = fila
        self.columna = columna
        self.expresion = expression

    def compile(self, environment: Environment):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()
        if environment.labelRtn == '':
            objErrores.setNewError(Error("Error: Instruccion Return fuera de instruccion", self.fila, self.columna, dt_string))   
            return
        newValue: Value = self.expresion.compile(environment)
        if newValue.type == typeExpression.BOOL:
            if(newValue == True):
                newValue.trueLabel = self.generator.newLabel()
            elif(newValue == False):
                newValue.falseLabel = self.generator.newLabel()
            else:
                objErrores.setNewError(Error("Error: Tipo de dato erroneo", self.fila, self.columna, dt_string))   
                print("Valor erroneo para Tipo Booleano")
        else:
            self.generator.addSetStack('P',str(newValue.value))
        self.generator.addGoto(environment.labelRtn)