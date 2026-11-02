import socket
from datetime import datetime

OBJETIVO = "127.0.0.1"

PUERTOS = [
    5000,
    8000,
    8080,
    3306,
    5432
]


def escanear_puerto(host, puerto):
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_obj.settimeout(0.5)

    resultado = socket_obj.connect_ex((host, puerto))
    socket_obj.close()

    return resultado == 0


if __name__ == "__main__":
    print(f"Escaneo autorizado del equipo local: {OBJETIVO}")
    print(f"Fecha y hora: {datetime.now()}")
    print("-" * 50)

    for puerto in PUERTOS:
        if escanear_puerto(OBJETIVO, puerto):
            print(f"Puerto {puerto}: ABIERTO")
        else:
            print(f"Puerto {puerto}: CERRADO")

    print("-" * 50)
    print("Escaneo finalizado.")