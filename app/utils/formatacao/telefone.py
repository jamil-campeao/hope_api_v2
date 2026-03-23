import re

def formatar_telefone(telefone: str) -> str:
    """
    Formata número de telefone para o padrão brasileiro (XX) XXXX-XXXX ou (XX) XXXXX-XXXX
    """
    # Remove todos os caracteres não numéricos
    telefone = re.sub(r'\D', '', str(telefone))
    
    # Verifica se o telefone tem 10 ou 11 dígitos (com DDD)
    if len(telefone) == 10:
        # Formato: (XX) XXXX-XXXX
        return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
    elif len(telefone) == 11:
        # Formato: (XX) XXXXX-XXXX
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
    else:
        # Se não for 10 ou 11 dígitos, retorna o número original
        return telefone
