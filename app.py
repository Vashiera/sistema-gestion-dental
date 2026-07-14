from datetime import datetime
from flask import Flask
from config import Config

from routes.auth import registrar_auth
from routes.dashboard import registrar_dashboard
from routes.agenda import registrar_agenda
from routes.pacientes import registrar_pacientes
from routes.tratamientos import registrar_tratamientos
from routes.presupuestos import registrar_presupuestos
from routes.documentos import registrar_documentos
from routes.administracion import registrar_administracion
from routes.evoluciones import registrar_evoluciones

app = Flask(__name__)
app.config.from_object(Config)

@app.context_processor
def inject_global_variables():
    return {"current_year": datetime.now().year}

registrar_auth(app)
registrar_dashboard(app)
registrar_agenda(app)
registrar_pacientes(app)
registrar_tratamientos(app)
registrar_presupuestos(app)
registrar_documentos(app)
registrar_administracion(app)
registrar_evoluciones(app)

if __name__ == "__main__":
    app.run(debug=True)