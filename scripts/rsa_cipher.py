# Módulo de Cifrado y Descifrado RSA-OAEP con SHA-256 idéntico a la receta de CyberChef.
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

class RSACipherEngine:
    # Motor criptográfico RSA optimizado para interoperabilidad con CyberChef usando OAEP y SHA-256.

    @staticmethod
    def cargar_llave_publica_pem(pem_str: str):
        # Carga y retorna un objeto de llave pública RSA a partir de una cadena PEM.
        return serialization.load_pem_public_key(pem_str.encode('utf-8'))

    @staticmethod
    def cargar_llave_privada_pem(pem_str: str):
        # Carga y retorna un objeto de llave privada RSA a partir de una cadena PEM.
        return serialization.load_pem_private_key(pem_str.encode('utf-8'), password=None)

    @classmethod
    def cifrar_mensaje(cls, mensaje_plano: str, pem_publico: str) -> str:
        # Cifra un mensaje plano usando la llave pública RSA con relleno OAEP y función hash SHA-256.
        llave_pub = cls.cargar_llave_publica_pem(pem_publico)
        bytes_cifrados = llave_pub.encrypt(
            mensaje_plano.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        # Codifica los bytes cifrados en Base64 para facilitar su transmisión e inspección
        return base64.b64encode(bytes_cifrados).decode('utf-8')

    @classmethod
    def descifrar_mensaje(cls, mensaje_cifrado_b64: str, pem_privado: str) -> str:
        # Descifra un criptograma Base64 usando la llave privada RSA con relleno OAEP y SHA-256.
        llave_priv = cls.cargar_llave_privada_pem(pem_privado)
        bytes_cifrados = base64.b64decode(mensaje_cifrado_b64)
        bytes_descifrados = llave_priv.decrypt(
            bytes_cifrados,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        # Retorna el mensaje original en texto claro formateado en UTF-8
        return bytes_descifrados.decode('utf-8')