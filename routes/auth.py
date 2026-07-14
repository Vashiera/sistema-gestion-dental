from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session
)

from models.usuario import validar_credenciales_usuario


def registrar_auth(app):

    @app.route("/")
    def login():
        if session.get("id_usuario"):
            return redirect(url_for("dashboard"))

        return render_template(
            "index.html",
            error=request.args.get("error")
        )


    @app.route(
        "/iniciar-sesion",
        methods=["POST"]
    )
    def iniciar_sesion():
        rut = request.form.get(
            "rut",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if not rut or not password:
            return render_template(
                "index.html",
                error="Debe ingresar su RUT y contraseña.",
                rut_ingresado=rut
            )

        usuario = validar_credenciales_usuario(
            rut,
            password
        )

        if usuario is None:
            return render_template(
                "index.html",
                error=(
                    "El RUT o la contraseña son incorrectos, "
                    "o el usuario se encuentra inactivo."
                ),
                rut_ingresado=rut
            )

        session.clear()

        session["id_usuario"] = usuario["id_usuario"]
        session["rut_usuario"] = usuario["rut"]
        session["nombre_usuario"] = usuario["nombre"]
        session["correo_usuario"] = usuario["correo"]
        session["id_rol"] = usuario["id_rol"]
        session["nombre_rol"] = usuario["nombre_rol"]

        # Compatibilidad temporal con topbar y código antiguo.
        session["usuario"] = usuario["nombre"]
        session["rol"] = usuario["nombre_rol"]

        return redirect(
            url_for("dashboard")
        )


    @app.route("/cerrar-sesion")
    def cerrar_sesion():
        session.clear()

        return redirect(
            url_for("login")
        )