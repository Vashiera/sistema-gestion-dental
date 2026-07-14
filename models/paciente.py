from database.conexion import obtener_conexion


# ----------------------------------------------------
# FORMATEO DE DATOS
# ----------------------------------------------------

def formatear_rut(rut):
    rut = rut.replace(".", "").replace("-", "").upper().strip()

    if len(rut) < 2:
        return rut

    cuerpo = rut[:-1]
    dv = rut[-1]

    cuerpo_formateado = ""
    contador = 0

    for numero in reversed(cuerpo):
        if contador == 3:
            cuerpo_formateado = "." + cuerpo_formateado
            contador = 0

        cuerpo_formateado = numero + cuerpo_formateado
        contador += 1

    return f"{cuerpo_formateado}-{dv}"


def formatear_telefono(telefono):
    if not telefono:
        return ""

    telefono = (
        telefono.replace("+", "")
        .replace(" ", "")
        .replace("-", "")
        .strip()
    )

    if telefono.startswith("56"):
        telefono = telefono[2:]

    if telefono.startswith("9") and len(telefono) == 9:
        return f"+56 9 {telefono[1:5]} {telefono[5:]}"

    return telefono


def formatear_texto(texto):
    if not texto:
        return ""

    return texto.strip().title()


# ----------------------------------------------------
# CONSULTAS DE PACIENTES
# ----------------------------------------------------

def obtener_pacientes():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_paciente,
            rut,
            nombre,
            apellido,
            telefono,
            correo,
            estado
        FROM pacientes
        ORDER BY id_paciente DESC
    """)

    pacientes = cursor.fetchall()

    cursor.close()
    conexion.close()

    return pacientes


def obtener_paciente_por_id(id_paciente):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_paciente,
            rut,
            nombre,
            apellido,
            telefono,
            correo,
            direccion,
            fecha_nacimiento,
            estado
        FROM pacientes
        WHERE id_paciente = %s
    """, (id_paciente,))

    paciente = cursor.fetchone()

    cursor.close()
    conexion.close()

    return paciente


def obtener_lista_pacientes():
    """
    Retorna solamente pacientes activos para los selectores
    de Agenda, Tratamientos, Presupuestos y Documentos.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_paciente,
            rut,
            nombre,
            apellido
        FROM pacientes
        WHERE estado = 'ACTIVO'
        ORDER BY nombre, apellido
    """)

    pacientes = cursor.fetchall()

    cursor.close()
    conexion.close()

    return pacientes


# ----------------------------------------------------
# CREAR PACIENTE
# ----------------------------------------------------

def crear_paciente(
    rut,
    nombre,
    apellido,
    telefono,
    correo,
    direccion,
    fecha_nacimiento
):
    rut = formatear_rut(rut)
    nombre = formatear_texto(nombre)
    apellido = formatear_texto(apellido)
    telefono = formatear_telefono(telefono)
    correo = correo.strip().lower() if correo else ""
    direccion = direccion.strip() if direccion else ""

    if fecha_nacimiento == "":
        fecha_nacimiento = None

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO pacientes (
            rut,
            nombre,
            apellido,
            telefono,
            correo,
            direccion,
            fecha_nacimiento,
            estado
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'ACTIVO')
    """, (
        rut,
        nombre,
        apellido,
        telefono,
        correo,
        direccion,
        fecha_nacimiento
    ))

    conexion.commit()

    cursor.close()
    conexion.close()


# ----------------------------------------------------
# ACTUALIZAR PACIENTE
# ----------------------------------------------------

def actualizar_paciente(
    id_paciente,
    rut,
    nombre,
    apellido,
    telefono,
    correo,
    direccion,
    fecha_nacimiento
):
    rut = formatear_rut(rut)
    nombre = formatear_texto(nombre)
    apellido = formatear_texto(apellido)
    telefono = formatear_telefono(telefono)
    correo = correo.strip().lower() if correo else ""
    direccion = direccion.strip() if direccion else ""

    if fecha_nacimiento == "":
        fecha_nacimiento = None

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE pacientes
        SET
            rut = %s,
            nombre = %s,
            apellido = %s,
            telefono = %s,
            correo = %s,
            direccion = %s,
            fecha_nacimiento = %s
        WHERE id_paciente = %s
    """, (
        rut,
        nombre,
        apellido,
        telefono,
        correo,
        direccion,
        fecha_nacimiento,
        id_paciente
    ))

    conexion.commit()

    cursor.close()
    conexion.close()


# ----------------------------------------------------
# ACTIVAR O DESACTIVAR PACIENTE
# ----------------------------------------------------

def cambiar_estado_paciente(id_paciente, nuevo_estado):
    estados_permitidos = ("ACTIVO", "INACTIVO")

    if nuevo_estado not in estados_permitidos:
        raise ValueError("Estado de paciente no permitido.")

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE pacientes
        SET estado = %s
        WHERE id_paciente = %s
    """, (
        nuevo_estado,
        id_paciente
    ))

    conexion.commit()

    cursor.close()
    conexion.close()


# ----------------------------------------------------
# ELIMINACIÓN SEGURA DE DUPLICADOS
# ----------------------------------------------------

def paciente_tiene_informacion_asociada(id_paciente):
    """
    Comprueba si el paciente tiene citas, tratamientos,
    presupuestos o documentos relacionados.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            (
                SELECT COUNT(*)
                FROM citas
                WHERE id_paciente = %s
            ) AS cantidad_citas,

            (
                SELECT COUNT(*)
                FROM tratamientos
                WHERE id_paciente = %s
            ) AS cantidad_tratamientos,

            (
                SELECT COUNT(*)
                FROM presupuestos
                WHERE id_paciente = %s
            ) AS cantidad_presupuestos,

            (
                SELECT COUNT(*)
                FROM documentos
                WHERE id_paciente = %s
            ) AS cantidad_documentos
    """, (
        id_paciente,
        id_paciente,
        id_paciente,
        id_paciente
    ))

    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    total_relaciones = (
        resultado["cantidad_citas"]
        + resultado["cantidad_tratamientos"]
        + resultado["cantidad_presupuestos"]
        + resultado["cantidad_documentos"]
    )

    return total_relaciones > 0


def eliminar_paciente(id_paciente):
    """
    Solo elimina al paciente si no posee información relacionada.
    Retorna True cuando se elimina y False cuando no corresponde.
    """

    if paciente_tiene_informacion_asociada(id_paciente):
        return False

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM pacientes
        WHERE id_paciente = %s
    """, (id_paciente,))

    conexion.commit()

    cursor.close()
    conexion.close()

    return True