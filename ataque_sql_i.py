import requests

URL = "http://127.0.0.1:5000/"


def probar_login(usuario, password, descripcion):
    try:
        respuesta = requests.post(
            URL,
            data={
                "usuario": usuario,
                "password": password
            },
            timeout=5
        )

        print("=" * 60)
        print(f"Prueba: {descripcion}")
        print(f"Estado HTTP: {respuesta.status_code}")

        if "Acceso concedido" in respuesta.text:
            print("Resultado: ACCESO CONCEDIDO")
        elif "Credenciales incorrectas" in respuesta.text:
            print("Resultado: ACCESO RECHAZADO")
        else:
            print("Resultado: RESPUESTA NO IDENTIFICADA")

    except requests.RequestException as error:
        print(f"No se pudo conectar con la aplicación: {error}")


if __name__ == "__main__":
    probar_login(
        "ana",
        "Clave123",
        "Credenciales válidas"
    )

    probar_login(
        "ana",
        "incorrecta",
        "Credenciales inválidas"
    )

    probar_login(
        "' OR '1'='1' -- -",
        "cualquiera",
        "Prueba controlada de SQL Injection"
    )