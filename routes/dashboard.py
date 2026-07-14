from flask import render_template

from models.dashboard import (
    obtener_resumen_dashboard,
    obtener_citas_hoy_dashboard,
    obtener_evoluciones_recientes_dashboard,
    obtener_pagos_recientes_dashboard,
    obtener_alertas_dashboard
)


def registrar_dashboard(app):

    @app.route("/dashboard")
    def dashboard():

        resumen = obtener_resumen_dashboard()
        citas_hoy = obtener_citas_hoy_dashboard()
        evoluciones_recientes = (
            obtener_evoluciones_recientes_dashboard()
        )
        pagos_recientes = obtener_pagos_recientes_dashboard()
        alertas = obtener_alertas_dashboard()

        return render_template(
            "dashboard/dashboard.html",
            resumen=resumen,
            citas_hoy=citas_hoy,
            evoluciones_recientes=evoluciones_recientes,
            pagos_recientes=pagos_recientes,
            alertas=alertas
        )