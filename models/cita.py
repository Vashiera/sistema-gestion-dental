from database.conexion import obtener_conexion


def obtener_citas():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            c.id_cita,
            c.id_paciente,
            c.id_usuario,
            DATE_FORMAT(c.fecha, '%Y-%m-%d') AS fecha,
            TIME_FORMAT(c.hora, '%H:%i') AS hora,
            c.duracion_minutos,
            c.motivo,
            c.estado,
            p.nombre,
            p.apellido,
            u.nombre AS nombre_profesional
        FROM citas c
        INNER JOIN pacientes p
            ON c.id_paciente = p.id_paciente
        INNER JOIN usuarios u
            ON c.id_usuario = u.id_usuario
        ORDER BY c.fecha DESC, c.hora ASC
    """)

    citas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return citas


def obtener_cita_por_id(id_cita):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            c.id_cita,
            c.id_paciente,
            c.id_usuario,
            DATE_FORMAT(c.fecha, '%Y-%m-%d') AS fecha,
            TIME_FORMAT(c.hora, '%H:%i') AS hora,
            c.duracion_minutos,
            c.motivo,
            c.estado
        FROM citas c
        WHERE c.id_cita = %s
    """, (id_cita,))

    cita = cursor.fetchone()

    cursor.close()
    conexion.close()

    return cita


def existe_cita_en_horario(
    id_usuario,
    fecha,
    hora,
    duracion_minutos,
    id_cita_excluir=None
):
    """
    Comprueba si el periodo solicitado se cruza con otra cita
    activa del mismo profesional.

    La validación considera tanto la hora de inicio como la
    duración de cada cita.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT
            id_cita
        FROM citas
        WHERE id_usuario = %s
        AND estado <> 'CANCELADA'

        AND TIMESTAMP(fecha, hora) <
            TIMESTAMPADD(
                MINUTE,
                %s,
                TIMESTAMP(%s, %s)
            )

        AND TIMESTAMPADD(
                MINUTE,
                duracion_minutos,
                TIMESTAMP(fecha, hora)
            ) >
            TIMESTAMP(%s, %s)
    """

    parametros = [
        id_usuario,
        duracion_minutos,
        fecha,
        hora,
        fecha,
        hora
    ]

    if id_cita_excluir is not None:
        consulta += """
            AND id_cita <> %s
        """
        parametros.append(id_cita_excluir)

    consulta += """
        LIMIT 1
    """

    cursor.execute(consulta, tuple(parametros))

    cita = cursor.fetchone()

    cursor.close()
    conexion.close()

    return cita is not None


def crear_cita(
    id_paciente,
    id_usuario,
    fecha,
    hora,
    duracion_minutos,
    motivo,
    estado
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO citas (
            id_paciente,
            id_usuario,
            fecha,
            hora,
            duracion_minutos,
            motivo,
            estado
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        id_paciente,
        id_usuario,
        fecha,
        hora,
        duracion_minutos,
        motivo,
        estado
    ))

    conexion.commit()

    cursor.close()
    conexion.close()


def actualizar_cita(
    id_cita,
    id_paciente,
    id_usuario,
    fecha,
    hora,
    duracion_minutos,
    motivo,
    estado
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE citas
        SET
            id_paciente = %s,
            id_usuario = %s,
            fecha = %s,
            hora = %s,
            duracion_minutos = %s,
            motivo = %s,
            estado = %s
        WHERE id_cita = %s
    """, (
        id_paciente,
        id_usuario,
        fecha,
        hora,
        duracion_minutos,
        motivo,
        estado,
        id_cita
    ))

    conexion.commit()

    cursor.close()
    conexion.close()


def cancelar_cita(id_cita):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE citas
        SET estado = 'CANCELADA'
        WHERE id_cita = %s
    """, (id_cita,))

    conexion.commit()

    cursor.close()
    conexion.close()

def obtener_citas_por_paciente(id_paciente):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            c.id_cita,
            c.id_paciente,
            c.id_usuario,
            DATE_FORMAT(c.fecha, '%Y-%m-%d') AS fecha,
            TIME_FORMAT(c.hora, '%H:%i') AS hora,
            c.duracion_minutos,
            c.motivo,
            c.estado,
            u.nombre AS nombre_profesional
        FROM citas c
        INNER JOIN usuarios u
            ON c.id_usuario = u.id_usuario
        WHERE c.id_paciente = %s
        ORDER BY c.fecha DESC, c.hora DESC
    """, (id_paciente,))

    citas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return citas

def obtener_citas_por_fecha(fecha):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            c.id_cita,
            c.id_paciente,
            c.id_usuario,
            DATE_FORMAT(c.fecha, '%Y-%m-%d') AS fecha,
            TIME_FORMAT(c.hora, '%H:%i') AS hora,
            c.duracion_minutos,
            c.motivo,
            c.estado,
            p.nombre,
            p.apellido,
            p.rut,
            u.nombre AS nombre_profesional
        FROM citas c
        INNER JOIN pacientes p
            ON c.id_paciente = p.id_paciente
        INNER JOIN usuarios u
            ON c.id_usuario = u.id_usuario
        WHERE c.fecha = %s
        ORDER BY c.hora ASC
    """, (fecha,))

    citas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return citas