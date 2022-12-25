# Construyendo el analizador léxico
import Grammar.ply.yacc as yacc
import Grammar.ply.lex as lex
from Expression.Relational.Menor import Menor
from Instructions.Lower import Lower
from Instructions.Print import Print
from Instructions.Println import Println
from Expression.Primitive.NumberVal import NumberVal
from Expression.Primitive.Cadena import Cadena
from Expression.Logic.Not import Not
from Expression.Logic.And import And
from Expression.Logic.Or import Or
from Environment.Environment import Environment
from Enum.typeExpression import typeExpression
from Generator.Generator import Generator
from Expression.Relational.Equal import Equal
from Instructions.Declaration import Declaration
from Instructions.DeclararArray import DeclararArray
from Instructions.AsignArray import AsignArray
from Instructions.SetGlobal import SetGlobal
from Instructions.Global import Global
from Instructions.Local import Local
from Instructions.Asignacion import Asignacion
from Instructions.Break import Break
from Instructions.Continue import Continue
from Expression.Primitive.VariableCall import VariableCall
from Instructions.Upper import Upper
from Instructions.While import While
from Expression.Arithmetic.Multiply import Multiply
from Expression.Arithmetic.PlusMinusModDivision import PlusMinusModDivision
from Expression.Arithmetic.Potency import Potency
from Enum.arithmeticOperation import arithmeticOperation
from Expression.Relational.Relacional import Relacional
from Enum.relationalOperation import relationalOperation
from Instructions.If import If
from Instructions.For import For
from Instructions.Funcion import Funcion
from Instructions.Len import Len
from Instructions.Str import Str
from Expression.Primitive.Booleano import Booleano
from Instructions.Llamada import Llamada
from Instructions.Return import Return

'''
######## Proyecto Vacas Diciembre 2022 ########
########          Gramatica            ########
'''

errores = []
variables = []
funciones = []
inp = ""


reservadas = {
    'None': 'RNULL',
    'int': 'RINT',
    'float': 'RFLOAT',
    'bool': 'RBOOLEAN',
    'string': 'RSTRING',
    'print': 'RPRINT',
    'upper': 'RUPPER',
    'lower': 'RLOWER',
    'println': 'RPRINTLN',
    'and': 'RAND',
    'or': 'ROR',
    'not': 'RNOT',
    'global': 'RGLOBAL',
    'struct' : 'RSTRUCT',
    'local': 'RLOCAL',
    'if': 'RIF',
    'elif': 'RELIF',
    'else': 'RELSE',
    'break': 'RBREAK',
    'while': 'RWHILE',
    'for': 'RFOR',
    'in': 'RIN',
    'range': 'RRANGE',
    'return': 'RRETURN',
    'continue': 'RCONTINUE',
    'def': 'RDEF',
    'len': 'RLEN',
    'str': 'RSTR',
}

tokens = [
    'PUNTOCOMA',
    'COMA',
    'DOSPUNTOS',
    'PARA',
    'PARC',
    'LLAVEA',
    'LLAVEC',
    'CORA',
    'CORC',
    'MAS',
    'MENOS',
    'INCREMENTO',
    'DECREMENTO',
    'POR',
    'DIV',
    'POT',
    'MOD',
    'MENORQUE',
    'MAYORQUE',
    'IGUALIGUAL',
    'IGUAL',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID',
    'BOOLEANO',
    'CHARACTER',
    'DIFERENTE',
    'MAYORIGUAL',
    'MENORIGUAL'
] + list(reservadas.values())

# Asignacion de valor de tokens
t_PUNTOCOMA = r';'
t_COMA = r','
t_DOSPUNTOS = r':'
t_PARA = r'\('
t_PARC = r'\)'
t_LLAVEA = r'{'
t_LLAVEC = r'}'
t_CORA = r'\['
t_CORC = r'\]'
t_MAS = r'\+'
t_POR = r'\*'
t_DIV = r'/'
t_POT = r'\*\*'
t_MOD = r'%'
t_MENOS = r'-'
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_IGUALIGUAL = r'=='
t_IGUAL = r'='
t_DIFERENTE = r'!='
t_MENORIGUAL = r'<='
t_MAYORIGUAL = r'>='

# Decimal


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

# Booleano


def t_BOOLEANO(t):
    r'True|False'
    try:
        if t.value == 'True':
            t.value = True
        elif t.value == 'False':
            t.value = False
    except ValueError:
        print("Value not boolean %d", t.value)
        t.value = 0
    return t

