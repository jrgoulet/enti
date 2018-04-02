import uuid

def generate_uuid():
    """Generates a uniquely-identifiable ID"""
    return str(uuid.uuid4()).upper()