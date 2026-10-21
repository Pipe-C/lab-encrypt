# Servidor Principal Flask que expone las vistas del Dashboard e Endpoints REST.
import os
import hashlib
from flask import Flask, render_template, request, jsonify
from scripts.rsa_cipher import RSACipherEngine
from scripts.rockyou_cracker import RockYouCracker
from scripts.argon2_kdf import Argon2Engine
from scripts.aes_fernet import AESFernetEngine
from scripts.generar_llaves import generar_par_llaves_rsa
import config

app = Flask(__name__)

# Carga inicial o verificación de existencia del diccionario RockYou
if not os.path.exists(config.ROCKYOU_PATH):
    os.makedirs(config.DATA_DIR, exist_ok=True)
    with open(config.ROCKYOU_PATH, "w", encoding="utf-8") as f:
        f.write("123456\npassword\n123456789\n12345\n12345678\nrockyou\niloveyou\nprincess\nfelipecano\nseguridad2026\nadmin123\n")

# Verificación de existencia y tamaño de llaves RSA al arrancar
if not os.path.exists(config.PUBLIC_KEY_PATH) or os.path.getsize(config.PUBLIC_KEY_PATH) == 0:
    generar_par_llaves_rsa(config.DEFAULT_RSA_KEY_SIZE, config.KEYS_DIR)

cracker = RockYouCracker(config.ROCKYOU_PATH)

@app.route("/")
def index():
    # Renderiza la interfaz gráfica principal
    with open(config.PUBLIC_KEY_PATH, "r") as f:
        pub_pem = f.read()
    with open(config.PRIVATE_KEY_PATH, "r") as f:
        priv_pem = f.read()
    return render_template("index.html", public_key_pem=pub_pem, private_key_pem=priv_pem)

@app.route("/api/rsa/generate-keys", methods=["POST"])
def api_generate_keys():
    # API REST para la generación dinámica de nuevos pares de llaves RSA
    data = request.json or {}
    bits = int(data.get("bits", 2048))
    priv_pem, pub_pem = generar_par_llaves_rsa(bits, config.KEYS_DIR)
    return jsonify({"success": True, "public_key": pub_pem, "private_key": priv_pem})

@app.route("/api/rsa/encrypt", methods=["POST"])
def api_rsa_encrypt():
    # API REST para cifrar un mensaje con RSA-OAEP SHA-256 compatible con CyberChef
    try:
        data = request.json or {}
        mensaje = data.get("mensaje", "")
        pub_pem = data.get("public_key", "")
        criptograma = RSACipherEngine.cifrar_mensaje(mensaje, pub_pem)
        return jsonify({"success": True, "criptograma": criptograma})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/rsa/decrypt", methods=["POST"])
def api_rsa_decrypt():
    # API REST para descifrar un mensaje RSA-OAEP SHA-256 usando la llave privada
    try:
        data = request.json or {}
        criptograma = data.get("criptograma", "")
        priv_pem = data.get("private_key", "")
        texto_plano = RSACipherEngine.descifrar_mensaje(criptograma, priv_pem)
        return jsonify({"success": True, "texto_plano": texto_plano})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/rockyou/crack", methods=["POST"])
def api_rockyou_crack():
    # API REST para realizar el ataque de diccionario SHA-256 sobre RockYou
    try:
        data = request.json or {}
        pwd = data.get("password", "").strip()
        hash_target = data.get("hash", "").strip()
        
        # Si se ingresó clave en texto plano, generar el hash SHA-256 exacto en Python
        if pwd:
            hash_target = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
            
        resultado = cracker.atacar_hash_sha256(hash_target)
        return jsonify({"success": True, "resultado": resultado})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/argon2/hash", methods=["POST"])
def api_argon2_hash():
    # API REST para hashing de contraseñas mediante derivación de clave con Argon2id
    try:
        data = request.json or {}
        pwd = data.get("password", "")
        resultado = Argon2Engine.generar_hash_argon2(pwd)
        return jsonify({"success": True, "resultado": resultado})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/aes/encrypt", methods=["POST"])
def api_aes_encrypt():
    # API REST para cifrado simétrico AES-128 / Fernet
    try:
        data = request.json or {}
        texto = data.get("texto", "")
        passphrase = data.get("passphrase", "")
        res = AESFernetEngine.cifrar(texto, passphrase)
        return jsonify({"success": True, "resultado": res})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == "__main__":
    print("[*] Iniciando Servidor Criptográfico en http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)