# Caracter (Char)


def t_CHARACTER(t):
    r'\'(\\\'|\\"|\\t|\\n|\\\\|[^\'\\])?\''
    t.value = t.value[1:-1]
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace("\\'", "\'")
    t.value = t.value.replace('\\\\', '\\')
    return t

# Entero


def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# ID
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'ID')
    return t

# Cadena


def t_CADENA(t):
    r'\"(\\"|.)*?\"'
    t.value = t.value[1:-1]
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace("\\'", "\'")
    t.value = t.value.replace('\\\\', '\\')
    return t


# Comentario multilinea
def t_COMENTARIO_MULTILINEA(t):
    r'\#\=(.|\n)*?\=\#'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple


def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1


# Caracteres ignorados
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# ------------------------- Analizador Sintactico----------------


# Asociación de operadores y precedencia
precedence = (
    ('left', 'ROR'),
    ('left', 'RAND'),
    ('right', 'UNOT'),
    ('left', 'MENORQUE', 'MAYORQUE', 'MAYORIGUAL',
     'MENORIGUAL', 'DIFERENTE', 'IGUALIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIV', 'MOD'),
    ('nonassoc', 'POT'),
    ('right', 'UMENOS'),
)

#Contador de columnas
def find_column(token, index):
    global inp
    line_start = 0
    line_start = inp.rfind('\n', 0, (token.lexpos(index))) +1
    return (token.lexpos(index) - line_start) + 1

# ///////////////////////////////////////GRAMATICA//////////////////////////////////////////////////

def p_init(t):
    'init            : instrucciones'
    generator: Generator = Generator()
    globalEnv = Environment(None, "Global")
    for ins in t[1]:
        ins.generator = generator
        ins.compile(globalEnv)

    
    t[0] = generator.getCode()


def p_instrucciones_instrucciones_instruccion(t):
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]

# ///////////////////////////////////////INSTRUCCIONES//////////////////////////////////////////////////


def p_instrucciones_instruccion(t):
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]

# ///////////////////////////////////////INSTRUCCION//////////////////////////////////////////////////


def p_instruccion(t):
    '''instruccion      : imprimir_instr
                        | declaracion_instr
                        | imprimir_instr2
                        | upper_instr
                        | lower_instr
                        | asignacion_instr
                        | global_asig
                        | global_ins
                        | local_ins
                        | if_instr
                        | decl_arr_uni
                        | acc_arr_uni
                        | for_instr
                        | while_instr
                        | break_instr
                        | continue_instr
                        | funcion_instr
                        | llamada_instr
                        | return_instr
                        | len_instr
                        | str_instr'''
    t[0] = t[1]

# ///////////////////////////////////////IMPRIMIR//////////////////////////////////////////////////


def p_imprimir(t):
    '''
    imprimir_instr     : RPRINT PARA expresion PARC PUNTOCOMA
    | RPRINT PARA expresion PARC 
    '''
    t[0] = Print(t.lineno(1), find_column(t, 3), t[3])

# ///////////////////////////////////////IMPRIMIR SALTO//////////////////////////////////////////////////

def p_declaracion1(t) :
    '''
    declaracion_instr     : ID DOSPUNTOS tipo IGUAL expresion
    '''
    t[0] = Declaration(t.lineno(1), find_column(t, 3), t[1],t[5],t[3])

def p_tipo(t) :
    '''
    tipo     : RINT
             | RFLOAT
             | RBOOLEAN
             | RSTRING
    '''
    if t[1] == 'string' : t[0] = typeExpression.STRING
    elif t[1] == 'int' : t[0] = typeExpression.INT
    elif t[1] == 'float' : t[0] = typeExpression.FLOAT
    elif t[1] == 'bool' : t[0] = typeExpression.BOOL

def p_imprimir2(t):
    '''
    imprimir_instr2     : RPRINTLN PARA expresion PARC PUNTOCOMA
    | RPRINTLN PARA expresion PARC 
    '''
    if t[1] == 'string' : t[0] = typeExpression.STRING
    elif t[1] == 'int' : t[0] = typeExpression.INT
    elif t[1] == 'float' : t[0] = typeExpression.FLOAT
    elif t[1] == 'bool' : t[0] = typeExpression.BOOL

# ///////////////////////////////////////UPPER_LOWER//////////////////////////////////////////////////


def p_upper(t):
    '''
    upper_instr     : RUPPER PARA expresion PARC 
    '''
    t[0] = Upper(t.lineno(1), find_column(t, 1), t[3])

