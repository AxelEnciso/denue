# import pandas as pd
# import mysql.connector

# conexion = mysql.connector.connect(
#     host='localhost',
#     port=4242,
#     user='root',
#     password='prueba123',
#     database='denue_axel'
# )

# cursor = conexion.cursor()

# df = pd.read_excel('copia_denue.xlsx')

# # Diccionarios para evitar duplicados
# tipos_vial = {}
# tipos_asent = {}
# contactos = {}
# localizaciones = {}

# def insertar_si_no_existe(diccionario, tabla, campo, valor):
#     if pd.isnull(valor) or valor == '':
#         return None  # no insertará valores nulos o vacíos
#     if valor not in diccionario:
#         cursor.execute(f"INSERT INTO {tabla} ({campo}) VALUES (%s)", (valor,))
#         diccionario[valor] = cursor.lastrowid
#     return diccionario[valor]


# for indice, fila in df.iterrows():
#     # Inserta y/o obtiene IDs
#     id_tipo_vial = insertar_si_no_existe(tipos_vial, 'tipo_vial', 'tipo', fila['tipo_vial'])
#     id_tipo_asent = insertar_si_no_existe(tipos_asent, 'tipo_asentamiento', 'tipo', fila['tipo_asent'])
#     if id_tipo_asent is None:
#         continue  

#     contacto_key = (fila['telefono'], fila['correoelec'], fila['WEB'], fila['contactos'])
#     if contacto_key not in contactos:
#         cursor.execute("""
#             INSERT INTO contacto (telefono, correoelec, web, contactos)
#             VALUES (%s, %s, %s, %s)
#         """, contacto_key)
#         contactos[contacto_key] = cursor.lastrowid

#     id_contacto = contactos[contacto_key]

#     loc_key = (id_tipo_vial, id_tipo_asent, fila['edificio'], fila['edificio_e'],
#                fila['nomb_asent'], fila['latitud'], fila['longitud'], fila['cod_postal'],
#                fila['cve_mun'], fila['cve_loc'])

#     if loc_key not in localizaciones:
#         cursor.execute("""
#             INSERT INTO localizacion (id_tipo_vial, id_tipo_asent, edificio, edificio_e, nomb_asent, latitud, longitud, cod_postal, cve_mun, cve_loc)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """, loc_key)
#         localizaciones[loc_key] = cursor.lastrowid

#     id_localizacion = localizaciones[loc_key]

#     # Inserta en tabla establecimiento
#     cursor.execute("""
#         INSERT INTO establecimiento (id_localizacion, id_contacto, nombre, razon_social, codigo_act, fecha_alta)
#         VALUES (%s, %s, %s, %s, %s, %s)
#     """, (id_localizacion, id_contacto, fila['nombre'], fila['razon_social'], fila['codigo_act'], fila['fecha_alta'].strftime('%Y-%m-%d') if not pd.isnull(fila['fecha_alta']) else None
# ))

# # Confirmar los cambios
# conexion.commit()
# cursor.close()
# conexion.close()

# print("Datos insertados correctamente")

# # scp boats.csv pako@10.4.8.40~
import pandas as pd
import mysql.connector
import json

# Conexión a MySQL
conexion = mysql.connector.connect(
    host='localhost',
    port=4242,
    user='root',
    password='prueba123',
    database='denue_axel'
)

cursor = conexion.cursor()

# Leer archivo Excel
df = pd.read_excel('copia_denue.xlsx')

# Diccionarios para evitar duplicados
tipos_vial = {}
tipos_asent = {}
contactos = {}
localizaciones = {}

# Iterar sobre cada fila
def insertar_si_no_existe(diccionario, tabla, campo, valor):
    if pd.isnull(valor) or valor == '':
        return None  # Evita insertar valores nulos o vacíos
    if valor not in diccionario:
        cursor.execute(f"INSERT INTO {tabla} ({campo}) VALUES (%s)", (valor,))
        diccionario[valor] = cursor.lastrowid
    return diccionario[valor]

for indice, fila in df.iterrows():
    # Inserta y/o obtiene IDs
    id_tipo_vial = insertar_si_no_existe(tipos_vial, 'tipo_vial', 'tipo', fila['tipo_vial'])
    id_tipo_asent = insertar_si_no_existe(tipos_asent, 'tipo_asentamiento', 'tipo', fila['tipo_asent'])

    contacto_key = (fila['telefono'], fila['correoelec'], fila['WEB'], fila['contactos'])
    if contacto_key not in contactos:
        telefono_json = json.dumps({"tel1": fila['telefono'], "tel2": fila['contactos']}) if not pd.isnull(fila['telefono']) else json.dumps({})
        correo_json = json.dumps({"email1": fila['correoelec']}) if not pd.isnull(fila['correoelec']) else json.dumps({})
        web_json = json.dumps({"web1": fila['WEB']}) if not pd.isnull(fila['WEB']) else json.dumps({})

        
        cursor.execute("""
            INSERT INTO contacto (telefono, correoelectronico, web, contactos)
            VALUES (%s, %s, %s, %s)
        """, (str(telefono_json), str(correo_json), str(web_json), fila['contactos']))
        contactos[contacto_key] = cursor.lastrowid

    id_contacto = contactos[contacto_key]

    loc_key = (id_tipo_vial, id_tipo_asent, fila['edificio'], fila['edificio_e'],
               fila['nomb_asent'], fila['latitud'], fila['longitud'], fila['cod_postal'],
               fila['cve_mun'], fila['cve_loc'])

    if loc_key not in localizaciones:
        cursor.execute("""
            INSERT INTO localizacion (id_tipo_vial, id_tipo_asent, edificio, edificio_e, nomb_asent, latitud, longitud, cod_postal, cve_mun, cve_loc, coordenadas)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_PointFromText(CONCAT('POINT(', %s, ' ', %s, ')')))
        """, (*loc_key, fila['longitud'], fila['latitud']))
        localizaciones[loc_key] = cursor.lastrowid

    id_localizacion = localizaciones[loc_key]

    # Inserta en tabla establecimiento
    cursor.execute("""
        INSERT INTO establecimiento (id_localizacion, id_contacto, nombre, razon_social, codigo_act, fecha_alta)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (id_localizacion, id_contacto, fila['nombre'], fila['razon_social'], fila['codigo_act'], 
          fila['fecha_alta'].strftime('%Y-%m-%d') if not pd.isnull(fila['fecha_alta']) else None))

# Confirmar los cambios
conexion.commit()
cursor.close()
conexion.close()

print("Datos insertados correctamente")
