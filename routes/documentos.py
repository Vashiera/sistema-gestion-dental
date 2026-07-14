import os
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, current_app

from models.documento import (
    obtener_documentos,
    obtener_tipos_documento,
    crear_documento
)

from models.paciente import obtener_lista_pacientes


def registrar_documentos(app):

    @app.route("/documentos")
    def documentos():

        lista_documentos = obtener_documentos()
        lista_pacientes = obtener_lista_pacientes()
        lista_tipos = obtener_tipos_documento()

        return render_template(
            "documentos/documentos.html",
            documentos=lista_documentos,
            pacientes=lista_pacientes,
            tipos_documento=lista_tipos
        )


    @app.route("/documentos/crear", methods=["POST"])
    def crear_documento_route():

        archivo = request.files.get("archivo")
        ruta_archivo = ""

        if archivo and archivo.filename != "":
            nombre_archivo = secure_filename(archivo.filename)

            carpeta_destino = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "documentos"
            )

            os.makedirs(carpeta_destino, exist_ok=True)

            ruta_guardado = os.path.join(carpeta_destino, nombre_archivo)
            archivo.save(ruta_guardado)

            ruta_archivo = f"uploads/documentos/{nombre_archivo}"

        crear_documento(
            request.form["id_paciente"],
            request.form["id_tipo_documento"],
            request.form["nombre_documento"],
            ruta_archivo
        )

        return redirect(url_for("documentos"))