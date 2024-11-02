
# Visor de Usuarios

Una aplicación Flask que permite monitorear usuarios en un servidor Ubuntu, mostrando su estado (ON/OFF) y registrando un historial de conexiones. La aplicación presenta una interfaz web para visualizar la información de conexión en tiempo real y un historial detallado.

## Características

- Muestra el estado de conexión (ON/OFF) de usuarios específicos.
- Resalta en verde los usuarios que se hayan conectado alguna vez.
- Permite consultar el historial de conexiones de cada usuario a través de un ícono de calendario.
- Interfaz amigable con tres columnas (una para cada grupo de usuarios).
- Se ejecuta en el puerto `9876` del servidor.

## Requisitos

- **Python 3** y **pip**.
- **Flask**: Un micro-framework para aplicaciones web en Python.
- **Git** (opcional, para clonar el repositorio).

## Instalación

### 1. Clonar el repositorio

Clona el repositorio en tu servidor Ubuntu:

```bash
git clone https://github.com/tu_usuario/NombreDelRepositorio.git
cd NombreDelRepositorio
```

### 2. Instalar dependencias

Instala Flask usando pip:

```bash
pip install flask
```

### 3. Crear archivo de usuarios

Crea un archivo `usuarios.txt` en el directorio raíz del proyecto. En este archivo, agrega los nombres de los usuarios a monitorear, uno por línea:

```plaintext
GRUPO_A_001
GRUPO_A_002
...
GRUPO_B_001
GRUPO_B_002
...
GRUPO_C_001
GRUPO_C_002
```

### 4. Configuración del servicio con `systemd`

Para que la aplicación se ejecute automáticamente y esté disponible tras reinicios, configuraremos un servicio `systemd`.

1. Crea un archivo de servicio en `/etc/systemd/system/visor_usuarios.service`:

   ```bash
   sudo nano /etc/systemd/system/visor_usuarios.service
   ```

2. Añade la siguiente configuración al archivo:

   ```ini
   [Unit]
   Description=Visor de Usuarios Flask Application
   After=network.target

   [Service]
   User=ubuntu  # Cambia 'ubuntu' por el usuario que ejecutará el servicio
   WorkingDirectory=/ruta/a/tu/proyecto  # Ruta a la carpeta donde está el proyecto
   ExecStart=/usr/bin/python3 /ruta/a/tu/proyecto/app.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Asegúrate de reemplazar `/ruta/a/tu/proyecto` con la ruta real donde clonaste el repositorio y de verificar la ruta de `python3` si es necesario.

3. Habilitar e iniciar el servicio:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable visor_usuarios
   sudo systemctl start visor_usuarios
   ```

4. Verificar el estado del servicio:

   ```bash
   sudo systemctl status visor_usuarios
   ```

La aplicación ahora se ejecutará automáticamente en el puerto `9876` y estará disponible en `http://<tu_ip_o_dominio>:9876`.

## Uso

### Acceder a la aplicación

Abre un navegador y ve a:

```
http://<tu_ip_o_dominio>:9876
```

### Visualizar usuarios

En la interfaz verás:
- **Estado de conexión**: Muestra "ON" si el usuario está conectado actualmente y "OFF" si no lo está.
- **Historial de conexiones**: Si el usuario se ha conectado alguna vez, verás un ícono 📅 en la columna "Últimas Conexiones". Haz clic en el ícono para ver el historial de conexiones del usuario en un modal.

### Actualización de usuarios

Para agregar o eliminar usuarios de monitoreo, edita el archivo `usuarios.txt` y reinicia el servicio:

```bash
sudo systemctl restart visor_usuarios
```

## Tecnologías

- **Python 3**
- **Flask**
- **Systemd** (para manejo del servicio en Ubuntu)

## Contribuciones

Las contribuciones son bienvenidas. Para contribuir, realiza un fork del proyecto, crea una rama con tu contribución y envía un pull request.

---

¡Gracias por utilizar el Visor de Usuarios! Esperamos que esta herramienta facilite la gestión de conexiones en tu servidor.
