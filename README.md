# YouTube Shorts Downloader

Este proyecto permite descargar todos los Shorts de YouTube desde un canal específico utilizando Selenium y yt-dlp. La interfaz gráfica está construida con Tkinter.

## Requisitos

Antes de ejecutar el script, asegúrate de tener instalado lo siguiente:

- **Python 3.7 o superior**
- **Dependencias de Python**: Puedes instalar las dependencias necesarias usando el archivo `requirements.txt`.

Puedes instalar todas las dependencias ejecutando el siguiente comando en tu terminal:

```bash
pip install --user -r requirements.txt
```

## Instalación del WebDriver

Para que Selenium funcione, necesitarás instalar un WebDriver compatible con tu navegador. Este proyecto utiliza Chrome, así que necesitarás ChromeDriver instalado y en tu PATH del sistema. Asegúrate de que la versión del ChromeDriver coincida con la versión de tu navegador Chrome.

## Uso

1. Clona o descarga este repositorio en tu máquina local.
2. Navega al directorio del proyecto en tu terminal.
3. Ejecuta el script:

```bash
python main.py
```

4. Se abrirá una ventana de la interfaz gráfica donde podrás ingresar la URL del canal de YouTube y seleccionar la carpeta de destino para los videos descargados. 
5. Haz clic en "Descargar Shorts" para iniciar el proceso.

## Vista previa

Video demostrativo sobre cómo usar el downloader:

!

## Contribuciones

Si deseas contribuir a este proyecto, siéntete libre de abrir un issue o enviar un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.