from database.conexion import obtener_conexion


def obtener_resumen_dashboard():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            (
                SELECT COUNT(*)
                FROM pacientes
                WHERE estado = 'ACTIVO'
            ) AS pacientes_activos,

            (
                SELECT COUNT(*)
                FROM citas
                WHERE fecha = CURDATE()
                AND estado <> 'CANCELADA'
            ) AS citas_hoy,

            (
                SELECT COUNT(*)
                FROM tratamientos
                WHERE estado IN ('PLANIFICADO', 'EN PROCESO')
            ) AS tratamientos_pendientes,

            (
                SELECT COUNT(*)
                FROM documentos
            ) AS documentos_registrados,

            (
                SELECT COALESCE(SUM(valor_presupuestado), 0)
                FROM tratamientos
            ) AS total_tratamientos,

            (
                SELECT COALESCE(SUM(monto), 0)
                FROM pagos
                WHERE estado = 'REGISTRADO'
            ) AS total_pagado
    """)

    resumen = cursor.fetchone()

    cursor.close()
    conexion.close()

    total_tratamientos = resumen["total_tratamientos"] or 0
    total_pagado = resumen["total_pagado"] or 0

    saldo_pendiente = total_tratamientos - total_pagado

    if saldo_pendiente < 0:
        saldo_pendiente = 0

    resumen["saldo_pendiente"] = saldo_pendiente

    return resumen


def obtener_citas_hoy_dashboard():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            c.id_cita,
            TIME_FORMAT(c.hora, '%H:%i') AS hora,
            c.motivo,
            c.estado,
            c.duracion_minutos,
            p.id_paciente,
            p.nombre,
            p.apellido,
            u.nombre AS nombre_profesional
        FROM citas c
        INNER JOIN pacientes p
            ON c.id_paciente = p.id_paciente
        INNER JOIN usuarios u
            ON c.id_usuario = u.id_usuario
        WHERE c.fecha = CURDATE()
        AND c.estado <> 'CANCELADA'
        ORDER BY c.hora ASC
        LIMIT 8
    """)

    citas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return citas


def obtener_evoluciones_recientes_dashboard():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            e.id_evolucion,
            DATE_FORMAT(e.fecha, '%d/%m/%Y') AS fecha,
            e.procedimiento_realizado,
            t.id_paciente,
            t.pieza_dental,
            ct.nombre_tratamiento,
            p.nombre,
            p.apellido,
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
        ORDER BY e.fecha DESC, e.id_evolucion DESC
        LIMIT 5
    """)

    evoluciones = cursor.fetchall()

    cursor.close()
    conexion.close()

    return evoluciones


def obtener_pagos_recientes_dashboard():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            pg.id_pago,
            pg.id_paciente,
            DATE_FORMAT(
                pg.fecha_pago,
                '%d/%m/%Y %H:%i'
            ) AS fecha_pago,
            pg.monto,
            pg.metodo_pago,
            p.nombre,
            p.apellido
        FROM pagos pg
        INNER JOIN pacientes p
            ON pg.id_paciente = p.id_paciente
        WHERE pg.estado = 'REGISTRADO'
        ORDER BY pg.fecha_pago DESC, pg.id_pago DESC
        LIMIT 5
    """)

    pagos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return pagos


def obtener_alertas_dashboard():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    alertas = []

    cursor.execute("""
        SELECT COUNT(*) AS cantidad
        FROM tratamientos
        WHERE estado = 'PLANIFICADO'
    """)

    tratamientos_planificados = cursor.fetchone()["cantidad"]

    if tratamientos_planificados > 0:
        alertas.append({
            "tipo": "tratamientos",
            "mensaje": (
                f"Hay {tratamientos_planificados} tratamiento"
                f"{'s' if tratamientos_planificados != 1 else ''} "
                "planificado"
                f"{'s' if tratamientos_planificados != 1 else ''}."
            )
        })

    cursor.execute("""
        SELECT COUNT(*) AS cantidad
        FROM citas
        WHERE fecha < CURDATE()
        AND estado IN ('PROGRAMADA', 'CONFIRMADA')
    """)

    citas_vencidas = cursor.fetchone()["cantidad"]

    if citas_vencidas > 0:
        alertas.append({
            "tipo": "citas",
            "mensaje": (
                f"Hay {citas_vencidas} cita"
                f"{'s' if citas_vencidas != 1 else ''} "
                "pasada"
                f"{'s' if citas_vencidas != 1 else ''} "
                "sin actualizar."
            )
        })

    cursor.execute("""
        SELECT COUNT(*) AS cantidad
        FROM documentos
        WHERE ruta_archivo IS NULL
        OR ruta_archivo = ''
    """)

    documentos_sin_archivo = cursor.fetchone()["cantidad"]

    if documentos_sin_archivo > 0:
        alertas.append({
            "tipo": "documentos",
            "mensaje": (
                f"Hay {documentos_sin_archivo} documento"
                f"{'s' if documentos_sin_archivo != 1 else ''} "
                "sin archivo adjunto."
            )
        })

    cursor.close()
    conexion.close()

    return alertas