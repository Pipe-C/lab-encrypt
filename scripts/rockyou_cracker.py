import hashlib
import time

class RockYouCracker:
    def __init__(self, diccionario_path: str):
        self.diccionario_path = diccionario_path

    def atacar_hash_sha256(self, hash_objetivo: str):
        hash_objetivo = hash_objetivo.strip().lower()
        intentos = 0
        contrasena_encontrada = None
        
        inicio_reloj = time.time()
        inicio_cpu = time.process_time()

        # Lectura en modo binario 'rb' para máximo rendimiento y compatibilidad absoluta
        try:
            with open(self.diccionario_path, "rb") as file:
                for line in file:
                    intentos += 1
                    # Eliminar saltos de línea binarios (\r, \n)
                    palabra_bytes = line.rstrip(b"\r\n")
                    
                    # Generar hash SHA-256 directo sobre los bytes de la línea
                    hash_cand = hashlib.sha256(palabra_bytes).hexdigest().lower()
                    
                    if hash_cand == hash_objetivo:
                        contrasena_encontrada = palabra_bytes.decode('latin-1', errors='replace')
                        break
        except Exception as e:
            print(f"[!] Error leyendo diccionario: {e}")

        fin_reloj = time.time()
        fin_cpu = time.process_time()

        tiempo_reloj = fin_reloj - inicio_reloj
        tiempo_cpu = fin_cpu - inicio_cpu
        velocidad_promedio_cpu = intentos / tiempo_cpu if tiempo_cpu > 0 else 0

        return {
            "encontrada": contrasena_encontrada is not None,
            "contrasena": contrasena_encontrada if contrasena_encontrada else "No encontrada en RockYou",
            "intentos_totales": intentos,
            "tiempo_reloj_segundos": round(tiempo_reloj, 6),
            "tiempo_cpu_segundos": round(tiempo_cpu, 6),
            "velocidad_hashes_por_seg_cpu": round(velocidad_promedio_cpu, 2)
        }