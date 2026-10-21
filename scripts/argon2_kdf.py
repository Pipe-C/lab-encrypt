# Módulo de derivación y hashing de contraseñas de alta seguridad utilizando Argon2id.
import os
import base64
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

class Argon2Engine:
    # Implementa derivación de claves resistentes a ataques mediante GPU/ASIC con Argon2id.

    @staticmethod
    def generar_hash_argon2(password: str, salt: bytes = None, memory_cost=65536, time_cost=3, parallelism=4):
        # Genera un hash derivado con Argon2id usando parámetros configurables de costo.
        if salt is None:
            salt = os.urandom(16)
            
        kdf = Argon2id(
            salt=salt,
            length=32,
            iterations=time_cost,
            lanes=parallelism,
            memory_cost=memory_cost
        )
        
        key = kdf.derive(password.encode('utf-8'))
        return {
            "hash_b64": base64.b64encode(key).decode('utf-8'),
            "salt_b64": base64.b64encode(salt).decode('utf-8'),
            "memory_cost_kb": memory_cost,
            "time_cost": time_cost,
            "parallelism": parallelism
        }

    @staticmethod
    def verificar_hash_argon2(password: str, salt_b64: str, hash_esperado_b64: str, memory_cost=65536, time_cost=3, parallelism=4) -> bool:
        # Verifica la validez de una contraseña contra un hash y salt Argon2id previos.
        salt = base64.b64decode(salt_b64)
        kdf = Argon2id(
            salt=salt,
            length=32,
            iterations=time_cost,
            lanes=parallelism,
            memory_cost=memory_cost
        )
        try:
            kdf.verify(password.encode('utf-8'), base64.b64decode(hash_esperado_b64))
            return True
        except Exception:
            return False