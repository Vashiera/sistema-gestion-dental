import json

from flask import render_template, request, redirect, url_for

from models.tratamiento import (
    crear_plan_tratamientos,
    obtener_tratamiento_por_id,
    actualizar_tratamiento,
    obtener_tratamientos_por_paciente,
    obtener_plan_agrupado_por_paciente
)

from models.paciente import (
    obtener_lista_pacientes,
    obtener_paciente_por_id
)

from models.catalogo_tratamiento import (
    obtener_catalogo_tratamientos
)


def registrar_tratamientos(app):

    def cargar_tratamientos(
        tratamiento_editar=None,
        mensaje=None,
        error=None,
        id_paciente=None
    ):
        paciente_seleccionado = None
        tratamientos_paciente = []
        plan_agrupado = None

        if id_paciente:
            paciente_seleccionado = obtener_paciente_por_id(
                id_paciente
            )

            if paciente_seleccionado:
                tratamientos_paciente = (
                    obtener_tratamientos_por_paciente(
                        id_paciente
                    )
                )

                plan_agrupado = (
                    obtener_plan_agrupado_por_paciente(
                        id_paciente
                    )
                )

        cantidad_planificados = sum(
            1
            for tratamiento in tratamientos_paciente
            if tratamiento["estado"] == "PLANIFICADO"
        )

        cantidad_en_proceso = sum(
            1
            for tratamiento in tratamientos_paciente
            if tratamiento["estado"] == "EN PROCESO"
        )

        cantidad_finalizados = sum(
            1
            for tratamiento in tratamientos_paciente
            if tratamiento["estado"] == "FINALIZADO"
        )

        return render_template(
            "tratamientos/tratamientos.html",
            pacientes=obtener_lista_pacientes(),
            catalogo=obtener_catalogo_tratamientos(),
            paciente_seleccionado=paciente_seleccionado,
            tratamientos=tratamientos_paciente,
            plan_agrupado=plan_agrupado,
            tratamiento_editar=tratamiento_editar,
            cantidad_planificados=cantidad_planificados,
            cantidad_en_proceso=cantidad_en_proceso,
            cantidad_finalizados=cantidad_finalizados,
            mensaje=mensaje,
            error=error
        )


    # -------------------------------------------------
    # CONSULTAR PLAN DE UN PACIENTE
    # -------------------------------------------------

    @app.route("/tratamientos")
    def tratamientos():

        id_paciente = request.args.get(
            "id_paciente",
            type=int
        )

        return cargar_tratamientos(
            id_paciente=id_paciente,
            mensaje=request.args.get("mensaje"),
            error=request.args.get("error")
        )


    # -------------------------------------------------
    # CREAR PLAN COMPLETO
    # -------------------------------------------------

    @app.route("/tratamientos/crear", methods=["POST"])
    def crear_tratamiento_route():

        id_paciente = request.form.get(
            "id_paciente",
            ""
        ).strip()

        tratamientos_json = request.form.get(
            "tratamientos_json",
            ""
        ).strip()

        if not id_paciente:
            return cargar_tratamientos(
                error="Debe seleccionar un paciente."
            )

        paciente = obtener_paciente_por_id(id_paciente)

        if paciente is None:
            return cargar_tratamientos(
                error="El paciente seleccionado no existe."
            )

        if not tratamientos_json:
            return cargar_tratamientos(
                id_paciente=int(id_paciente),
                error=(
                    "Debe agregar al menos un procedimiento "
                    "al plan de tratamiento."
                )
            )

        try:
            lista_tratamientos = json.loads(
                tratamientos_json
            )

        except json.JSONDecodeError:
            return cargar_tratamientos(
                id_paciente=int(id_paciente),
                error=(
                    "No fue posible procesar los procedimientos "
                    "agregados al plan."
                )
            )

        if not isinstance(lista_tratamientos, list):
            return cargar_tratamientos(
                id_paciente=int(id_paciente),
                error=(
                    "El contenido del plan de tratamiento "
                    "no es válido."
                )
            )

        if len(lista_tratamientos) == 0:
            return cargar_tratamientos(
                id_paciente=int(id_paciente),
                error=(
                    "Debe agregar al menos un procedimiento "
                    "al plan de tratamiento."
                )
            )

        registrado, mensaje = crear_plan_tratamientos(
            id_paciente,
            1,  # Temporal: usuario autenticado
            lista_tratamientos
        )

        if not registrado:
            return cargar_tratamientos(
                id_paciente=int(id_paciente),
                error=mensaje
            )

        return redirect(
            url_for(
                "tratamientos",
                id_paciente=id_paciente,
                mensaje=mensaje
            )
        )


    # -------------------------------------------------
    # CARGAR TRATAMIENTO PARA EDITAR
    # -------------------------------------------------

    @app.route("/tratamientos/editar/<int:id>")
    def editar_tratamiento(id):

        tratamiento = obtener_tratamiento_por_id(id)

        if tratamiento is None:
            return redirect(
                url_for(
                    "tratamientos",
                    error="El tratamiento solicitado no existe."
                )
            )

        return cargar_tratamientos(
            tratamiento_editar=tratamiento,
            id_paciente=tratamiento["id_paciente"]
        )


    # -------------------------------------------------
    # ACTUALIZAR TRATAMIENTO INDIVIDUAL
    # -------------------------------------------------

    @app.route(
        "/tratamientos/actualizar/<int:id>",
        methods=["POST"]
    )
    def actualizar_tratamiento_route(id):

        tratamiento_actual = obtener_tratamiento_por_id(id)

        if tratamiento_actual is None:
            return redirect(
                url_for(
                    "tratamientos",
                    error="El tratamiento solicitado no existe."
                )
            )

        id_paciente = request.form.get(
            "id_paciente",
            ""
        ).strip()

        id_catalogo = request.form.get(
            "id_catalogo",
            ""
        ).strip()

        pieza_dental = request.form.get(
            "pieza_dental",
            ""
        ).strip()

        descripcion = request.form.get(
            "descripcion",
            ""
        ).strip()

        valor_presupuestado = request.form.get(
            "valor_presupuestado",
            ""
        ).strip()

        estado = request.form.get(
            "estado",
            ""
        ).strip()

        tratamiento_temporal = {
            "id_tratamiento": id,
            "id_paciente": id_paciente,
            "id_catalogo": id_catalogo,
            "pieza_dental": pieza_dental,
            "descripcion": descripcion,
            "valor_presupuestado": valor_presupuestado,
            "estado": estado
        }

        if not id_paciente:
            return cargar_tratamientos(
                tratamiento_editar=tratamiento_temporal,
                error="No fue posible identificar al paciente."
            )

        if not id_catalogo:
            return cargar_tratamientos(
                tratamiento_editar=tratamiento_temporal,
                id_paciente=int(id_paciente),
                error="Debe seleccionar un procedimiento."
            )

        if valor_presupuestado == "":
            return cargar_tratamientos(
                tratamiento_editar=tratamiento_temporal,
                id_paciente=int(id_paciente),
                error="Debe ingresar un valor presupuestado."
            )

        try:
            valor_numerico = float(valor_presupuestado)

        except ValueError:
            return cargar_tratamientos(
                tratamiento_editar=tratamiento_temporal,
                id_paciente=int(id_paciente),
                error="El valor ingresado no es válido."
            )

        if valor_numerico < 0:
            return cargar_tratamientos(
                tratamiento_editar=tratamiento_temporal,
                id_paciente=int(id_paciente),
                error="El valor no puede ser negativo."
            )

        if estado not in {
            "PLANIFICADO",
            "EN PROCESO",
            "FINALIZADO"
        }:
            return cargar_tratamientos(
                tratamiento_editar=tratamiento_temporal,
                id_paciente=int(id_paciente),
                error="El estado seleccionado no es válido."
            )

        actualizar_tratamiento(
            id,
            id_paciente,
            id_catalogo,
            pieza_dental,
            descripcion,
            valor_presupuestado,
            estado
        )

        return redirect(
            url_for(
                "tratamientos",
                id_paciente=id_paciente,
                mensaje="Tratamiento actualizado correctamente."
            )
        )


    # -------------------------------------------------
    # DETALLE INDIVIDUAL
    # -------------------------------------------------

    @app.route("/tratamiento/<int:id>")
    def tratamiento(id):

        tratamiento_encontrado = obtener_tratamiento_por_id(id)

        if tratamiento_encontrado is None:
            return redirect(
                url_for(
                    "tratamientos",
                    error="El tratamiento solicitado no existe."
                )
            )

        return render_template(
            "tratamientos/tratamiento.html",
            tratamiento=tratamiento_encontrado
        )