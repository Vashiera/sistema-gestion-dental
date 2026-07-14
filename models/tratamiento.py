from decimal import Decimal, InvalidOperation

from database.conexion import obtener_conexion


def obtener_tratamientos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            t.id_tratamiento,
            t.id_paciente,
            t.id_usuario,
            t.id_catalogo,
            t.pieza_dental,
            t.descripcion,
            t.valor_presupuestado,
            t.estado,
            c.nombre_tratamiento,
            c.precio_base,
            p.nombre,
            p.apellido,
            p.rut
        FROM tratamientos t
        INNER JOIN pacientes p
            ON t.id_paciente = p.id_paciente
        INNER JOIN catalogo_tratamientos c
            ON t.id_catalogo = c.id_catalogo
        ORDER BY t.id_tratamiento DESC
    """)

    tratamientos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return tratamientos


def crear_tratamiento(
    id_paciente,
    id_usuario,
    id_catalogo,
    pieza_dental,
    descripcion,
    valor_presupuestado,
    estado
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO tratamientos (
                id_paciente,
                id_usuario,
                id_catalogo,
                pieza_dental,
                descripcion,
                valor_presupuestado,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            id_paciente,
            id_usuario,
            id_catalogo,
            pieza_dental if pieza_dental else None,
            descripcion.strip() if descripcion else "",
            valor_presupuestado,
            estado
        ))

        conexion.commit()

    except Exception:
        conexion.rollback()
        raise

    finally:
        cursor.close()
        conexion.close()


def crear_plan_tratamientos(
    id_paciente,
    id_usuario,
    tratamientos
):
    """
    Guarda varios tratamientos para un mismo paciente.

    Cada elemento debe contener:
        id_catalogo
        pieza_dental
        descripcion
        valor_presupuestado
        estado

    Si uno de los registros falla, no se guarda ninguno.
    """

    if not tratamientos:
        return False, "Debe agregar al menos un tratamiento al plan."

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        for item in tratamientos:
            id_catalogo = item.get("id_catalogo")
            pieza_dental = item.get("pieza_dental")
            descripcion = item.get("descripcion", "")
            estado = item.get("estado", "PLANIFICADO")

            if not id_catalogo:
                conexion.rollback()

                return (
                    False,
                    "Uno de los procedimientos no posee un tratamiento válido."
                )

            if estado not in {
                "PLANIFICADO",
                "EN PROCESO",
                "FINALIZADO"
            }:
                conexion.rollback()

                return (
                    False,
                    "Uno de los tratamientos posee un estado no válido."
                )

            try:
                valor_presupuestado = Decimal(
                    str(item.get("valor_presupuestado", ""))
                )
            except (InvalidOperation, TypeError, ValueError):
                conexion.rollback()

                return (
                    False,
                    "Uno de los tratamientos posee un valor no válido."
                )

            if valor_presupuestado < 0:
                conexion.rollback()

                return (
                    False,
                    "El valor de un tratamiento no puede ser negativo."
                )

            if pieza_dental in ("", None, "GENERAL"):
                pieza_dental = None
            else:
                pieza_dental = str(pieza_dental).strip()

            cursor.execute("""
                INSERT INTO tratamientos (
                    id_paciente,
                    id_usuario,
                    id_catalogo,
                    pieza_dental,
                    descripcion,
                    valor_presupuestado,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                id_paciente,
                id_usuario,
                id_catalogo,
                pieza_dental,
                descripcion.strip() if descripcion else "",
                valor_presupuestado,
                estado
            ))

        conexion.commit()

        return (
            True,
            "Plan de tratamiento registrado correctamente."
        )

    except Exception:
        conexion.rollback()
        raise

    finally:
        cursor.close()
        conexion.close()


def obtener_tratamiento_por_id(id_tratamiento):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            t.id_tratamiento,
            t.id_paciente,
            t.id_usuario,
            t.id_catalogo,
            t.pieza_dental,
            t.descripcion,
            t.valor_presupuestado,
            t.estado,
            p.nombre,
            p.apellido,
            p.rut,
            c.nombre_tratamiento,
            c.precio_base
        FROM tratamientos t
        INNER JOIN pacientes p
            ON t.id_paciente = p.id_paciente
        INNER JOIN catalogo_tratamientos c
            ON t.id_catalogo = c.id_catalogo
        WHERE t.id_tratamiento = %s
    """, (id_tratamiento,))

    tratamiento = cursor.fetchone()

    cursor.close()
    conexion.close()

    return tratamiento


def actualizar_tratamiento(
    id_tratamiento,
    id_paciente,
    id_catalogo,
    pieza_dental,
    descripcion,
    valor_presupuestado,
    estado
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            UPDATE tratamientos
            SET
                id_paciente = %s,
                id_catalogo = %s,
                pieza_dental = %s,
                descripcion = %s,
                valor_presupuestado = %s,
                estado = %s
            WHERE id_tratamiento = %s
        """, (
            id_paciente,
            id_catalogo,
            pieza_dental if pieza_dental else None,
            descripcion.strip() if descripcion else "",
            valor_presupuestado,
            estado,
            id_tratamiento
        ))

        conexion.commit()

    except Exception:
        conexion.rollback()
        raise

    finally:
        cursor.close()
        conexion.close()


def obtener_tratamientos_por_paciente(id_paciente):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            t.id_tratamiento,
            t.id_paciente,
            t.id_usuario,
            t.id_catalogo,
            t.pieza_dental,
            t.descripcion,
            t.valor_presupuestado,
            t.estado,
            c.nombre_tratamiento,
            c.precio_base
        FROM tratamientos t
        INNER JOIN catalogo_tratamientos c
            ON t.id_catalogo = c.id_catalogo
        WHERE t.id_paciente = %s
        ORDER BY t.id_tratamiento DESC
    """, (id_paciente,))

    tratamientos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return tratamientos

def agrupar_tratamientos_por_procedimiento(tratamientos):
    grupos = {}

    for tratamiento in tratamientos:
        id_catalogo = tratamiento["id_catalogo"]

        if id_catalogo not in grupos:
            grupos[id_catalogo] = {
                "id_catalogo": id_catalogo,
                "nombre_tratamiento": tratamiento["nombre_tratamiento"],
                "piezas": [],
                "registros": [],
                "total": 0,
                "cantidad": 0
            }

        pieza = tratamiento.get("pieza_dental")

        if pieza:
            pieza_formateada = f"{pieza[0]}.{pieza[1]}"
        else:
            pieza_formateada = "General"

        grupos[id_catalogo]["piezas"].append(pieza_formateada)
        grupos[id_catalogo]["registros"].append(tratamiento)
        grupos[id_catalogo]["total"] += (
            tratamiento["valor_presupuestado"] or 0
        )
        grupos[id_catalogo]["cantidad"] += 1

    return list(grupos.values())

def obtener_plan_agrupado_por_paciente(id_paciente):
    tratamientos = obtener_tratamientos_por_paciente(id_paciente)

    grupos = agrupar_tratamientos_por_procedimiento(
        tratamientos
    )

    total_plan = sum(
        grupo["total"]
        for grupo in grupos
    )

    return {
        "grupos": grupos,
        "total_plan": total_plan,
        "cantidad_tratamientos": len(tratamientos)
    }