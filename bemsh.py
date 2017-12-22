# -*- coding: utf-8 -*-
""" BEMSH-subset assembler """
import re
from pprint import pprint
from ply import lex, yacc

"""
    В трансляторе БЕМШ зарезервированы следующие управляюще команды:
"""
TRAN_KEYWORDS = ("код", "старт", "финиш", "адрес", "литер", "стрн", "строк",
                 "экв", "пам", "конд", "текст", "конк",
                 "употр", "отмен", "входн", "внеш")

"""
    Список коротких программ в порядке возрастания кода операции
"""
OP_SHORT = ("зп", "зпм", "рег", "счм", "сл", "вч", "вчоб", "вчаб",
            "сч", "и", "нтж", "слц", "знак", "или", "дел", "умн",
            "сбр", "рзб", "чед", "нед", "слп", "вчп", "сд", "рж",
            "счрж", "счмр", "э32", "увв", "слпа", "вчпа", "сда", "ржа",
            "уи", "уим", "счи", "счим", "уии", "сли", "э46", "э47",
            "э50", "э51", "э52", "э53", "э54", "э55", "э56", "э57",
            "э60", "э61", "э62", "э63", "э64", "э65", "э66", "э67",
            "э70", "э71", "э72", "э73", "э74", "э75", "э76", "э77")
"""
    Список длинных команд в порядке возростания кода операции
"""
OP_LONG = ("э20", "э21", "мода", "мод", "уиа", "слиа", "по", "пе",
           "пб", "пв", "выпр", "стоп", "пио", "пино", "э36", "цикл")

""" Ключевые слова компилятора """
KEYWORDS = OP_SHORT + OP_LONG

""" Словарь соответсвия мнемонике коду операции """
OPCODE_NUM = {KEYWORDS[i]: i for i in range(0, len(KEYWORDS))}

""" Распознаваемые токены для лекс. анализатора """
tokens = (
    'ID', 'NUMBER', 'NEWLINE', 'OPCODE', 'TRAN'
)

""" Литералы """
literals = ['(', ')', '+', '-', '*', '/']

""" Комментарии пропускаем """
t_ignore_COMMENT = r'[\*;].*'

def t_NUMBER(t):
    r'(м\d+)?((\'?-?\d+\'?)|([вbк]\'\d+\')|(п\'.*\'))'
    if t.value[0] == '\'':
        t.value = int(t.value[1:-1], 8)
    elif t.value[0] in 'кk':
        t.value = int(t.value[2:-1], 2)
    elif t.value[0] in 'вbк':
        t.value = int(t.value[2:-1], 8)
    elif t.value[0] == 'п':
        t.value = t.value[2:-1]
    elif t.value[0] == 'м':  # TODO: константа со здвигом влево
        p = r"м(?P<mod>\d+)[вb]'(?P<num>\d+)'"
        res = re.findall(p, t.value)
        t.value = int(res[0][1], 8) << int(res[0][0])
    else:
        t.value = int(t.value)
    return t

t_ignore = " \r\t"

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t


def t_ID(t):
    r'[a-zA-Zа-яА-Я]+[a-zA-Zа-яА-Я0-9]*'
    if t.value in TRAN_KEYWORDS:
        t.type = 'TRAN'
    elif t.value in KEYWORDS:
        t.type = 'OPCODE'
    return t


def t_error(t):
    print("Illegal character '%s' at line %d" % (t.value[0], t.lexer.lineno))


lexer = lex.lex(reflags=re.UNICODE)


precedence = (
    ('left', '+', '-'),
    #    ('left', '*', '/'),
    #    ('right', 'UMINUS'),
)


def p_prog_list(p):
    '''prog : prog statement
            | statement'''
    if len(p) == 2:
        if p[1] is None:
            p[1] = [('EMPTY', 0, 0)]
        p[0] = [p[1]]
    elif len(p) == 3:
        #print(p[0], p[1], p[2])
        if p[2] is not None:
            p[1].append(p[2])
        p[0] = p[1]


def p_tran_directive(p):
    '''tran_dir : TRAN NUMBER
                | TRAN'''
    if len(p) == 2:
        p[0] = ('TRAN', p[1])
    else:
        p[0] = ('TRAN', p[1], p[2])


def p_expr(p):
    """ expr : NUMBER
             | ID
             | expr '+' expr
             | expr '-' expr"""
    if len(p) == 2:
        # print(p[1], p.lexer.lexdata, repr(p))
        if not isinstance(p[1], int):
            p[0] = ('LABEL', p[1])
        else:
            p[0] = p[1]
    elif len(p) == 4:
        if isinstance(p[1], int) and isinstance(p[3], int):
            if p[2] == '+':
                p[0] = p[1] + p[3]
            else:
                p[0] = p[1] - p[3]
        else:
            p[0] = (p[2], p[1], p[3])


def p_addr(p):
    """addr : expr
            | expr '(' expr ')'
            | '(' expr ')'"""
    if len(p) == 2:
        p[0] = {"offset": p[1], "idx": 0}
    elif len(p) == 5:
        p[0] = {"offset": p[1], "idx": p[3]}
    elif len(p) == 4:
        p[0] = {"offset": 0, "idx": p[2]}


def p_instruction(p):
    ''' instruction : OPCODE
                    | OPCODE addr'''
    if len(p) == 3:
        p[0] = ('OPCODE', p[1], p[2])
    else:
        p[0] = ('OPCODE', p[1], {"offset": 0, "idx": 0})


def p_label(p):
    '''statement : ID'''
    p[0] = ('LABEL', p[1])


def p_stat_nl(p):
    '''statement : NEWLINE'''


def p_statement(p):
    '''statement : tran_dir NEWLINE
                 | instruction NEWLINE'''
    p[0] = p[1]


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value, p.lineno)
    else:
        print("Syntax error at EOF")
    exit()


