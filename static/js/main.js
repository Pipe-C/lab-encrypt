// Navegación por pestañas
function switchTab(tab) {
    const tabs = ['rsa', 'rockyou', 'argon2', 'aes'];
    tabs.forEach(t => {
        const sec = document.getElementById('tab-' + t);
        if (sec) sec.classList.add('hidden');
        
        const btn = document.getElementById('tab-' + t + '-btn');
        if (btn) {
            btn.classList.remove('bg-emerald-600', 'text-white');
            btn.classList.add('text-slate-400', 'hover:text-white', 'hover:bg-slate-800');
        }
    });

    const activeSec = document.getElementById('tab-' + tab);
    if (activeSec) activeSec.classList.remove('hidden');
    
    const activeBtn = document.getElementById('tab-' + tab + '-btn');
    if (activeBtn) {
        activeBtn.classList.remove('text-slate-400', 'hover:text-white', 'hover:bg-slate-800');
        activeBtn.classList.add('bg-emerald-600', 'text-white');
    }
}

// Alertas de Estado RSA
function mostrarEstadoRSA(mensaje, esError = false) {
    const alertBox = document.getElementById('rsa-status');
    if (!alertBox) return;
    alertBox.classList.remove('hidden', 'error', 'success');
    alertBox.classList.add(esError ? 'error' : 'success');
    alertBox.innerHTML = (esError ? '<i class="fa-solid fa-triangle-exclamation"></i> ' : '<i class="fa-solid fa-circle-check"></i> ') + mensaje;
}

// Cifrar RSA
async function ejecutarCifradoRSA() {
    const msg = document.getElementById('rsa-input-msg').value;
    const pub = document.getElementById('rsa-pub-key-area').value;

    if (!msg.trim() || !pub.trim()) {
        mostrarEstadoRSA("El mensaje y la llave pública no pueden estar vacíos.", true);
        return;
    }

    try {
        const res = await fetch('/api/rsa/encrypt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mensaje: msg, public_key: pub })
        });
        const data = await res.json();
        if (data.success) {
            document.getElementById('rsa-output-result').value = data.criptograma;
            mostrarEstadoRSA("Mensaje cifrado exitosamente con RSA-OAEP SHA-256.", false);
        } else {
            mostrarEstadoRSA("Error al cifrar: " + data.error, true);
        }
    } catch (e) {
        mostrarEstadoRSA("Error de red o servidor: " + e.message, true);
    }
}

// Descifrar RSA
async function ejecutarDescifradoRSA() {
    const crip = document.getElementById('rsa-output-result').value;
    const priv = document.getElementById('rsa-priv-key-area').value;

    if (!crip.trim() || !priv.trim()) {
        mostrarEstadoRSA("Debes tener un criptograma y la llave privada cargados.", true);
        return;
    }

    try {
        const res = await fetch('/api/rsa/decrypt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ criptograma: crip, private_key: priv })
        });
        const data = await res.json();
        if (data.success) {
            document.getElementById('rsa-output-result').value = data.texto_plano;
            mostrarEstadoRSA("Criptograma descifrado correctamente.", false);
        } else {
            mostrarEstadoRSA("Error al descifrar: " + data.error, true);
        }
    } catch (e) {
        mostrarEstadoRSA("Error de red o servidor: " + e.message, true);
    }
}

// Regenerar Par de Llaves
async function regenerarLlavesRSA() {
    try {
        const res = await fetch('/api/rsa/generate-keys', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ bits: 2048 })
        });
        const data = await res.json();
        if (data.success) {
            document.getElementById('rsa-pub-key-area').value = data.public_key;
            document.getElementById('rsa-priv-key-area').value = data.private_key;
            mostrarEstadoRSA("Nuevo par de llaves RSA de 2048-bits generado exitosamente.", false);
        }
    } catch (e) {
        mostrarEstadoRSA("Error al generar llaves: " + e.message, true);
    }
}

// Generar Hash SHA-256 en vivo en el navegador
async function actualizarHashDesdeClave() {
    const pwdInput = document.getElementById('rockyou-pass-input');
    if (!pwdInput) return;
    const pwd = pwdInput.value;
    if (!pwd) {
        document.getElementById('rockyou-hash-input').value = '';
        return;
    }
    const encoder = new TextEncoder();
    const data = encoder.encode(pwd);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    document.getElementById('rockyou-hash-input').value = hashHex;
}

// Ataque RockYou SHA-256
async function ejecutarAtaqueRockYou() {
    const pwd = document.getElementById('rockyou-pass-input').value;
    const hash = document.getElementById('rockyou-hash-input').value;
    
    document.getElementById('metric-pass').innerText = "Procesando...";
    document.getElementById('metric-lines').innerText = "Leyendo...";
    document.getElementById('metric-wall-time').innerText = "...";
    document.getElementById('metric-cpu-time').innerText = "...";
    document.getElementById('metric-speed').innerText = "...";

    try {
        const res = await fetch('/api/rockyou/crack', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: pwd, hash: hash })
        });
        const data = await res.json();
        if (data.success) {
            const r = data.resultado;
            document.getElementById('metric-pass').innerText = r.encontrada ? `¡Encontrada! (${r.contrasena})` : "No encontrada";
            document.getElementById('metric-lines').innerText = (r.intentos_totales || 0).toLocaleString() + " líneas";
            document.getElementById('metric-wall-time').innerText = r.tiempo_reloj_segundos + " s";
            document.getElementById('metric-cpu-time').innerText = r.tiempo_cpu_segundos + " s";
            document.getElementById('metric-speed').innerText = (r.velocidad_hashes_por_seg_cpu || 0).toLocaleString() + " hash/s";
        } else {
            alert("Error en el servidor: " + data.error);
        }
    } catch (e) {
        alert("Error en la ejecución: " + e.message);
    }
}

// Argon2id
async function ejecutarArgon2() {
    const pwd = document.getElementById('argon2-pwd').value;
    try {
        const res = await fetch('/api/argon2/hash', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: pwd })
        });
        const data = await res.json();
        if (data.success) {
            document.getElementById('argon2-result').value = JSON.stringify(data.resultado, null, 2);
        }
    } catch (e) {
        alert("Error en Argon2id: " + e.message);
    }
}

// AES-128 Fernet
async function ejecutarAES() {
    const txt = document.getElementById('aes-text').value;
    const pass = document.getElementById('aes-pass').value;

    try {
        const res = await fetch('/api/aes/encrypt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ texto: txt, passphrase: pass })
        });
        const data = await res.json();
        if (data.success) {
            document.getElementById('aes-result').value = JSON.stringify(data.resultado, null, 2);
        }
    } catch (e) {
        alert("Error en AES: " + e.message);
    }
}

// Inicializar Hash al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('rockyou-pass-input')) {
        actualizarHashDesdeClave();
    }
});