import ply.lex as lex
import ply.yacc as yacc
import csv

# Definição dos tokens
tokens = (
    'SEQID', 'SOURCE', 'TYPE', 'START', 'END', 'SCORE', 'STRAND', 'PHASE', 'ATTRIBUTE'
)


# Ignorar comentários
def t_COMMENT(t):
    r'\#.*'
    pass


# Ignorar espaços e tabulações
t_ignore = ' '


def t_SEQID(t):
    r'[^\t\n]+'
    return t


def t_SOURCE(t):
    r'[^\t\n]+'
    return t


def t_TYPE(t):
    r'[^\t\n]+'
    return t


def t_START(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_END(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_SCORE(t):
    r'[^\t\n]+'
    return t


def t_STRAND(t):
    r'[+-]'
    return t


def t_PHASE(t):
    r'[012.]'
    return t


def t_ATTRIBUTE(t):
    r'[^\n]+'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass


def t_error(t):
    print(f"Erro léxico: Caracter inválido '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()


# Definição da gramática
def p_gff(p):
    'gff : lines'
    p[0] = p[1]


def p_lines(p):
    '''lines : lines line
             | line'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_line(p):
    'line : SEQID SOURCE TYPE START END SCORE STRAND PHASE ATTRIBUTE'
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9])


def p_error(p):
    if p:
        print(f"Erro de sintaxe: Token inesperado '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe: Fim inesperado do arquivo")


parser = yacc.yacc()


def parse_gff(file_path, output_csv):
    with open(file_path, 'r') as file:
        data = [line.strip() for line in file.readlines() if not line.startswith('#') and line.strip()]

    print("Iniciando parsing do arquivo...")
    parsed_data = []

    for line in data:
        fields = line.split('\t')
        if len(fields) != 9:
            print(f"Linha ignorada (número incorreto de colunas): {line}")
            continue
        parsed_data.append(tuple(fields))

    if not parsed_data:
        print("Erro: Nenhum dado foi extraído do arquivo GFF.")
        return

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['SeqID', 'Source', 'Type', 'Start', 'End', 'Score', 'Strand', 'Phase', 'Attribute'])
        writer.writerows(parsed_data)

    print(f"Arquivo CSV '{output_csv}' gerado com sucesso.")

# Exemplo de uso:
parse_gff('genomic.gff', 'output.csv')
