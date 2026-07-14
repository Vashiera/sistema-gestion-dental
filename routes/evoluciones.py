from flask import render_template, request, redirect, url_for

from models.evolucion import (
    obtener_evolucion_por_id,
    obtener_evoluciones_por_paciente,
    crear_evolucion,
    actualizar_evolucion
)

from models.tratamiento import (
    obtener_tratamientos_por_paciente,
    obtener_tratamiento_por_id
)

from models.paciente import (
    obtener_lista_pacientes,
    obtener_paciente_por_id
)

from models.usuario import obtener_odontologos


def registrar_evoluciones(app):

    def cargar_evoluciones(
        id_paciente=None,
        evolucion_editar=None,
        mensaje=None,
        error=None
    ):
        paciente_seleccionado = None
        tratamientos = []
        evoluciones = []

        if id_paciente:
            paciente_seleccionado = obtener_paciente_por_id(
                id_paciente
            )

            if paciente_seleccionado:
                tratamientos = obtener_tratamientos_por_paciente(
                    id_paciente
                )

                evoluciones = obtener_evoluciones_por_paciente(
                    id_paciente
                )

        return render_template(
            "evoluciones/evoluciones.html",
            pacientes=obtener_lista_pacientes(),
            paciente_seleccionado=paciente_seleccionado,
            tratamientos=tratamientos,
            evoluciones=evoluciones,
            odontologos=obtener_odontologos(),
            evolucion_editar=evolucion_editar,
            mensaje=mensaje,
            error=error
        )


    # -------------------------------------------------
    # CONSULTAR HISTORIAL DE UN PACIENTE
    # -------------------------------------------------

    @app.route("/evoluciones")
    def evoluciones():
        id_paciente = request.args.get(
            "id_paciente",
            type=int
        )

        return cargar_evoluciones(
            id_paciente=id_paciente,
            mensaje=request.args.get("mensaje"),
            error=request.args.get("error")
        )


    # -------------------------------------------------
    # CREAR EVOLUCIÓN
    # -------------------------------------------------

    @app.route("/evoluciones/crear", methods=["POST"])
    def crear_evolucion_route():

        id_paciente = request.form.get(
            "id_paciente",
            ""
        ).strip()

        id_tratamiento = request.form.get(
            "id_tratamiento",
            ""
        ).strip()

        id_usuario = request.form.get(
            "id_usuario",
            ""
        ).strip()

        fecha = request.form.get(
            "fecha",
            ""
        ).strip()

        procedimiento_realizado = request.form.get(
            "procedimiento_realizado",
            ""
        ).strip()

        observaciones = request.form.get(
            "observaciones",
            ""
        ).strip()

        if not id_paciente:
            return cargar_evoluciones(
                error="Debe seleccionar un paciente."
            )

        paciente = obtener_paciente_por_id(id_paciente)

        if paciente is None:
            return cargar_evoluciones(
                error="El paciente seleccionado no existe."
            )

        if not id_tratamiento:
            return cargar_evoluciones(
                id_paciente=int(id_paciente),
                error="Debe seleccionar un tratamiento."
            )

        tratamiento = obtener_tratamiento_por_id(
            id_tratamiento
        )

        if tratamiento is None:
            return cargar_evoluciones(
                id_paciente=int(id_paciente),
                error="El tratamiento seleccionado no existe."
            )

        if int(tratamiento["id_paciente"]) != int(id_paciente):
            return cargar_evoluciones(
                id_paciente=int(id_paciente),
                error=(
                    "El tratamiento seleccionado no pertenece "
                    "al paciente indicado."
                )
            )

        if not id_usuario:
            return cargar_evoluciones(
                id_paciente=int(id_paciente),
                error="Debe seleccionar un profesional."
            )

        if not fecha:
            return cargar_evoluciones(
                id_paciente=int(id_paciente),
                error="Debe ingresar la fecha de la evolución."
            )

        if not procedimiento_realizado:
            return cargar_evoluciones(
                id_paciente=int(id_paciente),
                error=(
                    "Debe indicar el procedimiento realizado "
                    "durante la atención."
                )
            )

        crear_evolucion(
            id_tratamiento,
            id_usuario,
            fecha,
            procedimiento_realizado,
            observaciones
        )

        return redirect(
            url_for(
                "evoluciones",
                id_paciente=id_paciente,
                mensaje=(
                    "Evolución clínica registrada correctamente."
                )
            )
        )


    # -------------------------------------------------
    # CARGAR EVOLUCIÓN PARA EDITAR
    # -------------------------------------------------

    @app.route("/evoluciones/editar/<int:id>")
    def editar_evolucion(id):

        evolucion = obtener_evolucion_por_id(id)

        if evolucion is None:
            return redirect(
                url_for(
                    "evoluciones",
                    error="La evolución solicitada no existe."
                )
            )

        return cargar_evoluciones(
            id_paciente=evolucion["id_paciente"],
            evolucion_editar=evolucion
        )


    # -------------------------------------------------
    # ACTUALIZAR EVOLUCIÓN
    # -------------------------------------------------

    @app.route(
        "/evoluciones/actualizar/<int:id>",
        methods=["POST"]
    )
    def actualizar_evolucion_route(id):

        evolucion_actual = obtener_evolucion_por_id(id)

        if evolucion_actual is None:
            return redirect(
                url_for(
                    "evoluciones",
                    error="La evolución solicitada no existe."
                )
            )

        id_paciente = request.form.get(
            "id_paciente",
            ""
        ).strip()

        id_tratamiento = request.form.get(
            "id_tratamiento",
            ""
        ).strip()

        id_usuario = request.form.get(
            "id_usuario",
            ""
        ).strip()

        fecha = request.form.get(
            "fecha",
            ""
        ).strip()

        procedimiento_realizado = request.form.get(
            "procedimiento_realizado",
            ""
        ).strip()

        observaciones = request.form.get(
            "observaciones",
            ""
        ).strip()

        evolucion_temporal = {
            "id_evolucion": id,
            "id_paciente": id_paciente,
            "id_tratamiento": id_tratamiento,
            "id_usuario": id_usuario,
            "fecha": fecha,
            "procedimiento_realizado": procedimiento_realizado,
            "observaciones": observaciones
        }

        if not id_paciente:
            return cargar_evoluciones(
                evolucion_editar=evolucion_temporal,
                error="No fue posible identificar al paciente."
            )

        if not id_tratamiento:
            return cargar_evoluciones(
                id_paciente=int(id_paciente),
                evolucion_editar=evolucion_temporal,
                error="Debe seleccionar un tratamiento."
            )

        tratamiento = obtener_tratamiento_por_id(
            id_tratamiento
        )

        if tratamiento is None:
            return cargar_evoluciones(
                id_paciente=int(id_paciente),
                evolucion_editar=evolucion_temporal,
                error="El tratamiento seleccionado no existe."
            )

        if int(tratamiento["id_paciente"]) != int(id_paciente):
            return cargar_evoluciones(
                id_paciente=int(id_paciente),
                evolucion_editar=evolucion_temporal,
                error=(
                    "El tratamiento seleccionado no pertenece "
                    "al paciente indicado."
                )
            )

        if not id_usuario:
            return cargar_evoluciones(
                id_paciente=int(id_paciente),
                evolucion_editar=evolucion_temporal,
                error="Debe seleccionar un profesional."
            )

        if not fecha:
            return cargar_evoluciones(
                id_paciente=int(id_paciente),
                evolucion_editar=evolucion_temporal,
                error="Debe ingresar la fecha de la evolución."
            )

        if not procedimiento_realizado:
            return cargar_evoluciones(
                id_paciente=int(id_paciente),
                evolucion_editar=evolucion_temporal,
                error=(
                    "Debe indicar el procedimiento realizado "
                    "durante la atención."
                )
            )

        actualizar_evolucion(
            id,
            id_tratamiento,
            id_usuario,
            fecha,
            procedimiento_realizado,
            observaciones
        )

        return redirect(
            url_for(
                "evoluciones",
                id_paciente=id_paciente,
                mensaje=(
                    "Evolución clínica actualizada correctamente."
                )
            )
        )