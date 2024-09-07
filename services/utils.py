# utils.py
import random
import string

def generate_secret_code(length=8):
    """Generate a random secret code with letters and digits."""
    characters = string.ascii_letters + string.digits
    secret_code = ''.join(random.choice(characters) for _ in range(length))
    return secret_code
