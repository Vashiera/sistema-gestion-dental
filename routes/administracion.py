from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session
)

from models.usuario import (
    obtener_usuarios,
    obtener_roles,
    crear_usuario,
    obtener_usuario_por_id,
    actualizar_password_usuario
)


def registrar_administracion(app):

    def usuario_es_administrador():
        return (
            session.get("nombre_rol") == "Administrador"
        )


    @app.route("/administracion")
    def administracion():

        if not session.get("id_usuario"):
            return redirect(
                url_for("login")
            )

        if not usuario_es_administrador():
            return redirect(
                url_for("dashboard")
            )

        return render_template(
            "administracion/administracion.html",
            usuarios=obtener_usuarios(),
            roles=obtener_roles(),
            mensaje=request.args.get("mensaje"),
            error=request.args.get("error"),
            usuario_restablecer=None
        )


    @app.route(
        "/administracion/usuarios/crear",
        methods=["POST"]
    )
    def crear_usuario_route():

        if not session.get("id_usuario"):
            return redirect(
                url_for("login")
            )

        if not usuario_es_administrador():
            return redirect(
                url_for("dashboard")
            )

        rut = request.form.get(
            "rut",
            ""
        ).strip()

        nombre = request.form.get(
            "nombre",
            ""
        ).strip()

        correo = request.form.get(
            "correo",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        id_rol = request.form.get(
            "id_rol",
            ""
        ).strip()

        estado = request.form.get(
            "estado",
            ""
        ).strip()

        if not rut:
            return redirect(
                url_for(
                    "administracion",
                    error="Debe ingresar el RUT del usuario."
                )
            )

        if not nombre:
            return redirect(
                url_for(
                    "administracion",
                    error="Debe ingresar el nombre del usuario."
                )
            )

        if not correo:
            return redirect(
                url_for(
                    "administracion",
                    error="Debe ingresar el correo electrónico."
                )
            )

        if len(password) < 6:
            return redirect(
                url_for(
                    "administracion",
                    error=(
                        "La contraseña debe tener al menos "
                        "6 caracteres."
                    )
                )
            )

        if not id_rol:
            return redirect(
                url_for(
                    "administracion",
                    error="Debe seleccionar un rol."
                )
            )

        if estado not in {
            "ACTIVO",
            "INACTIVO"
        }:
            return redirect(
                url_for(
                    "administracion",
                    error="El estado seleccionado no es válido."
                )
            )

        creado, mensaje = crear_usuario(
            rut,
            nombre,
            correo,
            password,
            id_rol,
            estado
        )

        if not creado:
            return redirect(
                url_for(
                    "administracion",
                    error=mensaje
                )
            )

        return redirect(
            url_for(
                "administracion",
                mensaje=mensaje
            )
        )


    @app.route(
        "/administracion/usuarios/restablecer/<int:id>"
    )
    def mostrar_restablecer_password(id):

        if not session.get("id_usuario"):
            return redirect(
                url_for("login")
            )

        if not usuario_es_administrador():
            return redirect(
                url_for("dashboard")
            )

        usuario = obtener_usuario_por_id(id)

        if usuario is None:
            return redirect(
                url_for(
                    "administracion",
                    error="El usuario solicitado no existe."
                )
            )

        return render_template(
            "administracion/administracion.html",
            usuarios=obtener_usuarios(),
            roles=obtener_roles(),
            mensaje=request.args.get("mensaje"),
            error=request.args.get("error"),
            usuario_restablecer=usuario
        )


    @app.route(
        "/administracion/usuarios/restablecer/<int:id>",
        methods=["POST"]
    )
    def restablecer_password_route(id):

        if not session.get("id_usuario"):
            return redirect(
                url_for("login")
            )

        if not usuario_es_administrador():
            return redirect(
                url_for("dashboard")
            )

        usuario = obtener_usuario_por_id(id)

        if usuario is None:
            return redirect(
                url_for(
                    "administracion",
                    error="El usuario solicitado no existe."
                )
            )

        nueva_password = request.form.get(
            "nueva_password",
            ""
        )

        confirmar_password = request.form.get(
            "confirmar_password",
            ""
        )

        if len(nueva_password) < 6:
            return redirect(
                url_for(
                    "mostrar_restablecer_password",
                    id=id,
                    error=(
                        "La nueva contraseña debe tener "
                        "al menos 6 caracteres."
                    )
                )
            )

        if nueva_password != confirmar_password:
            return redirect(
                url_for(
                    "mostrar_restablecer_password",
                    id=id,
                    error=(
                        "Las contraseñas ingresadas "
                        "no coinciden."
                    )
                )
            )

        actualizado = actualizar_password_usuario(
            id,
            nueva_password
        )

        if not actualizado:
            return redirect(
                url_for(
                    "administracion",
                    error=(
                        "No fue posible restablecer "
                        "la contraseña."
                    )
                )
            )

        return redirect(
            url_for(
                "administracion",
                mensaje=(
                    f"Contraseña de {usuario['nombre']} "
                    "restablecida correctamente."
                )
            )
        )