def p_lower(t):
    '''
    lower_instr     : RLOWER PARA expresion PARC 
    '''
    t[0] = Lower(t.lineno(1), find_column(t, 1), t[3])

# ///////////////////////////////////////NATIVAS PRIMITIVAS//////////////////////////////////////////////////
def p_len(t):
    '''
    len_instr       : RLEN PARA expresion PARC 
    '''
    t[0] = Len(t.lineno(1), find_column(t,1),t[3])

def p_str(t):
    '''
    str_instr       : RSTR PARA expresion PARC 
    '''
    t[0] = Str(t.lineno(1), find_column(t, 1),t[3])

# ///////////////////////////////////////ASIGNACION//////////////////////////////////////////////////

def p_asignacion(t):
    '''
    asignacion_instr     : ID IGUAL expresion
    '''
    t[0] = Asignacion(t.lineno(1), find_column(t, 2),t[1], t[3])

# ///////////////////////////////////////GLOBAL//////////////////////////////////////////////////

def p_global(t):
    '''
    global_asig     : RGLOBAL ID IGUAL expresion
    '''
    t[0] = SetGlobal(t.lineno(1), find_column(t, 3),t[2], t[4])


def p_global2(t):
    '''
    global_ins     : RGLOBAL ID
    '''
    t[0] = Global(t.lineno(1), find_column(t, 2),t[2])


# ///////////////////////////////////////LOCAL//////////////////////////////////////////////////

def p_local(t):
    '''
    local_ins     : RLOCAL ID
    '''
    t[0] = Local(t.lineno(1), find_column(t, 1),t[2])

# ///////////////////////////////////////IF//////////////////////////////////////////////////
# //////////////// COLOCAR APARTADO DE TABULACIONES ENTRE DOSPUNTOS, SE BORRARON LLAVEA Y LLAVEC


def p_if1(t):
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC'
    print("IIIIIIIIIIIIIIIIIIIIF -> " + str(t[3]))
    t[0] = If(t.lineno(1), find_column(t, 4),t[3],t[6],None,None)


def p_if2(t):
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC RELSE LLAVEA instrucciones LLAVEC'
    print("IFFFFFFFFFFFF ELSEEEEEEEEEEEEE" + str(t[3]))
    t[0] = If(t.lineno(1), find_column(t, 4),t[3],t[6],t[10],None)


def p_if3(t):
    'if_instr     : RELIF PARA expresion PARC LLAVEA instrucciones LLAVEC RELSE LLAVEA instrucciones LLAVEC'
    t[0] = If(t.lineno(1), find_column(t, 4),t[3],t[6],t[10],None)


def p_if4(t):
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC if_instr'
    t[0] = If(t.lineno(1), find_column(t, 4),t[3],t[6],None,t[8])

def p_if5(t):
    'if_instr     : RELIF PARA expresion PARC LLAVEA instrucciones LLAVEC if_instr'
    t[0] = If(t.lineno(1), find_column(t, 4),t[3],t[6],None,t[8])


def p_if6(t):
    'if_instr     : RELIF PARA expresion PARC LLAVEA instrucciones LLAVEC'
    t[0] = If(t.lineno(1), find_column(t, 4),t[3],t[6],None,None)


# ///////////////////////////////////////WHILE//////////////////////////////////////////////////


def p_while(t):
    'while_instr     : RWHILE PARA expresion PARC DOSPUNTOS LLAVEA instrucciones LLAVEC'
    t[0]=While(t.lineno(1), find_column(t, 4), t[3],t[7])

def p_while1(t):
    'while_instr     : RWHILE expresion DOSPUNTOS LLAVEA instrucciones LLAVEC'
    t[0]=While(t.lineno(1), find_column(t, 4), t[2],t[5])

# ///////////////////////////////////////BREAK//////////////////////////////////////////////////


def p_break(t):
    'break_instr     : RBREAK'
    t[0] = Break(t.lineno(1), find_column(t, 1),)

# ///////////////////////////////////////CONTINUE//////////////////////////////////////////////////


def p_continue(t):
    'continue_instr     : RCONTINUE'
    t[0] = Continue(t.lineno(1), find_column(t, 1),)

# ///////////////////////////////////////FOR//////////////////////////////////////////////////


