# 🛡️ Laboratorio Criptográfico Avanzado: RSA, RockYou SHA-256, Argon2id y AES-128

**Autor:** Felipe Cano  
**Asignatura:** Cifrado e Integridad de la Información  
**Tecnologías:** Python 3.10, Flask, Cryptography, Tailwind CSS y CyberChef

---

## 📌 Descripción general

Este proyecto implementa una plataforma web interactiva y modular de ciberseguridad criptográfica, orientada a la experimentación y evaluación de algoritmos de cifrado asimétrico, cifrado simétrico y funciones hash.

### Funcionalidades principales

1. **RSA-OAEP con SHA-256:** interoperabilidad criptográfica con CyberChef.
2. **Ataque de diccionario SHA-256:** evaluación de contraseñas candidatas mediante RockYou.txt y medición de tiempos de ejecución.
3. **Hashing con Argon2id:** derivación de hashes de contraseñas con resistencia frente a ataques de fuerza bruta.
4. **Cifrado simétrico:** uso de Fernet y derivación de claves mediante PBKDF2HMAC.
5. **Interfaz web:** integración de herramientas criptográficas con Flask y tecnologías de frontend.

---

## 🚀 Instalación y ejecución

### 1. Descomprimir el proyecto

Si recibiste el proyecto como archivo ZIP:

```bash
unzip laboratorio_cifrado_rsa.zip
cd laboratorio_cifrado_rsa
```

### 2. Crear un entorno virtual

```bash
python -m venv venv
```

Activar en Linux o macOS:

```bash
source venv/bin/activate
```

Activar en Windows CMD:

```cmd
venv\Scripts\activate.bat
```

Activar en Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Generar las claves RSA

Si el proyecto incluye el script correspondiente:

```bash
python scripts/generar_llaves.py
```

Este paso es opcional si ya dispones de un par de claves válido y la aplicación permite utilizarlo.

**Importante:** nunca publiques la clave privada en un repositorio público.

### 5. Iniciar el servidor

```bash
python app.py
```

Abre la aplicación en el navegador:

http://localhost:5000

---

## 🔗 Integración con CyberChef

