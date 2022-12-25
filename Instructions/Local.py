from Environment.SymbolsTable import SymbolsTable
from Environment.Symbol import Symbol
from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class Local(Instruction):
    def __init__(self, fila, columna,  id:str) -> None:
        super().__init__(fila,columna)
        self.id = id
        self.fila = fila
        self.columna = columna

    def compile(self, environment: Environment) -> Value:

        tempVar: Symbol = environment.saveVariable(self.id,typeExpression.UNDEFINED, self.fila, self.columna)
        tmpTabla = SymbolsTable()
        tmpTabla.setNewSimbol(tempVar)
        self.generator.addSetStack(str(tempVar.position),str(0))