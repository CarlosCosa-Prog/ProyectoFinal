# Manual del Módulo de Gestión Escolar (School System)

## 1. Introducción

Este documento sirve como un manual de usuario para el módulo **School System** de Odoo. El módulo está diseñado para facilitar la gestión de las entidades clave en una institución educativa, como estudiantes, profesores, clases y calificaciones.

## 2. Características Principales

-   Gestión de información de Estudiantes.
-   Gestión de información de Profesores.
-   Organización de Clases.
-   Registro de Materias.
-   Creación y cálculo de Boletines de calificaciones.
-   Generación de reportes imprimibles para los boletines.

## 3. Modelos de Datos (Registros)

El módulo se compone de varios modelos interconectados para gestionar la información de manera eficiente.

### 3.1. Estudiante (`student`)

Almacena la información detallada de cada estudiante.

-   **Campos Principales:**
    -   `Nom`: Nombre del estudiante.
    -   `Prénom`: Apellido del estudiante.
    -   `Age`: Edad (campo de texto).
    -   `Date Of Birth`: Fecha de nacimiento.
    -   `Total Age`: Edad calculada automáticamente a partir de la fecha de nacimiento.
    -   `Teacher`: Profesor asignado al estudiante.
    -   `Classe`: Clase a la que pertenece el estudiante.
-   **Etapas (Stages):**
    -   `Draft`: Borrador.
    -   `Enrolled`: Inscrito.
    -   `Completed`: Completado.

### 3.2. Profesor (`teacher`)

Registra la información de los profesores.

-   **Campos Principales:**
    -   `Nom`: Nombre del profesor.
    -   `Prénom`: Apellido del profesor.

### 3.3. Clase (`classe`)

Define las clases o aulas de la institución.

-   **Campos Principales:**
    -   `Libellé`: Nombre o etiqueta de la clase (ej. "5to Grado A").
    -   `Code`: Código único para la clase.

### 3.4. Materia (`matiere`)

Define las materias o asignaturas que se imparten.

-   **Campos Principales:**
    -   `Libellé`: Nombre de la materia (ej. "Matemáticas").
    -   `Code`: Código único para la materia.

### 3.5. Boletín de Calificaciones (`bulletin`)

Permite registrar las calificaciones de un estudiante para generar un boletín.

-   **Campos Principales:**
    -   `Student`: El estudiante al que pertenece el boletín.
    -   `Teacher`: El profesor asociado.
    -   `Note Moyenne`: Nota media calculada automáticamente.
-   **Líneas de Boletín (`bulletin.ligne`):**
    -   Cada línea representa la calificación de una materia.
    -   `Matière`: La materia evaluada.
    -   `Note`: La calificación obtenida.
    -   `Coefficient`: El peso o coeficiente de la materia para el cálculo del promedio.
-   **Etapas (Stages):**
    -   `Draft`: Borrador.
    -   `Failed`: Reprobado.
    -   `Succeed`: Aprobado.

## 4. Navegación

El acceso a las diferentes funcionalidades del módulo se realiza a través del menú principal de Odoo:

-   **School System**: Este es el menú principal del módulo. Al hacer clic, se desplegarán submenús para acceder a las vistas de:
    -   Estudiantes
    -   Profesores
    -   Clases
    -   Materias
    -   Boletines

## 5. Seguridad y Permisos

Según el archivo `ir.model.access.csv`, el acceso a los datos del módulo está configurado de la siguiente manera:

-   **Grupo de Usuarios**: `base.group_user` (Usuarios generales de Odoo).
-   **Permisos**: Todos los usuarios del grupo `base.group_user` tienen permisos completos (Lectura, Escritura, Creación y Borrado) en todos los modelos del módulo:
    -   `student`
    -   `teacher`
    -   `classe`
    -   `bulletin`
    -   `matiere`
    -   `bulletin.ligne`

Esto significa que cualquier usuario registrado en el sistema puede gestionar toda la información escolar.

## 6. Reportes

El módulo incluye un reporte para imprimir los boletines de calificaciones.

-   **Reporte de Boletín**: Se puede generar desde la vista de un registro de `Boletín`. Este reporte formatea las calificaciones, el promedio y la información del estudiante en un documento PDF listo para ser impreso o distribuido.