def p_for_instr_1(t):
    '''
    for_instr : RFOR ID RIN RRANGE PARA expresion PARC LLAVEA instrucciones LLAVEC  
    '''
    valorInicial = NumberVal(t.lineno(1), find_column(t, 1), typeExpression.INT, 0)
    declaracion = Declaration(t.lineno(1), find_column(t, 1), t[2],valorInicial,typeExpression.INT)
    llamadaId = VariableCall(t.lineno(1), find_column(t, 1), t[2])
    condition = Relacional(t.lineno(1), find_column(t, 1), llamadaId,t[6],relationalOperation.MENOR)
    
    valorIncremento = NumberVal(t.lineno(1), find_column(t, 1), typeExpression.INT, 1)
    expresionIncremento=PlusMinusModDivision(t.lineno(1), find_column(t, 1), llamadaId,valorIncremento,arithmeticOperation.PLUS)
    asignacionIncremento  = Asignacion(t.lineno(1), find_column(t, 1), t[2], expresionIncremento)
    t[0]=For(t.lineno(1), find_column(t, 1), declaracion,condition,typeExpression.INT,asignacionIncremento,t[9])

def p_for_instr_2(t):
    '''
    for_instr : RFOR ID RIN expresion PARA expresion PARC LLAVEA instrucciones LLAVEC  
    '''
# ///////////////////////////////////////FUNCION//////////////////////////////////////////////////


def p_funcion_1(t):
    'funcion_instr     : RDEF ID PARA parametros PARC LLAVEA instrucciones LLAVEC'
    t[0] = Funcion(t.lineno(1), find_column(t, 4), t[2], t[4], t[7])


def p_funcion_2(t):
    'funcion_instr     : RDEF ID PARA PARC LLAVEA instrucciones LLAVEC'
    t[0] = Funcion(t.lineno(1), find_column(t, 4), t[2], None, t[6])

# ///////////////////////////////////////PARAMETROS//////////////////////////////////////////////////


def p_parametros_1(t):
    'parametros     : parametros COMA parametro'
    t[1].append(t[3])
    t[0] = t[1]


def p_parametros_2(t):
    'parametros    : parametro'
    t[0] = [t[1]]

# ///////////////////////////////////////PARAMETRO//////////////////////////////////////////////////


def p_parametro(t):
    'parametro     : ID DOSPUNTOS tipo'
    t[0] = {'identificador': t[1], 'tipo': t[3], 'struct_type': None}

# ///////////////////////////////////////LLAMADA A FUNCION//////////////////////////////////////////////////


def p_return(t):
    'return_instr     : RRETURN'
    t[0] = Return(t.lineno(1), find_column(t, 1),None)

def p_return1(t):
    'return_instr     : RRETURN expresion'
    t[0] = Return(t.lineno(1), find_column(t, 1),t[2])


def p_llamada1(t):
    'llamada_instr     : ID PARA PARC'
    t[0] = Llamada(t.lineno(1), find_column(t, 1),t[1],[])


def p_llamada2(t):
    'llamada_instr     : ID PARA parametros_llamada PARC'
    t[0] = Llamada(t.lineno(1), find_column(t, 1),t[1],t[3])

# ///////////////////////////////////////PARAMETROS LLAMADA A FUNCION//////////////////////////////////////////////////


def p_parametrosLL_1(t):
    'parametros_llamada     : parametros_llamada COMA parametro_llamada'
    t[1].append(t[3])
    t[0] = t[1]


def p_parametrosLL_2(t):
    'parametros_llamada    : parametro_llamada'
    t[0] = [t[1]]

# ///////////////////////////////////////PARAMETRO LLAMADA A FUNCION//////////////////////////////////////////////////


def p_parametroLL(t):
    'parametro_llamada     : expresion'
    t[0] = t[1]

# ///////////////////////////////////////DECLARACION ARREGLOS//////////////////////////////////////////////////

def p_accesArrUni(t):
    'acc_arr_uni : ID CORA ENTERO CORC IGUAL expresion'
    print("IN ARRAY ")
    t[0] = AsignArray(t.lineno(1), find_column(t, 1), t[1],t[3],t[6])


def p_declArrUni(t):
    'decl_arr_uni : ID IGUAL CORA list_values CORC'
    t[0] = DeclararArray(t.lineno(1), find_column(t, 1), t[1],t[4],typeExpression.LIST)

def p_list_valores(t):
    'list_values : list_values COMA expresion '
    t[1].append(t[3])
    t[0] = t[1]


def p_list_valores2(t):
    'list_values : expresion '
    t[0] = [t[1]]



# ///////////////////////////////////////EXPRESION//////////////////////////////////////////////////

