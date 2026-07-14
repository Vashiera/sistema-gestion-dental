from decimal import Decimal, InvalidOperation

from database.conexion import obtener_conexion


def obtener_estados_cuenta():
    """
    Retorna el estado financiero global de los pacientes que poseen
    tratamientos o pagos registrados.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.id_paciente,
            p.rut,
            p.nombre,
            p.apellido,
            p.estado,

            COALESCE(t.total_tratamientos, 0) AS total_tratamientos,
            COALESCE(pg.total_pagado, 0) AS total_pagado,

            GREATEST(
                COALESCE(t.total_tratamientos, 0)
                - COALESCE(pg.total_pagado, 0),
                0
            ) AS saldo

        FROM pacientes p

        LEFT JOIN (
            SELECT
                id_paciente,
                SUM(valor_presupuestado) AS total_tratamientos
            FROM tratamientos
            GROUP BY id_paciente
        ) t
            ON p.id_paciente = t.id_paciente

        LEFT JOIN (
            SELECT
                id_paciente,
                SUM(monto) AS total_pagado
            FROM pagos
            WHERE estado = 'REGISTRADO'
            GROUP BY id_paciente
        ) pg
            ON p.id_paciente = pg.id_paciente

        WHERE
            t.total_tratamientos IS NOT NULL
            OR pg.total_pagado IS NOT NULL

        ORDER BY
            saldo DESC,
            p.apellido,
            p.nombre
    """)

    estados_cuenta = cursor.fetchall()

    cursor.close()
    conexion.close()

    for cuenta in estados_cuenta:
        cuenta["estado_pago"] = calcular_estado_pago(
            cuenta["total_tratamientos"],
            cuenta["total_pagado"]
        )

    return estados_cuenta


def obtener_estado_cuenta_paciente(id_paciente):
    """
    Retorna el resumen financiero individual de un paciente.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            p.id_paciente,
            p.rut,
            p.nombre,
            p.apellido,
            p.telefono,
            p.correo,

            COALESCE((
                SELECT SUM(t.valor_presupuestado)
                FROM tratamientos t
                WHERE t.id_paciente = p.id_paciente
            ), 0) AS total_tratamientos,

            COALESCE((
                SELECT SUM(pg.monto)
                FROM pagos pg
                WHERE pg.id_paciente = p.id_paciente
                AND pg.estado = 'REGISTRADO'
            ), 0) AS total_pagado

        FROM pacientes p
        WHERE p.id_paciente = %s
    """, (id_paciente,))

    cuenta = cursor.fetchone()

    cursor.close()
    conexion.close()

    if cuenta is None:
        return None

    total_tratamientos = Decimal(
        str(cuenta["total_tratamientos"] or 0)
    )

    total_pagado = Decimal(
        str(cuenta["total_pagado"] or 0)
    )

    saldo = total_tratamientos - total_pagado

    if saldo < 0:
        saldo = Decimal("0")

    cuenta["saldo"] = saldo

    cuenta["estado_pago"] = calcular_estado_pago(
        total_tratamientos,
        total_pagado
    )

    return cuenta


def obtener_pagos_por_paciente(id_paciente):
    """
    Obtiene el historial de pagos registrados para un paciente.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            pg.id_pago,
            pg.id_paciente,
            pg.id_usuario,
            DATE_FORMAT(
                pg.fecha_pago,
                '%Y-%m-%d %H:%i'
            ) AS fecha_pago,
            pg.monto,
            pg.metodo_pago,
            pg.observaciones,
            pg.estado,
            u.nombre AS nombre_usuario

        FROM pagos pg

        INNER JOIN usuarios u
            ON pg.id_usuario = u.id_usuario

        WHERE pg.id_paciente = %s

        ORDER BY
            pg.fecha_pago DESC,
            pg.id_pago DESC
    """, (id_paciente,))

    pagos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return pagos


def obtener_tratamientos_financieros_por_paciente(id_paciente):
    """
    Obtiene los tratamientos valorizados que conforman el total
    del estado de cuenta del paciente.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            t.id_tratamiento,
            t.pieza_dental,
            t.descripcion,
            t.valor_presupuestado,
            t.estado,
            ct.nombre_tratamiento

        FROM tratamientos t

        INNER JOIN catalogo_tratamientos ct
            ON t.id_catalogo = ct.id_catalogo

        WHERE t.id_paciente = %s

        ORDER BY t.id_tratamiento DESC
    """, (id_paciente,))

    tratamientos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return tratamientos


def registrar_pago(
    id_paciente,
    id_usuario,
    monto,
    metodo_pago,
    observaciones
):
    """
    Registra un abono siempre que el monto sea válido y no supere
    el saldo pendiente.

    Retorna:
        (True, mensaje) cuando el pago se registra.
        (False, mensaje) cuando existe un error de validación.
    """

    metodos_permitidos = {
        "EFECTIVO",
        "DEBITO",
        "CREDITO",
        "TRANSFERENCIA"
    }

    if metodo_pago not in metodos_permitidos:
        return False, "El método de pago seleccionado no es válido."

    try:
        monto_decimal = Decimal(str(monto))
    except (InvalidOperation, TypeError, ValueError):
        return False, "El monto ingresado no es válido."

    if monto_decimal <= 0:
        return False, "El monto del pago debe ser mayor que cero."

    cuenta = obtener_estado_cuenta_paciente(id_paciente)

    if cuenta is None:
        return False, "El paciente seleccionado no existe."

    saldo = Decimal(str(cuenta["saldo"] or 0))

    if saldo <= 0:
        return False, "El paciente no tiene saldo pendiente."

    if monto_decimal > saldo:
        return (
            False,
            "El monto ingresado no puede superar el saldo pendiente."
        )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO pagos (
            id_paciente,
            id_usuario,
            monto,
            metodo_pago,
            observaciones,
            estado
        )
        VALUES (%s, %s, %s, %s, %s, 'REGISTRADO')
    """, (
        id_paciente,
        id_usuario,
        monto_decimal,
        metodo_pago,
        observaciones.strip() if observaciones else ""
    ))

    conexion.commit()

    cursor.close()
    conexion.close()

    return True, "Pago registrado correctamente."


def anular_pago(id_pago):
    """
    Anula un pago sin eliminarlo, conservándolo en el historial.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE pagos
        SET estado = 'ANULADO'
        WHERE id_pago = %s
        AND estado = 'REGISTRADO'
    """, (id_pago,))

    conexion.commit()

    actualizado = cursor.rowcount > 0

    cursor.close()
    conexion.close()

    return actualizado


def calcular_estado_pago(total_tratamientos, total_pagado):
    """
    Determina automáticamente el estado financiero del paciente.
    """

    total = Decimal(str(total_tratamientos or 0))
    pagado = Decimal(str(total_pagado or 0))

    if total <= 0:
        return "SIN TRATAMIENTOS"

    if pagado <= 0:
        return "PENDIENTE"

    if pagado < total:
        return "PAGO PARCIAL"

    return "PAGADO"