def collect_labels(prog):
    """ Сбор меток """
    labels = {}
    for i in prog:
        if i[0] == 'LABEL':
            labels[i[1]] = None
    return labels


def calc_tree(labels, expr):
    """ Вычисление адресного выражения операнда команды """
    if isinstance(expr, int):
        return expr
    if expr[0] == 'LABEL':
        result = labels[expr[1]]
    elif expr[0] == '+':
        result = calc_tree(labels, expr[1]) + calc_tree(labels, expr[2])
    elif expr[0] == '-':
        result = calc_tree(labels, expr[1]) - calc_tree(labels, expr[2])
    else:
        print("Unkonown oper in expr", expr)
    return result


def pack_instructions(prog):
    """ Укладывание команд в память во внутреннее представление программы """
    cur_addr = 0  # адрес в полусловах, т.е. одно слово занимает два полуслова

    # проход по дереву - определение списка меток
    labels = collect_labels(prog)

    memory = []
    # проход по дереву - укладывание команд в память
    for i in prog:
        if i[0] == 'LABEL':                 # если метка и правая команда
            if cur_addr % 2 == 1:           # то вставляема "мода 0"
                memory.append(
                    (cur_addr, ('OPCODE', 'мода', {
                        'idx': 0, 'offset': 0})))
                cur_addr += 1
            labels[i[1]] = cur_addr // 2    # сопоставление адрес соотв. метке
            # в машинных словах
            continue
        elif i[0] == 'TRAN':
            if i[1] == 'старт' or i[1] == 'адрес':
                cur_addr = int(i[2]) * 2    # директива старт
            elif i[1] == 'конд':            # длинная константа занимает одно слово
                if cur_addr % 2 == 1:       # поэтому выравниваем если необходимо
                    memory.append(
                        (cur_addr, ('OPCODE', 'мода', {
                            'idx': 0, 'offset': 0})))
                    cur_addr += 1
                memory.append((cur_addr, ('TRAN', 'конк', i[2] >> 24)))
                memory.append((cur_addr+1, ('TRAN', 'конк', i[2] & 0o77777777)))
                cur_addr += 2
            elif i[1] == 'конк':            # короткая константа занимает полуслово
                memory.append((cur_addr, i))
                cur_addr += 1
            elif i[1] == 'текст':           # укладываем текст по 6 букв в машинные слова
                j = 0
                text = i[2].encode('utf-8')
                while j < len(text):
                    t = text[j:j + 6]
                    j += 6
                    if len(t) < 6:
                        t += b' ' * (6 - len(t))
                    memory.append((cur_addr, ('TRAN', 'конк', t[:3])))
                    memory.append((cur_addr + 1, ('TRAN', 'конк', t[3:])))
                    cur_addr += 2
            else:
                print("Неизвестная директива", i[1])
                exit()
            continue
        elif i[0] == 'OPCODE':
            memory.append((cur_addr, i))
            cur_addr += 1
            continue
        else:
            print("Warning: Unknown token:", i)

    if cur_addr % 2 == 1:
        memory.append((cur_addr, ('OPCODE', 'мода', {'idx': 0, 'offset': 0})))

    print("Внутреннее представление:")
    for m in memory:
        print('Address: {:0>8o} Data: {:0>20}'.format(m[0] // 2, str(m[1])))

    print("Адреса меток:")
    for m in labels.items():
        print('Label: {:<8} Address: {:0>5o}'.format(m[0], m[1]))

    # после того как стали известны адреса меток,
    # вычислим адресные выражения команд
    for i in range(0, len(memory)):
        if memory[i][1][0] == 'OPCODE' and not isinstance(
                memory[i][1][2]['offset'], int):
            memory[i][1][2]['offset'] = calc_tree(
                labels, memory[i][1][2]['offset'])
    return memory


def gen_instr(cmd):
    """ Получение машинного кода по мнемонике и адресному выражению """
    global OPCODE_NUM
    op = 0

    if cmd[0] == 'OPCODE':
        mc = ((cmd[2]['idx'] << 20) & 0o74000000)
        if cmd[1] in OP_SHORT:
            op = (OPCODE_NUM[cmd[1]] << 12) & 0o770000
            op |= (cmd[2]['offset'] & 0o7777)
        else:
            op = (OPCODE_NUM[cmd[1]] << 15) & 0o3700000 | 0o2000000
            op |= (cmd[2]['offset'] & 0o77777)
        op |= mc
    elif cmd[0] == 'TRAN' and cmd[1] == 'конк':
        if isinstance(cmd[2], int):
            op = cmd[2]
        else:
            op = (cmd[2][0] << 16) | (cmd[2][1] << 8) | cmd[2][2]
    return op


def gen_mcode(mem):
    """ Укладывание двух команд или коротких констант в машинное слово """
    mem_ret = []
    i = 0
    while i < len(mem)-1:
        mem_ret.append((mem[i][0]//2, (gen_instr(mem[i][1])<<24) | gen_instr(mem[i+1][1])))
        i += 2
    return mem_ret


yacc.yacc()

# ШАГ 1. Построение дерева разбора
prog = yacc.parse(open('simple.bemsh', encoding='utf-8').read())
print("Дерево разбора: ")
pprint(prog)

# ШАГ 2. Укладывание инструкций/констант в память и определение адресов меток
mem = pack_instructions(prog)

print("Вычисленные метки прописаны:")
pprint(mem)

# ШАГ 3. Генерирование машинного кода с упаковкой в слова по 48-бит
mem = gen_mcode(mem)
print("Машинный код")
for m in mem:
    print('Address: {:>6o} Data: {:0>16o}'.format(m[0], m[1]))