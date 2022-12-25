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

class DeclararArray(Instruction):

    def __init__(self, fila, columna,  id:str, values , type:typeExpression) -> None:
        super().__init__(fila,columna)
        self.id = id
        self.values = values
        self.type = type
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        objErrores = ListErrores()

        auxValue:Value = self.values[0]
        if(auxValue.type == typeExpression.INT or auxValue.type == typeExpression.FLOAT):
            tempVar: Symbol = environment.saveVariable(self.id,typeExpression.LIST_INTFL, self.fila, self.columna,False, "")
            
        tmpTabla = SymbolsTable()
        tmpTabla.setNewSimbol(tempVar)

        if(self.type == typeExpression.LIST):
            self.generator.addSetStack(str(tempVar.position),str(len(self.values)))
            pos = environment.size
            for value in self.values:
                if(value.type == typeExpression.INT or value.type == typeExpression.FLOAT):
                    self.generator.addSetStack(str(pos),str(value.value))
                    pos += 1
                    environment.size = pos
            self.generator.addSetStack(str(pos),"-1")
            pos += 1
            environment.size = pos + 1
            
