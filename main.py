import ply.lex as lex
import ply.yacc as yacc
import csv

# Definição dos tokens
tokens = (
    'COMMENT', 'SEQID', 'SOURCE', 'TYPE', 'START', 'END', 'SCORE', 'STRAND', 'PHASE', 'ATTRIBUTE'
)


def t_COMMENT(t):
    r'\#.*'
    pass  # Ignorar linhas de comentário


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_SEQID(t):
    r'[^\t\n]+'
    return t


t_SOURCE = t_TYPE = t_SCORE = t_STRAND = t_PHASE = t_ATTRIBUTE = t_SEQID
t_START = t_END = r'\d+'

t_ignore = ' \t'


def t_error(t):
    print(f"Caracter inválido: {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()


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
    p[0] = (p[1], p[2], p[3], int(p[4]), int(p[5]), p[6], p[7], p[8], p[9])


def p_error(p):
    print("Erro de sintaxe")


parser = yacc.yacc()


def parse_gff(file_path, output_csv):
    with open(file_path, 'r') as file:
        data = file.readlines()

    parsed_data = parser.parse(''.join(data))

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['SeqID', 'Source', 'Type', 'Start', 'End', 'Score', 'Strand', 'Phase', 'Attribute'])
        writer.writerows(parsed_data)

    print(f"Arquivo CSV '{output_csv}' gerado com sucesso.")

# Exemplo de uso:
# parse_gff('input.gff', 'output.csv')
