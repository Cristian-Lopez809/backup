import enum

class typeExpression(enum.Enum):
    NULL = 0
    INT = 1
    FLOAT = 2
    BOOL = 3
    STRING = 4
    LIST = 5
    STRUCT = 6
    UNDEFINED = 7
    RETURN_ST = 8
    BREAK_ST = 9
    CONTINUE_ST = 10
    FUNCION = 11
    LIST_INTFL = 12
    LIST_BOOL = 13
    LIST_STRING = 14

class Return:
    def __init__(self, value, ret_type, is_temp, aux_type=''):
        self.value = value
        self.type = ret_type
        self.is_temp = is_temp
        self.struct_type = aux_type
        self.true_lbl = ''
        self.false_lbl = ''