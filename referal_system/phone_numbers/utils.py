import random
import string


def generate_invite_code() -> str:
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(characters, k=6))
    return code


def generate_verifircation_code() -> str:
    return random.randint(1000, 9999)
