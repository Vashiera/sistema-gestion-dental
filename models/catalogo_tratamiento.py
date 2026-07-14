from database.conexion import obtener_conexion


def obtener_catalogo_tratamientos():

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_catalogo,
            nombre_tratamiento,
            precio_base
        FROM catalogo_tratamientos
        WHERE activo = 1
        ORDER BY nombre_tratamiento
    """)

    tratamientos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return tratamientos


def obtener_catalogo_por_id(id_catalogo):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM catalogo_tratamientos
        WHERE id_catalogo=%s
    """, (id_catalogo,))

    tratamiento = cursor.fetchone()

    cursor.close()
    conexion.close()

    return tratamiento