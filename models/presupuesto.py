import json
from database.conexion import obtener_conexion


def obtener_presupuestos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            pr.id_presupuesto,
            pr.numero_presupuesto,
            pr.fecha,
            pr.fecha_vencimiento,
            pr.estado,
            pr.total,
            pr.observaciones,
            p.id_paciente,
            p.nombre,
            p.apellido
        FROM presupuestos pr
        INNER JOIN pacientes p ON pr.id_paciente = p.id_paciente
        ORDER BY pr.id_presupuesto DESC
    """)

    presupuestos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return presupuestos


def generar_numero_presupuesto():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) + 1 AS siguiente FROM presupuestos")
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    return f"PRES-{resultado['siguiente']:06d}"


def crear_presupuesto(
    id_paciente,
    id_usuario,
    fecha,
    fecha_vencimiento,
    estado,
    observaciones,
    detalles
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    numero_presupuesto = generar_numero_presupuesto()

    total = 0

    for item in detalles:
        total += int(item["cantidad"]) * float(item["precio_unitario"])

    cursor.execute("""
        INSERT INTO presupuestos (
            numero_presupuesto,
            id_paciente,
            id_usuario,
            fecha,
            fecha_vencimiento,
            estado,
            total,
            observaciones
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        numero_presupuesto,
        id_paciente,
        id_usuario,
        fecha,
        fecha_vencimiento,
        estado,
        total,
        observaciones
    ))

    id_presupuesto = cursor.lastrowid

    for item in detalles:
        cantidad = int(item["cantidad"])
        precio_unitario = float(item["precio_unitario"])
        subtotal = cantidad * precio_unitario

        cursor.execute("""
            INSERT INTO detalle_presupuesto (
                id_presupuesto,
                id_catalogo,
                cantidad,
                precio_unitario,
                subtotal
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            id_presupuesto,
            item["id_catalogo"],
            cantidad,
            precio_unitario,
            subtotal
        ))

    conexion.commit()
    cursor.close()
    conexion.close()


def obtener_presupuesto_por_id(id_presupuesto):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            pr.*,
            p.nombre,
            p.apellido,
            p.rut,
            p.telefono,
            p.correo
        FROM presupuestos pr
        INNER JOIN pacientes p ON pr.id_paciente = p.id_paciente
        WHERE pr.id_presupuesto = %s
    """, (id_presupuesto,))

    presupuesto = cursor.fetchone()

    cursor.execute("""
        SELECT
            dp.*,
            ct.nombre_tratamiento
        FROM detalle_presupuesto dp
        INNER JOIN catalogo_tratamientos ct
            ON dp.id_catalogo = ct.id_catalogo
        WHERE dp.id_presupuesto = %s
    """, (id_presupuesto,))

    detalle = cursor.fetchall()

    cursor.close()
    conexion.close()

    return presupuesto, detalle