# Expresion binaria
def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
            | expresion DIV expresion
            | expresion POT expresion
            | expresion MOD expresion
            | expresion MENORQUE expresion
            | expresion MAYORQUE expresion
            | expresion MENORIGUAL expresion
            | expresion MAYORIGUAL expresion
            | expresion DIFERENTE expresion
            | expresion IGUALIGUAL expresion
            | expresion RAND expresion
            | expresion ROR expresion
    '''
    if t[2] == '+'  : t[0] = PlusMinusModDivision(t.lineno(1), find_column(t, 2), t[1],t[3],arithmeticOperation.PLUS)
    elif t[2] == '-': t[0] = PlusMinusModDivision(t.lineno(1), find_column(t, 2), t[1],t[3],arithmeticOperation.MINUS)    
    elif t[2] == '%': t[0] = PlusMinusModDivision(t.lineno(1), find_column(t, 2), t[1],t[3],arithmeticOperation.MODULE)
    elif t[2] == '/': t[0] = PlusMinusModDivision(t.lineno(1), find_column(t, 2), t[1],t[3],arithmeticOperation.DIV)
    elif t[2] == '*': t[0] = Multiply(t.lineno(1), find_column(t, 2), t[1],t[3])
    elif t[2] == '**': t[0] = Potency(t.lineno(1), find_column(t, 2), t[1],t[3])
    elif t[2] == 'and': t[0] = And(t.lineno(1), find_column(t, 2), t[1],t[3])
    elif t[2] == 'or': t[0] = Or(t.lineno(1), find_column(t, 2), t[1],t[3])
    elif t[2] == '<': t[0] = Relacional(t.lineno(1), find_column(t, 2), t[1],t[3],relationalOperation.MENOR)
    elif t[2] == '>': t[0] = Relacional(t.lineno(1), find_column(t, 2), t[1],t[3],relationalOperation.MAYOR)
    elif t[2] == '<=': t[0] = Relacional(t.lineno(1), find_column(t, 2), t[1],t[3],relationalOperation.MENORIGUAL)
    elif t[2] == '>=': t[0] = Relacional(t.lineno(1), find_column(t, 2), t[1],t[3],relationalOperation.MAYORIGUAL)
    elif t[2] == '==': t[0] = Relacional(t.lineno(1), find_column(t, 2), t[1],t[3],relationalOperation.IGUAL)
    elif t[2] == '!=': t[0] = Relacional(t.lineno(1), find_column(t, 2), t[1],t[3],relationalOperation.DIFERENTE)

# Expresion unaria


def p_expresion_unaria(t):
    '''
    expresion : MENOS expresion %prec UMENOS 
            | RNOT expresion %prec UNOT 
    '''
    if t[1] == 'not'  : t[0] = Not(t.lineno(1), find_column(t, 1), t[2])

# Expresion agrupacion


def p_expresion_agrupacion(t):
    '''
    expresion :   PARA expresion PARC 
    '''
    t[0] = t[2]

# Expresion llamada


def p_expresion_llamada(t):
    '''expresion : llamada_instr'''
    t[0] = t[1]

 # Expresiones y primitivos


def p_expresion_identificador(t):
    '''expresion : ID'''
    t[0] = VariableCall(t.lineno(1), find_column(t, 1),t[1])


def p_expresion_entero(t):
    '''expresion : ENTERO'''
    t[0] = NumberVal(t.lineno(1), find_column(t, 1),typeExpression.INT, t[1])


def p_primitivo_decimal(t):
    '''expresion : DECIMAL'''
    t[0] = NumberVal(t.lineno(1), find_column(t, 1),typeExpression.FLOAT, t[1])


def p_primitivo_cadena(t):                  #
    '''expresion : CADENA'''
    t[0] = Cadena(t.lineno(1), find_column(t, 1),typeExpression.STRING, t[1])

def p_nativa_upper(t):                  #
    '''expresion : upper_instr'''
    t[0] = t[1]

def p_nativa_lower(t):                  #
    '''expresion : lower_instr'''
    t[0] = t[1]

def p_nativa_len(t):
    '''expresion : len_instr'''
    t[0] = t[1]

def p_nativa_str(t):
    '''expresion : str_instr'''
    t[0] = t[1]


def p_primitivo_booleano(t):
    '''expresion : BOOLEANO'''
    t[0] = Booleano(t.lineno(1), find_column(t, 1),typeExpression.BOOL, t[1])


def p_primitivo_null(t):
    '''expresion : RNULL'''


def p_error(t):
    print("Error sintáctico en '%s'" % t.value)

parser = yacc.yacc()