Para verificar la interoperabilidad de RSA-OAEP con SHA-256, utiliza [CyberChef](https://cyberchef.io/).

### Procedimiento

1. Inicia la aplicación web.
2. Accede a la sección RSA.
3. Copia la clave pública en formato PEM.
4. Abre CyberChef y configura la operación RSA Encrypt.
5. Selecciona OAEP como esquema de relleno y SHA-256 como función hash.
6. Introduce el mensaje que deseas cifrar.
7. Copia el criptograma generado y verifica si la aplicación puede descifrarlo con la clave privada correspondiente.

También puedes cifrar desde la aplicación y comprobar el resultado con una configuración compatible en CyberChef.

### Consideraciones

- La clave pública y la privada deben pertenecer al mismo par RSA.
- Los parámetros OAEP y las funciones hash deben coincidir en ambos sistemas, incluida la configuración de MGF1 cuando corresponda.
- RSA-OAEP limita el tamaño máximo del mensaje según el tamaño de la clave y la función hash.
- Los criptogramas pueden representarse en Base64 para facilitar su intercambio.
- RSA-OAEP utiliza aleatoriedad, por lo que cifrar el mismo mensaje dos veces no necesariamente produce el mismo criptograma.

La interoperabilidad debe verificarse mediante el descifrado correcto del mensaje original, no comparando directamente los criptogramas.

---

## 🔐 Funcionalidades criptográficas

### 1. RSA-OAEP con SHA-256

RSA utiliza un par de claves:

- **Clave pública:** permite cifrar mensajes.
- **Clave privada:** permite descifrarlos.

OAEP (*Optimal Asymmetric Encryption Padding*) es un esquema de relleno diseñado para mejorar la seguridad del cifrado RSA.

En este proyecto, SHA-256 se utiliza como función hash de OAEP, de acuerdo con los parámetros configurados en la aplicación.

### 2. Ataque de diccionario con RockYou.txt

Esta funcionalidad permite evaluar contraseñas candidatas mediante la comparación de hashes SHA-256.

El procedimiento consiste en:

1. Leer las contraseñas candidatas del diccionario.
2. Calcular el hash SHA-256 de cada candidato.
3. Comparar el resultado con el hash objetivo.
4. Registrar el tiempo de ejecución y calcular el rendimiento cuando corresponda.

El rendimiento se calcula mediante:

[
\text{Hashes por segundo} =
\frac{\text{Número de intentos}}{\text{Tiempo transcurrido}}
]

Se utilizan dos métricas:

- **Wall-clock time:** tiempo real transcurrido durante la ejecución.
- **CPU process time:** tiempo de CPU consumido por el proceso, medido con `time.process_time()`.

Para medir el tiempo real transcurrido también puede utilizarse `time.perf_counter()`.

**Nota de seguridad:** SHA-256 es una función hash de propósito general y no está diseñada específicamente para almacenar contraseñas. Esta práctica es educativa y no constituye una recomendación para almacenar credenciales.

### 3. Hashing de contraseñas con Argon2id

Argon2id es un algoritmo de hashing de contraseñas que permite configurar el consumo de memoria y el coste computacional para dificultar los ataques de fuerza bruta.

Sus características incluyen:

- Uso configurable de memoria.
- Coste computacional ajustable.
- Mayor dificultad para ejecutar grandes cantidades de intentos en paralelo.
- Uso de sales únicas para cada contraseña.

La seguridad depende de la configuración de los parámetros y de una gestión adecuada de los hashes.

### 4. Cifrado simétrico con Fernet y PBKDF2HMAC

Fernet proporciona cifrado simétrico autenticado para proteger la confidencialidad e integridad de los datos.

PBKDF2HMAC permite derivar una clave a partir de una contraseña utilizando una función hash, una sal y un número configurable de iteraciones.

Buenas prácticas:

- Utilizar una sal aleatoria y única.
- Conservar los parámetros necesarios para derivar nuevamente la clave.
- No almacenar contraseñas en texto plano.
- Proteger las claves y los datos sensibles.
- Configurar los parámetros de acuerdo con los requisitos de seguridad.

**Aclaración técnica:** Fernet utiliza una clave de 256 bits dividida internamente para cifrado y autenticación; no equivale directamente a AES-128. Si el proyecto implementa AES-128 de forma independiente, debe documentarse como una funcionalidad separada.

---

## 🔒 Anexo de seguridad

### Relleno RSA

RSA-OAEP se utiliza en lugar del esquema de cifrado RSA PKCS#1 v1.5 por su diseño orientado a mejorar la robustez frente a ataques criptográficos.

La seguridad también depende de la configuración correcta de las funciones hash, la protección de la clave privada y el manejo adecuado de errores.

### Evaluación de contraseñas

Las pruebas con RockYou.txt deben ejecutarse exclusivamente en entornos controlados y con fines educativos o de auditoría autorizada.

El rendimiento depende del hardware, la implementación, el entorno de ejecución y las condiciones del sistema.

### Gestión de claves y datos sensibles

- No publiques claves privadas ni secretos en GitHub.
- Evita utilizar contraseñas reales en pruebas.
- Utiliza claves de prueba para las demostraciones.
- No publiques diccionarios de contraseñas ni archivos sensibles innecesarios.
- Mantén actualizadas las dependencias.
- Utiliza algoritmos y parámetros apropiados para cada finalidad.

---

## 📦 Dependencias

El archivo `requirements.txt` debe incluir las dependencias necesarias para ejecutar el proyecto.

Contenido inicial:

```text
flask>=3.0.0
cryptography>=41.0.0
python-docx>=1.1.0
```

- **Flask:** framework para desarrollar la aplicación web.
- **Cryptography:** biblioteca para operaciones criptográficas, incluidas RSA y Fernet.
- **python-docx:** biblioteca para crear y modificar documentos de Word desde Python.

Si se utiliza Argon2id mediante una biblioteca adicional, como `argon2-cffi`, debe añadirse a las dependencias. También deben incluirse las demás bibliotecas que realmente utilice el proyecto.

---

## 📁 Estructura del proyecto

La siguiente estructura es orientativa. Debe ajustarse a los archivos reales del repositorio.

```text
laboratorio_cifrado_rsa/
├── app.py
├── requirements.txt
├── scripts/
│   └── generar_llaves.py
├── templates/
├── static/
├── README.md
└── venv/
```

- `app.py`: punto de entrada de la aplicación Flask.
- `requirements.txt`: dependencias de Python.
- `scripts/generar_llaves.py`: script para generar las claves RSA.
- `templates/`: plantillas HTML.
- `static/`: archivos estáticos, como CSS, JavaScript e imágenes.
- `README.md`: documentación del proyecto.
- `venv/`: entorno virtual local, que no debe incluirse en el repositorio.

Se recomienda agregar `venv/` a `.gitignore`.

---

## 👨‍💻 Autor

**Felipe Cano**

Proyecto académico desarrollado para la asignatura **Cifrado e Integridad de la Información**, con fines educativos y de experimentación en criptografía aplicada.

---

## ⚖️ Aviso de uso

Este proyecto tiene fines educativos y de investigación en ciberseguridad. Utiliza las herramientas de análisis de contraseñas y evaluación criptográfica únicamente con autorización y en entornos controlados.
