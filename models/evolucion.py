from database.conexion import obtener_conexion


def obtener_evoluciones():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            e.id_evolucion,
            e.id_tratamiento,
            e.id_usuario,
            DATE_FORMAT(e.fecha, '%Y-%m-%d') AS fecha,
            e.procedimiento_realizado,
            e.observaciones,

            t.id_paciente,
            t.pieza_dental,
            t.estado AS estado_tratamiento,

            ct.nombre_tratamiento,

            p.nombre,
            p.apellido,
            p.rut,

            u.nombre AS nombre_profesional

        FROM evoluciones e

        INNER JOIN tratamientos t
            ON e.id_tratamiento = t.id_tratamiento

        INNER JOIN catalogo_tratamientos ct
            ON t.id_catalogo = ct.id_catalogo

        INNER JOIN pacientes p
            ON t.id_paciente = p.id_paciente

        INNER JOIN usuarios u
            ON e.id_usuario = u.id_usuario

        ORDER BY
            e.fecha DESC,
            e.id_evolucion DESC
    """)

    evoluciones = cursor.fetchall()

    cursor.close()
    conexion.close()

    return evoluciones


def obtener_evolucion_por_id(id_evolucion):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            e.id_evolucion,
            e.id_tratamiento,
            e.id_usuario,
            DATE_FORMAT(e.fecha, '%Y-%m-%d') AS fecha,
            e.procedimiento_realizado,
            e.observaciones,

            t.id_paciente,
            t.pieza_dental,
            t.estado AS estado_tratamiento,

            ct.nombre_tratamiento,

            p.nombre,
            p.apellido,
            p.rut,

            u.nombre AS nombre_profesional

        FROM evoluciones e

        INNER JOIN tratamientos t
            ON e.id_tratamiento = t.id_tratamiento

        INNER JOIN catalogo_tratamientos ct
            ON t.id_catalogo = ct.id_catalogo

        INNER JOIN pacientes p
            ON t.id_paciente = p.id_paciente

        INNER JOIN usuarios u
            ON e.id_usuario = u.id_usuario

        WHERE e.id_evolucion = %s
    """, (id_evolucion,))

    evolucion = cursor.fetchone()

    cursor.close()
    conexion.close()

    return evolucion


def obtener_evoluciones_por_paciente(id_paciente):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            e.id_evolucion,
            e.id_tratamiento,
            e.id_usuario,
            DATE_FORMAT(e.fecha, '%Y-%m-%d') AS fecha,
            e.procedimiento_realizado,
            e.observaciones,

            t.id_paciente,
            t.pieza_dental,
            t.estado AS estado_tratamiento,

            ct.nombre_tratamiento,

            u.nombre AS nombre_profesional

        FROM evoluciones e

        INNER JOIN tratamientos t
            ON e.id_tratamiento = t.id_tratamiento

        INNER JOIN catalogo_tratamientos ct
            ON t.id_catalogo = ct.id_catalogo

        INNER JOIN usuarios u
            ON e.id_usuario = u.id_usuario

        WHERE t.id_paciente = %s

        ORDER BY
            e.fecha DESC,
            e.id_evolucion DESC
    """, (id_paciente,))

    evoluciones = cursor.fetchall()

    cursor.close()
    conexion.close()

    return evoluciones


def obtener_evoluciones_por_tratamiento(id_tratamiento):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            e.id_evolucion,
            e.id_tratamiento,
            e.id_usuario,
            DATE_FORMAT(e.fecha, '%Y-%m-%d') AS fecha,
            e.procedimiento_realizado,
            e.observaciones,

            u.nombre AS nombre_profesional

        FROM evoluciones e

        INNER JOIN usuarios u
            ON e.id_usuario = u.id_usuario

        WHERE e.id_tratamiento = %s

        ORDER BY
            e.fecha DESC,
            e.id_evolucion DESC
    """, (id_tratamiento,))

    evoluciones = cursor.fetchall()

    cursor.close()
    conexion.close()

    return evoluciones


def crear_evolucion(
    id_tratamiento,
    id_usuario,
    fecha,
    procedimiento_realizado,
    observaciones
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO evoluciones (
                id_tratamiento,
                id_usuario,
                fecha,
                procedimiento_realizado,
                observaciones
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            id_tratamiento,
            id_usuario,
            fecha,
            procedimiento_realizado.strip(),
            observaciones.strip() if observaciones else ""
        ))

        conexion.commit()

    except Exception:
        conexion.rollback()
        raise

    finally:
        cursor.close()
        conexion.close()


def actualizar_evolucion(
    id_evolucion,
    id_tratamiento,
    id_usuario,
    fecha,
    procedimiento_realizado,
    observaciones
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            UPDATE evoluciones
            SET
                id_tratamiento = %s,
                id_usuario = %s,
                fecha = %s,
                procedimiento_realizado = %s,
                observaciones = %s
            WHERE id_evolucion = %s
        """, (
            id_tratamiento,
            id_usuario,
            fecha,
            procedimiento_realizado.strip(),
            observaciones.strip() if observaciones else "",
            id_evolucion
        ))

        conexion.commit()

    except Exception:
        conexion.rollback()
        raise

    finally:
        cursor.close()
        conexion.close()