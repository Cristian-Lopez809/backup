from Generator.Generator import Generator
from Environment.Value import Value
from abc import ABC, abstractclassmethod
from Environment.Environment import Environment

class Instruction(ABC):

    def __init__(self, fila, columna) -> None:
        super().__init__()
        self.generator = Generator()
        self.fila = fila
        self.columna = columna

    @abstractclassmethod
    def compile(self, environment: Environment) -> Value:
        pass