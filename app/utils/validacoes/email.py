import re

def valida_email(email: str) -> bool:
    """
    Valida email
    """
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None