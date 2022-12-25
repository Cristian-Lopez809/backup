from Abstract.Expression import Expression
from Abstract.Instruction import Instruction
from Environment.Environment import Environment
from Environment.Value import Value
from Enum.typeExpression import typeExpression

class Llamada(Instruction):
    def __init__(self, fila, columna,  id ,param) -> None:
        super().__init__(fila,columna)
        self.id = id
        self.param = param
        self.fila = fila
        self.columna = columna
    
    def compile(self, environment: Environment) -> Value:
        try:
            print("hola")
            funciones = environment.getFuncion(self.id)
            if funciones is not None:
                parametros = []
                size = environment.size
                for parms in self.param:
                    parametros.append(parms.compile(environment))
                newTemp = self.generator.newTemp()
                self.generator.addExpression(newTemp, 'P', str(size),'+')
                auxiliar = 0
                for parms1 in parametros:
                    auxiliar += 1
                    self.generator.addSetStack(newTemp, parms1.value)
                    if auxiliar != len(parametros):
                        self.generator.addExpression(newTemp, newTemp, '1', '+')
                self.generator.addNextStack(str(size))
                self.generator.addCallFunc(self.id)
                self.generator.addGetStack(newTemp, 'P')
                self.generator.addBackStack(str(size))
                return Value(newTemp,True,typeExpression.NULL)
        except Exception as e:
            print("Me dio Ansiedad Aqui en llamada")