# README - Subida de Base de Datos al Servidor

Este documento describe el proceso utilizado para subir una base de datos local con **138,123** registros a un servidor remoto utilizando comandos de **MySQL**.

## Pasos Seguidos

### 1. **Exportación de la Base de Datos Local**
Para exportar la base de datos local, se utilizó el comando `mysqldump`, que permite generar un archivo SQL con la estructura y los datos de la base de datos.

```bash
mysqldump -u usuario_local -p nombre_base_datos > backup.sql
```

Este comando:
- `-u usuario_local`: Especifica el usuario de MySQL en la máquina local.
- `-p`: Solicita la contraseña antes de proceder con la exportación.
- `nombre_base_datos`: Es el nombre de la base de datos que se exportará.
- `> backup.sql`: Redirige la salida del comando a un archivo SQL llamado `backup.sql`.

### 2. **Transferencia del Archivo al Servidor**
Una vez generado el archivo `backup.sql`, se transfirió al servidor remoto usando `scp`:

```bash
scp backup.sql usuario_remoto@servidor:/ruta/destino/
```

### 3. **Importación de la Base de Datos en el Servidor**
En el servidor, se utilizó MySQL para importar los datos en la base de datos remota:

```bash
mysql -u usuario_remoto -p nombre_base_datos < /ruta/destino/backup.sql
```

Este comando:
- `-u usuario_remoto`: Especifica el usuario de MySQL en el servidor.
- `-p`: Solicita la contraseña antes de proceder con la importación.
- `nombre_base_datos`: Es el nombre de la base de datos en el servidor donde se importarán los datos.
- `< /ruta/destino/backup.sql`: Indica que se usará el archivo `backup.sql` como fuente para importar los datos.

## Conclusión
Este método permitió transferir **138,123 registros** de forma eficiente y sin pérdida de datos. Usar `mysqldump` y `mysql` garantiza la integridad de la base de datos y permite una migración segura entre entornos locales y remotos.

