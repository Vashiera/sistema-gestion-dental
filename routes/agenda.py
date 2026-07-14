from datetime import date, datetime, timedelta

from flask import render_template, request, redirect, url_for

from models.usuario import obtener_odontologos

from models.cita import (
    obtener_citas_por_fecha,
    obtener_cita_por_id,
    crear_cita,
    actualizar_cita,
    cancelar_cita,
    existe_cita_en_horario
)

from models.paciente import obtener_lista_pacientes


HORARIOS_AGENDA = [
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "12:00",
    "12:30",
    "14:00",
    "14:30",
    "15:00",
    "15:30",
    "16:00",
    "16:30",
    "17:00",
    "17:30"
]


def convertir_fecha(fecha_texto):
    try:
        return datetime.strptime(
            fecha_texto,
            "%Y-%m-%d"
        ).date()

    except (TypeError, ValueError):
        return date.today()


def formatear_fecha_espanol(fecha_objeto):
    dias = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo"
    ]

    meses = [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre"
    ]

    return (
        f"{dias[fecha_objeto.weekday()]} "
        f"{fecha_objeto.day} de "
        f"{meses[fecha_objeto.month - 1]} de "
        f"{fecha_objeto.year}"
    )


def construir_matriz_agenda(
    fecha_objeto,
    horarios,
    odontologos,
    citas
):
    """
    Crea una celda por profesional y horario.

    """

    matriz = {}

    for odontologo in odontologos:
        id_usuario = odontologo["id_usuario"]
        matriz[id_usuario] = {}

        citas_profesional = [
            cita
            for cita in citas
            if int(cita["id_usuario"]) == int(id_usuario)
        ]

        for horario in horarios:
            hora_slot = datetime.strptime(
                horario,
                "%H:%M"
            ).time()

            fecha_hora_slot = datetime.combine(
                fecha_objeto,
                hora_slot
            )

            celda = None

            for cita in citas_profesional:
                if cita["estado"] == "CANCELADA":
                    continue

                hora_inicio = datetime.strptime(
                    cita["hora"],
                    "%H:%M"
                ).time()

                inicio = datetime.combine(
                    fecha_objeto,
                    hora_inicio
                )

                termino = inicio + timedelta(
                    minutes=int(cita["duracion_minutos"])
                )

                if inicio <= fecha_hora_slot < termino:
                    celda = {
                        "cita": cita,
                        "es_inicio": (
                            fecha_hora_slot == inicio
                        ),
                        "es_cancelada": False,
                        "hora_termino": termino.strftime(
                            "%H:%M"
                        )
                    }
                    break

            if celda is None:
                for cita in citas_profesional:
                    if (
                        cita["estado"] == "CANCELADA"
                        and cita["hora"] == horario
                    ):
                        celda = {
                            "cita": cita,
                            "es_inicio": True,
                            "es_cancelada": True,
                            "hora_termino": None
                        }
                        break

            matriz[id_usuario][horario] = celda

    return matriz


