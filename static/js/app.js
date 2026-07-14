document.addEventListener("DOMContentLoaded", function () {

    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const rol = document.getElementById("rol").value;

            if (rol === "") {
                alert("Debe seleccionar un rol.");
                return;
            }

            localStorage.setItem("rolUsuario", rol);
            window.location.href = "/dashboard";
        });
    }

    const rolActivo = document.getElementById("rolActivo");

    if (rolActivo) {
        const rol = localStorage.getItem("rolUsuario") || "Sin rol";
        rolActivo.textContent = "Rol: " + rol;
    }

    const catalogoTratamiento = document.getElementById("id_catalogo");
    const valorTratamiento = document.getElementById("valor_presupuestado");

    if (catalogoTratamiento && valorTratamiento) {
        catalogoTratamiento.addEventListener("change", function () {
            const opcion = this.options[this.selectedIndex];
            valorTratamiento.value = opcion.dataset.precio || "";
        });
    }

    const catalogoPresupuesto = document.getElementById("presupuesto_catalogo");
    const cantidadPresupuesto = document.getElementById("presupuesto_cantidad");
    const precioPresupuesto = document.getElementById("presupuesto_precio");
    const btnAgregar = document.getElementById("btnAgregarTratamiento");
    const tablaDetalle = document.getElementById("tablaDetallePresupuesto");
    const totalPresupuesto = document.getElementById("totalPresupuesto");
    const detallesJson = document.getElementById("detalles_json");
    const formPresupuesto = document.getElementById("formPresupuesto");

    let detalles = [];

    function formatearCLP(valor) {
        return "$" + Number(valor).toLocaleString("es-CL");
    }

    function actualizarTablaPresupuesto() {
        if (!tablaDetalle || !totalPresupuesto || !detallesJson) {
            return;
        }

        tablaDetalle.innerHTML = "";

        if (detalles.length === 0) {
            tablaDetalle.innerHTML = `
                <tr>
                    <td colspan="5" style="text-align:center;">
                        No hay tratamientos agregados.
                    </td>
                </tr>
            `;

            totalPresupuesto.value = "$0";
            detallesJson.value = "";
            return;
        }

        let total = 0;

        detalles.forEach((item, index) => {
            total += item.subtotal;

            const fila = document.createElement("tr");

            fila.innerHTML = `
                <td>${item.nombre_tratamiento}</td>
                <td>${item.cantidad}</td>
                <td>${formatearCLP(item.precio_unitario)}</td>
                <td>${formatearCLP(item.subtotal)}</td>
                <td>
                    <button type="button" class="btn-tabla" data-index="${index}">
                        Quitar
                    </button>
                </td>
            `;

            tablaDetalle.appendChild(fila);
        });

        totalPresupuesto.value = formatearCLP(total);
        detallesJson.value = JSON.stringify(detalles);
    }

    if (catalogoPresupuesto && precioPresupuesto) {
        catalogoPresupuesto.addEventListener("change", function () {
            const opcion = this.options[this.selectedIndex];
            precioPresupuesto.value = opcion.dataset.precio || "";
        });
    }

    if (btnAgregar) {
        btnAgregar.addEventListener("click", function () {
            const opcion = catalogoPresupuesto.options[catalogoPresupuesto.selectedIndex];

            const idCatalogo = catalogoPresupuesto.value;
            const nombreTratamiento = opcion.dataset.nombre;
            const cantidad = parseInt(cantidadPresupuesto.value);
            const precioUnitario = parseFloat(precioPresupuesto.value);

            if (!idCatalogo || !cantidad || !precioUnitario) {
                alert("Debe seleccionar un tratamiento, cantidad y precio.");
                return;
            }

            const subtotal = cantidad * precioUnitario;

            detalles.push({
                id_catalogo: idCatalogo,
                nombre_tratamiento: nombreTratamiento,
                cantidad: cantidad,
                precio_unitario: precioUnitario,
                subtotal: subtotal
            });

            catalogoPresupuesto.value = "";
            cantidadPresupuesto.value = 1;
            precioPresupuesto.value = "";

            actualizarTablaPresupuesto();
        });
    }

    if (tablaDetalle) {
        tablaDetalle.addEventListener("click", function (event) {
            if (event.target.classList.contains("btn-tabla")) {
                const index = event.target.dataset.index;
                detalles.splice(index, 1);
                actualizarTablaPresupuesto();
            }
        });
    }

    if (formPresupuesto) {
        formPresupuesto.addEventListener("submit", function (event) {
            if (detalles.length === 0) {
                event.preventDefault();
                alert("Debe agregar al menos un tratamiento al presupuesto.");
                return;
            }

            detallesJson.value = JSON.stringify(detalles);
        });
    }

    const agendaProfesional = document.getElementById("agenda_id_usuario");
    const agendaFecha = document.getElementById("agenda_fecha");
    const agendaHora = document.getElementById("agenda_hora");
    const citasAgendaData = document.getElementById("citas-agenda-data");

    let citasAgenda = [];

    if (citasAgendaData) {
        try {
            citasAgenda = JSON.parse(citasAgendaData.textContent);
        } catch (error) {
            citasAgenda = [];
        }
    }

    function actualizarHorasDisponibles() {
        if (!agendaProfesional || !agendaFecha || !agendaHora) {
            return;
        }

        const idUsuario = agendaProfesional.value;
        const fecha = agendaFecha.value;

        for (const option of agendaHora.options) {
            option.disabled = false;

            if (option.value === "") {
                option.textContent = "Seleccione una hora";
            } else {
                option.textContent = option.value;
            }
        }

        if (!idUsuario || !fecha) {
            return;
        }

        const citasOcupadas = citasAgenda.filter(function (cita) {
            return (
                cita.id_usuario === idUsuario &&
                cita.fecha === fecha &&
                cita.estado !== "CANCELADA"
            );
        });

        citasOcupadas.forEach(function (cita) {
            for (const option of agendaHora.options) {
                if (option.value === cita.hora) {
                    option.disabled = true;
                    option.textContent = option.value + " - No disponible";
                }
            }
        });

        if (agendaHora.selectedOptions[0] && agendaHora.selectedOptions[0].disabled) {
            agendaHora.value = "";
        }
    }

    if (agendaProfesional && agendaFecha && agendaHora) {
        agendaProfesional.addEventListener("change", actualizarHorasDisponibles);
        agendaFecha.addEventListener("change", actualizarHorasDisponibles);
        actualizarHorasDisponibles();
    }

});