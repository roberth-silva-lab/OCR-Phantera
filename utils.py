import re

def limpar_texto(t):
    return re.sub(r'[^A-Z0-9]', '', t.upper())
