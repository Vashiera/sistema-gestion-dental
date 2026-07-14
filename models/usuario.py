from mysql.connector import IntegrityError

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database.conexion import obtener_conexion


def formatear_rut_usuario(rut):
    rut_limpio = (
        rut.replace(".", "")
        .replace("-", "")
        .replace(" ", "")
        .upper()
        .strip()
    )

    if len(rut_limpio) < 2:
        return rut_limpio

    cuerpo = rut_limpio[:-1]
    digito_verificador = rut_limpio[-1]

    grupos = []

    while cuerpo:
        grupos.insert(0, cuerpo[-3:])
        cuerpo = cuerpo[:-3]

    cuerpo_formateado = ".".join(grupos)

    return f"{cuerpo_formateado}-{digito_verificador}"


def obtener_odontologos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            u.id_usuario,
            u.rut,
            u.nombre
        FROM usuarios u
        INNER JOIN roles r
            ON u.id_rol = r.id_rol
        WHERE r.nombre_rol = 'Odontólogo'
        AND u.estado = 'ACTIVO'
        ORDER BY u.nombre
    """)

    odontologos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return odontologos


def obtener_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            u.id_usuario,
            u.rut,
            u.nombre,
            u.correo,
            u.estado,
            u.id_rol,
            r.nombre_rol
        FROM usuarios u
        INNER JOIN roles r
            ON u.id_rol = r.id_rol
        ORDER BY u.nombre
    """)

    usuarios = cursor.fetchall()

    cursor.close()
    conexion.close()

    return usuarios


def obtener_usuario_por_rut(rut):
    rut = formatear_rut_usuario(rut)

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            u.id_usuario,
            u.rut,
            u.nombre,
            u.correo,
            u.password_hash,
            u.id_rol,
            u.estado,
            r.nombre_rol
        FROM usuarios u
        INNER JOIN roles r
            ON u.id_rol = r.id_rol
        WHERE u.rut = %s
        LIMIT 1
    """, (rut,))

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    return usuario


def obtener_usuario_por_id(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            u.id_usuario,
            u.rut,
            u.nombre,
            u.correo,
            u.id_rol,
            u.estado,
            r.nombre_rol
        FROM usuarios u
        INNER JOIN roles r
            ON u.id_rol = r.id_rol
        WHERE u.id_usuario = %s
    """, (id_usuario,))

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    return usuario


def obtener_roles():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id_rol,
            nombre_rol
        FROM roles
        ORDER BY nombre_rol
    """)

    roles = cursor.fetchall()

    cursor.close()
    conexion.close()

    return roles


def crear_usuario(
    rut,
    nombre,
    correo,
    password,
    id_rol,
    estado
):
    rut = formatear_rut_usuario(rut)
    nombre = nombre.strip().title()
    correo = correo.strip().lower()
    password_hash = generate_password_hash(password)

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios (
                rut,
                nombre,
                correo,
                password_hash,
                id_rol,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            rut,
            nombre,
            correo,
            password_hash,
            id_rol,
            estado
        ))

        conexion.commit()

        return (
            True,
            "Usuario creado correctamente."
        )

    except IntegrityError as error:
        conexion.rollback()

        mensaje_error = str(error).lower()

        if "rut" in mensaje_error:
            return (
                False,
                "Ya existe un usuario registrado con ese RUT."
            )

        if "correo" in mensaje_error:
            return (
                False,
                "Ya existe un usuario registrado con ese correo."
            )

        return (
            False,
            "No fue posible crear el usuario."
        )

    finally:
        cursor.close()
        conexion.close()


def validar_credenciales_usuario(rut, password):
    usuario = obtener_usuario_por_rut(rut)

    if usuario is None:
        return None

    if usuario["estado"] != "ACTIVO":
        return None

    try:
        password_correcta = check_password_hash(
            usuario["password_hash"],
            password
        )
    except (ValueError, TypeError):
        return None

    if not password_correcta:
        return None

    return usuario


def actualizar_password_usuario(id_usuario, nueva_password):
    password_hash = generate_password_hash(
        nueva_password
    )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET password_hash = %s
        WHERE id_usuario = %s
    """, (
        password_hash,
        id_usuario
    ))

    conexion.commit()

    actualizado = cursor.rowcount > 0

    cursor.close()
    conexion.close()

    return actualizado