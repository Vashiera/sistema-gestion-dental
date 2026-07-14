from database.conexion import obtener_conexion


def obtener_documentos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            d.id_documento,
            d.id_paciente,
            d.id_tipo_documento,
            d.nombre_documento,
            d.ruta_archivo,
            d.fecha_subida,
            p.nombre,
            p.apellido,
            td.nombre_tipo
        FROM documentos d
        INNER JOIN pacientes p
            ON d.id_paciente = p.id_paciente
        INNER JOIN tipos_documento td
            ON d.id_tipo_documento = td.id_tipo_documento
        ORDER BY d.id_documento DESC
    """)

    documentos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return documentos


def obtener_tipos_documento():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_tipo_documento,
            nombre_tipo
        FROM tipos_documento
        ORDER BY nombre_tipo
    """)

    tipos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return tipos


def crear_documento(
    id_paciente,
    id_tipo_documento,
    nombre_documento,
    ruta_archivo
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO documentos (
            id_paciente,
            id_tipo_documento,
            nombre_documento,
            ruta_archivo
        )
        VALUES (%s, %s, %s, %s)
    """, (
        id_paciente,
        id_tipo_documento,
        nombre_documento,
        ruta_archivo
    ))

    conexion.commit()

    cursor.close()
    conexion.close()

def obtener_documentos_por_paciente(id_paciente):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            d.id_documento,
            d.id_paciente,
            d.id_tipo_documento,
            d.nombre_documento,
            d.ruta_archivo,
            d.fecha_subida,
            td.nombre_tipo
        FROM documentos d
        INNER JOIN tipos_documento td
            ON d.id_tipo_documento = td.id_tipo_documento
        WHERE d.id_paciente = %s
        ORDER BY d.id_documento DESC
    """, (id_paciente,))

    documentos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return documentos