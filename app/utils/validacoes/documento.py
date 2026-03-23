import re

def _char_to_int(c: str) -> int:
    """Converte caractere alfanumérico para valor inteiro segundo regra ASCII-48"""
    if c.isalpha():
        return ord(c.upper()) - 48
    return int(c)

def valida_documento(documento: str) -> bool:
    """
    Valida CPF ou CNPJ (suportando regras normais ou alfanuméricas)
    """
    # Remove pontuação para analisar o tamanho real
    doc_limpo = re.sub(r'[^A-Za-z0-9]', '', str(documento))
    
    if len(doc_limpo) == 11:
        return valida_cpf(doc_limpo)
    elif len(doc_limpo) == 14:
        return valida_cnpj(doc_limpo)
    else:
        return False

def valida_cpf(cpf: str) -> bool:
    """
    Valida CPF
    """
    cpf = ''.join(filter(str.isalnum, cpf))
    if len(cpf) != 11:
        return False
        
    # Verifica se os últimos 2 dígitos são realmente números (são verificadores)
    if not cpf[9:].isdigit():
        return False
        
    # Evita CPFs com todos os caracteres iguais
    if len(set(cpf)) == 1:
        return False
    
    valores = [_char_to_int(c) for c in cpf]
    
    # Valida primeiro dígito
    soma = sum(valores[i] * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    if resto >= 10:
        resto = 0
    if resto != valores[9]:
        return False
    
    # Valida segundo dígito
    soma = sum(valores[i] * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    if resto >= 10:
        resto = 0
    if resto != valores[10]:
        return False
    
    return True

def valida_cnpj(cnpj: str) -> bool:
    """
    Valida CNPJ
    """
    cnpj = ''.join(filter(str.isalnum, cnpj))
    if len(cnpj) != 14:
        return False
        
    # Verifica se os últimos 2 dígitos são realmente números (são verificadores)
    if not cnpj[12:].isdigit():
        return False
        
    # Evita CNPJs com todos os caracteres iguais
    if len(set(cnpj)) == 1:
        return False
    
    valores = [_char_to_int(c) for c in cnpj]
    
    # Pesos do CNPJ
    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    # Valida primeiro dígito verificador
    soma = sum(valores[i] * pesos_1[i] for i in range(12))
    resto = soma % 11
    resto = 0 if resto < 2 else 11 - resto
    if resto != valores[12]:
        return False
    
    # Valida segundo dígito verificador
    soma = sum(valores[i] * pesos_2[i] for i in range(13))
    resto = soma % 11
    resto = 0 if resto < 2 else 11 - resto
    if resto != valores[13]:
        return False
    
    return True