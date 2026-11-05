"""Genera data/semilla.sql: usuarios iniciales y el usuario de sistema para el proceso de carga.

Se pega una sola vez en Supabase > SQL Editor después de supabase/schema.sql. No se sube a Git.
La contraseña del usuario de sistema se genera al azar y se guarda en el Administrador de credenciales.
Los analistas se agregan después en Administración, con el nombre exacto que trae la primera carga.
"""
import secrets
import sys
import unicodedata
from pathlib import Path

import keyring

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tiempos_dac.conexion import RAIZ, leer_config  # noqa: E402

CLAVE = "12345678"
FIJOS = [("Carlos Manuel Alvarez Gutierrez", "admin"), ("Katherine Gissell Mora Garcia", "jefe"),
         ("Marvin Efrain Orellana Zepeda", "gerente")]


def slug(s: str) -> str:
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower().strip()
    return ".".join(p for p in "".join(c if c.isalnum() else " " for c in s).split())


def q(s):
    return "null" if s is None else "'" + str(s).replace("'", "''") + "'"


def main():
    cfg = leer_config()["supabase"]
    clave_sis = secrets.token_urlsafe(24)
    keyring.set_password(cfg["servicio_credenciales"], cfg["usuario"], clave_sis)

    L = ["-- Carga inicial de Tiempos DAC El Salvador (pegar en Supabase > SQL Editor después de schema.sql)"]
    for nombre, rol in FIJOS:
        L.append(f"select dac_sv.dac_crear_usuario({q(slug(nombre))}, {q(nombre)}, '{rol}', '{CLAVE}');")
    L.append(f"select dac_sv.dac_crear_usuario('{cfg['usuario']}', 'Proceso de actualización', 'sistema', {q(clave_sis)});")
    destino = RAIZ / "data" / "semilla.sql"
    destino.parent.mkdir(exist_ok=True)
    destino.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Escrito {destino}. Contraseña de sistema guardada en el Administrador de credenciales.")


if __name__ == "__main__":
    main()
