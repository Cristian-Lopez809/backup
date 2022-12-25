from Generator.Generator import Generator
from Environment.Value import Value
from abc import ABC, abstractclassmethod
from Environment.Environment import Environment

class Expression(ABC):

    def __init__(self, fila, columna) -> None:
        super().__init__()
        self.generator: Generator = None
        self.trueLabel = ""
        self.falseLabel = ""
        self.fila = fila
        self.columna = columna
        

    @abstractclassmethod
    def compile(self, environment: Environment) -> Value:
        pass