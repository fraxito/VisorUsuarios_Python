from flask import Flask, render_template_string
import subprocess
import json
import datetime

app = Flask(__name__)

HISTORIAL_ARCHIVO = "conexiones.json"

def obtener_usuarios_conectados():
    resultado = subprocess.run(['who'], stdout=subprocess.PIPE, text=True)
    usuarios_conectados = {}
    for linea in resultado.stdout.splitlines():
        partes = linea.split()
        usuario = partes[0]
        usuarios_conectados[usuario] = {
            'terminal': partes[1],
            'fecha': partes[2],
            'hora': partes[3],
            'origen': partes[4] if len(partes) > 4 else 'local'
        }
    return usuarios_conectados

def obtener_lista_usuarios():
    with open("usuarios.txt", "r") as f:
        usuarios = [line.strip() for line in f if line.strip()]
    return usuarios

def cargar_historial():
    try:
        with open(HISTORIAL_ARCHIVO, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def actualizar_historial(usuarios_conectados):
    historial = cargar_historial()
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for usuario, datos in usuarios_conectados.items():
        if usuario not in historial:
            historial[usuario] = []
        if not any(conexion["fecha_hora"] == fecha_actual for conexion in historial[usuario]):
            historial[usuario].append({
                "fecha_hora": fecha_actual,
                "terminal": datos["terminal"],
                "origen": datos["origen"]
            })

    with open(HISTORIAL_ARCHIVO, "w") as f:
        json.dump(historial, f)

@app.route('/')
def index():
    lista_usuarios = obtener_lista_usuarios()
    usuarios_conectados = obtener_usuarios_conectados()
    
    # Actualizar el historial con los usuarios actualmente conectados
    actualizar_historial(usuarios_conectados)
    
    # Cargar historial actualizado
    historial = cargar_historial()

    # Dividir los usuarios en grupos A, B y C
    grupo_a = [u for u in lista_usuarios if u.startswith("GRUPO_A")]
    grupo_b = [u for u in lista_usuarios if u.startswith("GRUPO_B")]
    grupo_c = [u for u in lista_usuarios if u.startswith("GRUPO_C")]

    html = """
    <html>
    <head>
        <title>Visor de Usuarios</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            h1 {
                text-align: center;
            }
            .container {
                display: flex;
                justify-content: space-around;
            }
            .column {
                width: 30%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }
            .column h2 {
                text-align: center;
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 8px;
                margin-top: 0;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }
            th {
                background-color: #f7f7f7;
            }
            .connected {
                background-color: #d4edda;
                color: #155724;
            }
            .disconnected {
                background-color: #f8d7da;
                color: #721c24;
            }
            .history {
                font-size: 0.9em;
                color: #555;
            }
            .history-icon {
                cursor: pointer;
                font-size: 1.2em;
                color: #007bff;
            }
            .has-history {
                background-color: #c3e6cb;
            }
        </style>
        <script>
            function mostrarHistorial(usuario, historial) {
                let mensaje = 'Historial de conexiones para ' + usuario + ':\\n';
                historial = JSON.parse(historial);
                for (let conexion of historial) {
                    mensaje += 'Fecha y Hora: ' + conexion.fecha_hora + ', Origen: ' + conexion.origen + '\\n';
                }
                alert(mensaje);
            }
        </script>
    </head>
    <body>
        <h1>Visor de Usuarios</h1>
        <div class="container">
            <div class="column">
                <h2>Grupo A</h2>
                <table>
                    <tr><th>Usuario</th><th>Estado</th><th>Últimas Conexiones</th></tr>
                    {% for usuario in grupo_a %}
                        <tr class="{{ 'connected' if usuario in usuarios_conectados else 'disconnected' }} {{ 'has-history' if historial.get(usuario) else '' }}">
                            <td>{{ usuario }}</td>
                            <td>{{ 'ON' if usuario in usuarios_conectados else 'OFF' }}</td>
                            <td>
                                {% if historial.get(usuario) %}
                                    <span class="history-icon" onclick='mostrarHistorial("{{ usuario }}", `{{ historial.get(usuario, []) | tojson | safe }}`)'>📅</span>
                                {% endif %}
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            </div>
            <div class="column">
                <h2>Grupo B</h2>
                <table>
                    <tr><th>Usuario</th><th>Estado</th><th>Últimas Conexiones</th></tr>
                    {% for usuario in grupo_b %}
                        <tr class="{{ 'connected' if usuario in usuarios_conectados else 'disconnected' }} {{ 'has-history' if historial.get(usuario) else '' }}">
                            <td>{{ usuario }}</td>
                            <td>{{ 'ON' if usuario in usuarios_conectados else 'OFF' }}</td>
                            <td>
                                {% if historial.get(usuario) %}
                                    <span class="history-icon" onclick='mostrarHistorial("{{ usuario }}", `{{ historial.get(usuario, []) | tojson | safe }}`)'>📅</span>
                                {% endif %}
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            </div>
            <div class="column">
                <h2>Grupo C</h2>
                <table>
                    <tr><th>Usuario</th><th>Estado</th><th>Últimas Conexiones</th></tr>
                    {% for usuario in grupo_c %}
                        <tr class="{{ 'connected' if usuario in usuarios_conectados else 'disconnected' }} {{ 'has-history' if historial.get(usuario) else '' }}">
                            <td>{{ usuario }}</td>
                            <td>{{ 'ON' if usuario in usuarios_conectados else 'OFF' }}</td>
                            <td>
                                {% if historial.get(usuario) %}
                                    <span class="history-icon" onclick='mostrarHistorial("{{ usuario }}", `{{ historial.get(usuario, []) | tojson | safe }}`)'>📅</span>
                                {% endif %}
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, grupo_a=grupo_a, grupo_b=grupo_b, grupo_c=grupo_c, usuarios_conectados=usuarios_conectados, historial=historial)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876)
