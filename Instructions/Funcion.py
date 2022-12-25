from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression
from Environment.SymbolsTable import SymbolsTable
from Environment.Symbol import Symbol

class Funcion(Instruction):
    def __init__(self, fila, columna,  id ,param, block:Instruction) -> None:
        super().__init__(fila,columna)
        self.id = id
        self.param = param
        self.block = block
        self.fila = fila
        self.columna = columna
        
    def compile(self, environment: Environment) -> Value:
        tmpFunc:Symbol = environment.saveFuncion(self.id,self, self.fila, self.columna)
        tmpTabla = SymbolsTable()
        tmpTabla.setNewSimbol(tmpFunc)
        #self.block.generator = self.generator
        newEnv = Environment(environment, "Funcion-"+self.id)
        lblrtn =  self.generator.newLabel()
        newEnv.labelRtn = lblrtn
        newEnv.size = 1
        print(self.param)
        if self.param != None:
            for parm in self.param:
                newEnv.saveVariable(parm["identificador"]+"#", parm["tipo"], self.fila, self.columna,(parm["tipo"] == typeExpression.STRING or parm["tipo"] == typeExpression.STRUCT or parm["tipo"] == typeExpression.INT), parm["struct_type"])
        self.generator.inicioFuncion(self.id)
        try:
            for ins in self.block:
                ins.generator = self.generator
                ins.compile(newEnv)
        except Exception as e:
            print("Me dio ansiedad compilar")
        self.generator.finFuncion()