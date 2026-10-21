# Configuración global de parámetros para el laboratorio criptográfico.
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.join(BASE_DIR, "keys")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Apuntando al diccionario completo rockyou.txt
ROCKYOU_PATH = os.path.join(DATA_DIR, "rockyou.txt")
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, "public_key.pem")
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "private_key.pem")

DEFAULT_RSA_KEY_SIZE = 2048
DEFAULT_HASH_ALGORITHM = "SHA-256"