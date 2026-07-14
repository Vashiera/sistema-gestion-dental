from flask import render_template, request, redirect, url_for

from models.pago import (
    obtener_estados_cuenta,
    obtener_estado_cuenta_paciente,
    obtener_pagos_por_paciente,
    obtener_tratamientos_financieros_por_paciente,
    registrar_pago,
    anular_pago
)


def registrar_presupuestos(app):

    # -------------------------------------------------
    # PANEL GLOBAL DE PRESUPUESTOS Y PAGOS
    # -------------------------------------------------

    @app.route("/presupuestos")
    def presupuestos():
        estados_cuenta = obtener_estados_cuenta()

        mensaje = request.args.get("mensaje")
        error = request.args.get("error")

        total_presupuestado = sum(
            cuenta["total_tratamientos"] or 0
            for cuenta in estados_cuenta
        )

        total_pagado = sum(
            cuenta["total_pagado"] or 0
            for cuenta in estados_cuenta
        )

        total_pendiente = sum(
            cuenta["saldo"] or 0
            for cuenta in estados_cuenta
        )

        cantidad_pendientes = sum(
            1
            for cuenta in estados_cuenta
            if cuenta["estado_pago"] == "PENDIENTE"
        )

        cantidad_parciales = sum(
            1
            for cuenta in estados_cuenta
            if cuenta["estado_pago"] == "PAGO PARCIAL"
        )

        cantidad_pagados = sum(
            1
            for cuenta in estados_cuenta
            if cuenta["estado_pago"] == "PAGADO"
        )

        return render_template(
            "presupuestos/presupuestos.html",
            estados_cuenta=estados_cuenta,
            total_presupuestado=total_presupuestado,
            total_pagado=total_pagado,
            total_pendiente=total_pendiente,
            cantidad_pendientes=cantidad_pendientes,
            cantidad_parciales=cantidad_parciales,
            cantidad_pagados=cantidad_pagados,
            mensaje=mensaje,
            error=error
        )


    # -------------------------------------------------
    # DETALLE FINANCIERO DE UN PACIENTE
    # -------------------------------------------------

    @app.route("/presupuesto/paciente/<int:id>")
    def presupuesto_detalle(id):
        cuenta = obtener_estado_cuenta_paciente(id)

        if cuenta is None:
            return redirect(
                url_for(
                    "presupuestos",
                    error="El paciente solicitado no existe."
                )
            )

        tratamientos = (
            obtener_tratamientos_financieros_por_paciente(id)
        )

        pagos = obtener_pagos_por_paciente(id)

        mensaje = request.args.get("mensaje")
        error = request.args.get("error")

        return render_template(
            "presupuestos/presupuesto-detalle.html",
            cuenta=cuenta,
            tratamientos=tratamientos,
            pagos=pagos,
            mensaje=mensaje,
            error=error
        )


    # -------------------------------------------------
    # REGISTRAR UN PAGO O ABONO
    # -------------------------------------------------

    @app.route(
        "/presupuestos/pago/registrar/<int:id_paciente>",
        methods=["POST"]
    )
    def registrar_pago_route(id_paciente):
        cuenta = obtener_estado_cuenta_paciente(id_paciente)

        if cuenta is None:
            return redirect(
                url_for(
                    "presupuestos",
                    error="El paciente seleccionado no existe."
                )
            )

        monto = request.form.get("monto", "").strip()
        metodo_pago = request.form.get(
            "metodo_pago",
            ""
        ).strip().upper()

        observaciones = request.form.get(
            "observaciones",
            ""
        ).strip()

        registrado, mensaje = registrar_pago(
            id_paciente,
            1,  # Temporal: usuario autenticado
            monto,
            metodo_pago,
            observaciones
        )

        if not registrado:
            return redirect(
                url_for(
                    "presupuesto_detalle",
                    id=id_paciente,
                    error=mensaje
                )
            )

        return redirect(
            url_for(
                "presupuesto_detalle",
                id=id_paciente,
                mensaje=mensaje
            )
        )


    # -------------------------------------------------
    # ANULAR UN PAGO
    # -------------------------------------------------

    @app.route(
        "/presupuestos/pago/anular/<int:id_pago>",
        methods=["POST"]
    )
    def anular_pago_route(id_pago):
        id_paciente = request.form.get(
            "id_paciente",
            type=int
        )

        if id_paciente is None:
            return redirect(
                url_for(
                    "presupuestos",
                    error=(
                        "No se pudo identificar al paciente "
                        "asociado al pago."
                    )
                )
            )

        pago_anulado = anular_pago(id_pago)

        if not pago_anulado:
            return redirect(
                url_for(
                    "presupuesto_detalle",
                    id=id_paciente,
                    error=(
                        "El pago no existe o ya se encuentra anulado."
                    )
                )
            )

        return redirect(
            url_for(
                "presupuesto_detalle",
                id=id_paciente,
                mensaje=(
                    "Pago anulado correctamente. "
                    "El registro se conserva en el historial."
                )
            )
        )