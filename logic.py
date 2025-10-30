import string
import secrets

def generate_keys(amount: int) -> list:
    """
    Generate a specified amount of keys with the pattern PDSMP-XXXX-XXXX.

    Args:
        amount (int): The number of keys to generate.

    Returns:
        list: A list of strings with the generated keys.
    """
    if amount <= 0:
        return []

    # Use uppercase letters and digits for random characters
    alphabet = string.ascii_uppercase + string.digits
    generated_keys = []
    
    print(f"⚙️  Generando {amount} clave(s)...")

    for _ in range(amount):
        # Generate 8 random characters
        random_chars = ''.join(secrets.choice(alphabet) for _ in range(8))

        # Format the key with the desired pattern
        key = f"PDSMP-{random_chars[:4]}-{random_chars[4:]}"
        generated_keys.append(key)
    
    print("✅ ¡Claves generadas con éxito!")
    return generated_keys