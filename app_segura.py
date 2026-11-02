from flask import Flask, request, render_template_string
import sqlite3
from pathlib import Path

app = Flask(__name__)

DB = Path(__file__).with_name("usuarios.db")

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Laboratorio SQL Injection - Aplicación segura</title>
</head>
<body>
    <h1>Inicio de sesión seguro</h1>

    {% if mensaje %}
        <p><strong>{{ mensaje }}</strong></p>
    {% endif %}

    <form method="POST">
        <label>Usuario:</label><br>
        <input type="text" name="usuario" required><br><br>

        <label>Contraseña:</label><br>
        <input type="password" name="password" required><br><br>

        <button type="submit">Ingresar</button>
    </form>
</body>
</html>
"""


def conectar():
    conexion = sqlite3.connect(DB)
    conexion.row_factory = sqlite3.Row
    return conexion


def inicializar_bd():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    """)

    cantidad = conexion.execute(
        "SELECT COUNT(*) AS total FROM usuarios"
    ).fetchone()["total"]

    if cantidad == 0:
        conexion.executemany("""
            INSERT INTO usuarios (usuario, password, rol)
            VALUES (?, ?, ?)
        """, [
            ("ana", "Clave123", "estudiante"),
            ("admin", "Admin123", "administrador")
        ])

    conexion.commit()
    conexion.close()


@app.route("/", methods=["GET", "POST"])
def login():
    mensaje = ""

    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        password = request.form.get("password", "")

        # Consulta parametrizada segura
        consulta = """
            SELECT id, usuario, rol
            FROM usuarios
            WHERE usuario = ?
            AND password = ?
        """

        print("\n[LABORATORIO] Consulta parametrizada:")
        print(consulta)
        print("Valores recibidos:", usuario, password)

        conexion = conectar()

        try:
            resultado = conexion.execute(
                consulta,
                (usuario, password)
            ).fetchone()

            if resultado:
                mensaje = (
                    f"Acceso concedido. Usuario: {resultado['usuario']} "
                    f"| Rol: {resultado['rol']}"
                )
            else:
                mensaje = "Credenciales incorrectas."

        except sqlite3.Error as error:
            mensaje = f"Error SQL controlado: {error}"

        finally:
            conexion.close()

    return render_template_string(HTML, mensaje=mensaje)


if __name__ == "__main__":
    inicializar_bd()
    app.run(host="127.0.0.1", port=5000, debug=False)