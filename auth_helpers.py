from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """
    Hashes a password using Werkzeug's hash function.
    """
    return generate_password_hash(password)

def verify_password(stored_password, provided_password):
    """
    Verifies a provided password against a stored hashed password.
    """
    return check_password_hash(stored_password, provided_password)
