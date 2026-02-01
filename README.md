# Bot de Discord en Python

Este proyecto contiene un bot básico de Discord desarrollado en Python usando la librería `discord.py`.

## Requisitos
- Python 3.8 o superior
- Un token de bot de Discord

## Instalación

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Crea un archivo `.env` en la raíz de este proyecto y agrega tu token:
   ```
   DISCORD_TOKEN=tu_token_aqui
   ```
3. Ejecuta el bot:
   ```bash
   python bot.py
   ```

## Estructura
- `bot.py`: Archivo principal del bot.
- `cogs/`: Directorio con cogs para organizar comandos.
- `requirements.txt`: Dependencias del proyecto.
- `Dockerfile` y `docker-compose.yml`: Archivos para despliegue con Docker.
- `.env`: Variables de entorno (no se incluye por seguridad).