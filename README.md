# Sistema de Gestión Dental

**Proyecto de Titulación – Ingeniería en Informática | IPLACEX**

---

## Descripción

Sistema web orientado a clínicas odontológicas pequeñas, diseñado para administrar pacientes, citas, tratamientos, presupuestos, pagos, evoluciones clínicas y documentos digitales de manera centralizada.

El objetivo del proyecto es mejorar la organización de la información clínica y administrativa, reduciendo el uso de documentación física mediante la digitalización de documentos y facilitando el acceso seguro a la información de los pacientes.

---

## Funcionalidades principales

- Inicio de sesión con autenticación de usuarios.
- Gestión de pacientes.
- Agenda de citas.
- Gestión de tratamientos odontológicos.
- Registro de evoluciones clínicas.
- Creación y administración de presupuestos.
- Registro de pagos.
- Gestión de documentos digitales asociados al paciente.
- Administración de usuarios y roles.

---

## Tecnologías utilizadas

### Backend

- Python 3
- Flask

### Frontend

- HTML5
- CSS3
- JavaScript

### Base de datos

- MySQL 8
- MySQL Workbench

### Despliegue

- Render
- Aiven MySQL

---

## Modelo de Base de Datos

La base de datos fue diseñada utilizando un modelo relacional normalizado hasta Tercera Forma Normal (3FN).

### Tablas principales

- Roles
- Usuarios
- Pacientes
- Citas
- Catálogo de Tratamientos
- Tratamientos
- Evoluciones
- Presupuestos
- Detalle Presupuesto
- Pagos
- Tipos de Documento
- Documentos

---

## Estructura del proyecto

```
DentalClinic/
│
├── app.py
├── config.py
├── models/
├── routes/
├── templates/
├── static/
└── database/
    ├── conexion.py
    └── dentalclinic.sql
```

---

## Contenido del repositorio

- Código fuente del sistema.
- Script SQL completo (`database/dentalclinic.sql`).
- Modelos, rutas y vistas de la aplicación.
- Recursos estáticos (CSS y JavaScript).

---

## Estado del proyecto

Proyecto de titulación en desarrollo.

Actualmente cuenta con:

- Base de datos relacional completamente implementada.
- Sistema desplegado en Render.
- Base de datos MySQL alojada en Aiven.
- Módulos principales implementados y operativos.
- Autenticación de usuarios.
- Gestión de pacientes, citas, tratamientos, presupuestos, pagos, documentos y evoluciones.

---

## Autor

**Fernanda Julio**

Proyecto desarrollado como parte del proceso de titulación de Ingeniería en Informática en IPLACEX.
