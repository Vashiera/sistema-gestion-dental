from flask import render_template, request, redirect, url_for

from models.paciente import (
    obtener_pacientes,
    crear_paciente,
    obtener_paciente_por_id,
    actualizar_paciente,
    cambiar_estado_paciente,
    eliminar_paciente
)

from models.cita import obtener_citas_por_paciente

from models.tratamiento import (
    obtener_tratamientos_por_paciente,
    obtener_plan_agrupado_por_paciente
)

from models.documento import (
    obtener_documentos_por_paciente
)

from models.pago import (
    obtener_estado_cuenta_paciente,
    obtener_pagos_por_paciente
)

from models.evolucion import (
    obtener_evoluciones_por_paciente
)


def registrar_pacientes(app):

    @app.route("/pacientes")
    def pacientes():
        lista_pacientes = obtener_pacientes()

        mensaje = request.args.get("mensaje")
        tipo_mensaje = request.args.get("tipo")

        return render_template(
            "pacientes/pacientes.html",
            pacientes=lista_pacientes,
            paciente_editar=None,
            mensaje=mensaje,
            tipo_mensaje=tipo_mensaje
        )


    @app.route("/pacientes/crear", methods=["POST"])
    def crear_paciente_route():
        crear_paciente(
            request.form["rut"],
            request.form["nombre"],
            request.form["apellido"],
            request.form["telefono"],
            request.form["correo"],
            request.form["direccion"],
            request.form["fecha_nacimiento"]
        )

        return redirect(
            url_for(
                "pacientes",
                mensaje="Paciente registrado correctamente.",
                tipo="exito"
            )
        )


    @app.route("/pacientes/editar/<int:id>")
    def editar_paciente(id):
        paciente = obtener_paciente_por_id(id)
        lista_pacientes = obtener_pacientes()

        if paciente is None:
            return redirect(
                url_for(
                    "pacientes",
                    mensaje="El paciente solicitado no existe.",
                    tipo="error"
                )
            )

        return render_template(
            "pacientes/pacientes.html",
            pacientes=lista_pacientes,
            paciente_editar=paciente,
            mensaje=None,
            tipo_mensaje=None
        )


    @app.route(
        "/pacientes/actualizar/<int:id>",
        methods=["POST"]
    )
    def actualizar_paciente_route(id):
        paciente = obtener_paciente_por_id(id)

        if paciente is None:
            return redirect(
                url_for(
                    "pacientes",
                    mensaje="El paciente solicitado no existe.",
                    tipo="error"
                )
            )

        actualizar_paciente(
            id,
            request.form["rut"],
            request.form["nombre"],
            request.form["apellido"],
            request.form["telefono"],
            request.form["correo"],
            request.form["direccion"],
            request.form["fecha_nacimiento"]
        )

        return redirect(
            url_for(
                "pacientes",
                mensaje="Paciente actualizado correctamente.",
                tipo="exito"
            )
        )


    @app.route(
        "/pacientes/cambiar-estado/<int:id>",
        methods=["POST"]
    )
    def cambiar_estado_paciente_route(id):
        paciente = obtener_paciente_por_id(id)

        if paciente is None:
            return redirect(
                url_for(
                    "pacientes",
                    mensaje="El paciente solicitado no existe.",
                    tipo="error"
                )
            )

        nuevo_estado = (
            "INACTIVO"
            if paciente["estado"] == "ACTIVO"
            else "ACTIVO"
        )

        cambiar_estado_paciente(
            id,
            nuevo_estado
        )

        accion = (
            "desactivado"
            if nuevo_estado == "INACTIVO"
            else "activado"
        )

        return redirect(
            url_for(
                "pacientes",
                mensaje=f"Paciente {accion} correctamente.",
                tipo="exito"
            )
        )


    @app.route(
        "/pacientes/eliminar/<int:id>",
        methods=["POST"]
    )
    def eliminar_paciente_route(id):
        paciente = obtener_paciente_por_id(id)

        if paciente is None:
            return redirect(
                url_for(
                    "pacientes",
                    mensaje="El paciente solicitado no existe.",
                    tipo="error"
                )
            )

        eliminado = eliminar_paciente(id)

        if not eliminado:
            return redirect(
                url_for(
                    "pacientes",
                    mensaje=(
                        "No se puede eliminar el paciente porque tiene "
                        "citas, tratamientos, presupuestos, pagos, "
                        "documentos o evoluciones asociadas. "
                        "Puedes desactivarlo."
                    ),
                    tipo="error"
                )
            )

        return redirect(
            url_for(
                "pacientes",
                mensaje="Paciente eliminado definitivamente.",
                tipo="exito"
            )
        )


    @app.route("/ficha-paciente/<int:id>")
    def ficha_paciente(id):
        paciente = obtener_paciente_por_id(id)

        if paciente is None:
            return redirect(
                url_for(
                    "pacientes",
                    mensaje="El paciente solicitado no existe.",
                    tipo="error"
                )
            )

        citas = obtener_citas_por_paciente(id)

        tratamientos = obtener_tratamientos_por_paciente(
            id
        )

        plan_agrupado = obtener_plan_agrupado_por_paciente(
            id
        )

        documentos = obtener_documentos_por_paciente(
            id
        )

        cuenta = obtener_estado_cuenta_paciente(
            id
        )

        pagos = obtener_pagos_por_paciente(
            id
        )

        evoluciones = obtener_evoluciones_por_paciente(
            id
        )

        total_tratamientos = sum(
            tratamiento["valor_presupuestado"] or 0
            for tratamiento in tratamientos
        )

        cantidad_planificados = sum(
            1
            for tratamiento in tratamientos
            if tratamiento["estado"] == "PLANIFICADO"
        )

        cantidad_en_proceso = sum(
            1
            for tratamiento in tratamientos
            if tratamiento["estado"] == "EN PROCESO"
        )

        cantidad_finalizados = sum(
            1
            for tratamiento in tratamientos
            if tratamiento["estado"] == "FINALIZADO"
        )

        return render_template(
            "pacientes/ficha-paciente.html",
            paciente=paciente,
            citas=citas,
            tratamientos=tratamientos,
            plan_agrupado=plan_agrupado,
            documentos=documentos,
            cuenta=cuenta,
            pagos=pagos,
            evoluciones=evoluciones,
            total_tratamientos=total_tratamientos,
            cantidad_planificados=cantidad_planificados,
            cantidad_en_proceso=cantidad_en_proceso,
            cantidad_finalizados=cantidad_finalizados
        )