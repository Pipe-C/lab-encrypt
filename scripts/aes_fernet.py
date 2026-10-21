# Módulo de cifrado simétrico AES-128 en modo CBC con autenticación HMAC usando Fernet.
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class AESFernetEngine:
    # Proporciona cifrado simétrico AES de 128 bits garantizando confidencialidad e integridad.

    @staticmethod
    def derivar_clave_desde_passphrase(passphrase: str, salt: bytes) -> bytes:
        # Deriva una clave Fernet de 32 bytes codificada en Base64 usando PBKDF2HMAC SHA-256.
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(passphrase.encode('utf-8')))

    @classmethod
    def cifrar(cls, texto_plano: str, passphrase: str):
        # Cifra un texto plano derivando la clave simétrica AES mediante passphrase y salt.
        salt = os.urandom(16)
        key = cls.derivar_clave_desde_passphrase(passphrase, salt)
        fernet = Fernet(key)
        criptograma = fernet.encrypt(texto_plano.encode('utf-8'))
        return {
            "criptograma": criptograma.decode('utf-8'),
            "salt_b64": base64.b64encode(salt).decode('utf-8')
        }

    @classmethod
    def descifrar(cls, criptograma: str, passphrase: str, salt_b64: str) -> str:
        # Descifra el criptograma Fernet verificando el HMAC y retornando el texto claro.
        salt = base64.b64decode(salt_b64)
        key = cls.derivar_clave_desde_passphrase(passphrase, salt)
        fernet = Fernet(key)
        texto_descifrado = fernet.decrypt(criptograma.encode('utf-8'))
        return texto_descifrado.decode('utf-8')