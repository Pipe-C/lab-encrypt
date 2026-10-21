# Script profesional para la generación e inspección de pares de llaves RSA en formato PEM.
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generar_par_llaves_rsa(tamano_bits=2048, ruta_salida="../keys"):
    # Genera un par de llaves RSA (Pública/Privada) y las exporta en archivos PEM seguros.
    os.makedirs(ruta_salida, exist_ok=True)
    
    # Generación de la clave privada RSA usando exponente público estándar 65537
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=tamano_bits
    )
    
    # Serialización de la llave privada en formato PKCS#8 PEM sin contraseña
    pem_privado = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serialización de la llave pública en formato SubjectPublicKeyInfo (X.509 PEM)
    public_key = private_key.public_key()
    pem_publico = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    ruta_privada = os.path.join(ruta_salida, "private_key.pem")
    ruta_publica = os.path.join(ruta_salida, "public_key.pem")
    
    with open(ruta_privada, "wb") as f:
        f.write(pem_privado)
        
    with open(ruta_publica, "wb") as f:
        f.write(pem_publico)
        
    print(f"[+] Par de llaves RSA de {tamano_bits} bits generado exitosamente en '{ruta_salida}'")
    return pem_privado.decode('utf-8'), pem_publico.decode('utf-8')

if __name__ == "__main__":
    generar_par_llaves_rsa()