# Cin3.ar-DL

Script para descargar de Cine AR lo estoy probando pero parece funcionar bien, tanto para películas, como series, todos los episodios que estén.

Necesita que tengas "N_m3u8DL" (https://github.com/nilaoda/N_m3u8DL-CLI/releases/) agregado en el path de windows (neoguias.com/agregar-directorio-path-windows/)

Importante que al descargar "N_m3u8DL" llega con el número de la version en el nombre "N_m3u8DL-CLI_v3.0.2.exe" y hay que renombrar a "N_m3u8DL.exe"  específicamente para que el script funcione (o modificar las partes del script para que haga referencia al nombre correcto del programa igual a como esta guardado).

Para funcionar debes tener python instalado y ejecutas:

# python cinedl.py

La primera vez de uso te logueas con correo y contraseña, y luego queda guardado el token en "C:\Users\USER\" en un archivo llamado "tkn.txt"

y luego de loguearte preguntará por la url, ejemplo: https://play.cine.ar/INCAA/produccion/8054

Entonces reconocerá si es película y serie, autonombrará los archivos con la infrmación en línea de episodio, titulo, año, etc.

Finalmente los archivos se descargarán a "C:\Downloads"