def registrar_agenda(app):

    def cargar_agenda(
        fecha=None,
        error=None,
        mensaje=None,
        cita_editar=None
    ):
        fecha_objeto = convertir_fecha(
            fecha or date.today().isoformat()
        )

        fecha_seleccionada = fecha_objeto.isoformat()

        odontologos = obtener_odontologos()

        citas = obtener_citas_por_fecha(
            fecha_seleccionada
        )

        matriz_agenda = construir_matriz_agenda(
            fecha_objeto,
            HORARIOS_AGENDA,
            odontologos,
            citas
        )

        return render_template(
            "agenda/agenda.html",
            citas=citas,
            pacientes=obtener_lista_pacientes(),
            odontologos=odontologos,
            horarios=HORARIOS_AGENDA,
            agenda_matriz=matriz_agenda,
            fecha_seleccionada=fecha_seleccionada,
            fecha_formateada=formatear_fecha_espanol(
                fecha_objeto
            ),
            fecha_anterior=(
                fecha_objeto - timedelta(days=1)
            ).isoformat(),
            fecha_siguiente=(
                fecha_objeto + timedelta(days=1)
            ).isoformat(),
            fecha_hoy=date.today().isoformat(),
            error=error,
            mensaje=mensaje,
            cita_editar=cita_editar
        )


    # -------------------------------------------------
    # AGENDA DIARIA
    # -------------------------------------------------

    @app.route("/agenda")
    def agenda():
        fecha_seleccionada = request.args.get(
            "fecha",
            date.today().isoformat()
        )

        return cargar_agenda(
            fecha=fecha_seleccionada,
            mensaje=request.args.get("mensaje"),
            error=request.args.get("error"),
            cita_editar=None
        )


    # -------------------------------------------------
    # CREAR CITA
    # -------------------------------------------------

    @app.route("/agenda/crear", methods=["POST"])
    def crear_cita_route():
        id_paciente = request.form["id_paciente"]
        id_usuario = request.form["id_usuario"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]

        duracion_minutos = int(
            request.form["duracion_minutos"]
        )

        motivo = request.form["motivo"]
        estado = request.form["estado"]

        if estado != "CANCELADA":
            horario_ocupado = existe_cita_en_horario(
                id_usuario,
                fecha,
                hora,
                duracion_minutos
            )

            if horario_ocupado:
                return cargar_agenda(
                    fecha=fecha,
                    error=(
                        "El horario seleccionado se cruza con otra "
                        "cita del mismo profesional."
                    ),
                    cita_editar=None
                )

        crear_cita(
            id_paciente,
            id_usuario,
            fecha,
            hora,
            duracion_minutos,
            motivo,
            estado
        )

        return redirect(
            url_for(
                "agenda",
                fecha=fecha,
                mensaje="Cita registrada correctamente."
            )
        )


    # -------------------------------------------------
    # CARGAR CITA PARA EDITAR
    # -------------------------------------------------

    @app.route("/agenda/editar/<int:id>")
    def editar_cita(id):
        cita = obtener_cita_por_id(id)

        if cita is None:
            return redirect(
                url_for(
                    "agenda",
                    error="La cita solicitada no existe."
                )
            )

        return cargar_agenda(
            fecha=cita["fecha"],
            cita_editar=cita
        )


    # -------------------------------------------------
    # ACTUALIZAR CITA
    # -------------------------------------------------

    @app.route(
        "/agenda/actualizar/<int:id>",
        methods=["POST"]
    )
    def actualizar_cita_route(id):
        cita = obtener_cita_por_id(id)

        if cita is None:
            return redirect(
                url_for(
                    "agenda",
                    error="La cita solicitada no existe."
                )
            )

        id_paciente = request.form["id_paciente"]
        id_usuario = request.form["id_usuario"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]

        duracion_minutos = int(
            request.form["duracion_minutos"]
        )

        motivo = request.form["motivo"]
        estado = request.form["estado"]

        if estado != "CANCELADA":
            horario_ocupado = existe_cita_en_horario(
                id_usuario,
                fecha,
                hora,
                duracion_minutos,
                id_cita_excluir=id
            )

            if horario_ocupado:
                cita_temporal = {
                    "id_cita": id,
                    "id_paciente": int(id_paciente),
                    "id_usuario": int(id_usuario),
                    "fecha": fecha,
                    "hora": hora,
                    "duracion_minutos": duracion_minutos,
                    "motivo": motivo,
                    "estado": estado
                }

                return cargar_agenda(
                    fecha=fecha,
                    error=(
                        "No se pudo actualizar la cita porque el "
                        "horario se cruza con otra atención del "
                        "mismo profesional."
                    ),
                    cita_editar=cita_temporal
                )

        actualizar_cita(
            id,
            id_paciente,
            id_usuario,
            fecha,
            hora,
            duracion_minutos,
            motivo,
            estado
        )

        return redirect(
            url_for(
                "agenda",
                fecha=fecha,
                mensaje="Cita actualizada correctamente."
            )
        )


    # -------------------------------------------------
    # CANCELAR CITA
    # -------------------------------------------------

    @app.route(
        "/agenda/cancelar/<int:id>",
        methods=["POST"]
    )
    def cancelar_cita_route(id):
        cita = obtener_cita_por_id(id)

        fecha_retorno = request.form.get(
            "fecha_retorno",
            date.today().isoformat()
        )

        if cita is None:
            return redirect(
                url_for(
                    "agenda",
                    fecha=fecha_retorno,
                    error="La cita solicitada no existe."
                )
            )

        if cita["estado"] == "CANCELADA":
            return redirect(
                url_for(
                    "agenda",
                    fecha=fecha_retorno,
                    error="La cita ya se encuentra cancelada."
                )
            )

        cancelar_cita(id)

        return redirect(
            url_for(
                "agenda",
                fecha=fecha_retorno,
                mensaje=(
                    "Cita cancelada correctamente. "
                    "El registro se mantiene en el historial."
                )
            )
        )