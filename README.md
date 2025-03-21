# Skynet
# Skynet hará las delicias de cualquier interesado en sistemas de comunicación de empresas.
# Gestión de proyectos:
Los usuarios administradores podrán crear nuevos proyectos, asignándoles un título, una descripción, una fecha de inicio y una fecha de finalización.
Los proyectos podrán ser asignados a uno o varios usuarios.

# Gestión de tareas:
Dentro de cada proyecto, los usuarios administradores podrán crear nuevas tareas, asignándoles un título, una descripción, una fecha límite y un estado (pendiente, en progreso, completada).
Las tareas podrán ser asignadas a uno o varios usuarios dentro del proyecto.

# Visualización de tareas:
La aplicación mostrará una lista de todas las tareas, ordenadas por fecha límite y proyecto.
Se podrán filtrar las tareas por estado, usuario asignado y proyecto.

# Modificación y completación de tareas:
Los usuarios asignados a una tarea podrán modificar su descripción y marcarla como completada.
Los usuarios administradores podrán modificar todos los campos de una tarea, incluyendo su estado y los usuarios asignados.

# Mensajes y comentarios:
Los usuarios podrán enviar mensajes a otros usuarios dentro de un proyecto. Podrán enviar mensajes que pueden ver usuarios del proyecto y además mensajes entre usuarios (de un usuario a otro)
Los usuarios podrán dejar comentarios en las tareas para discutir detalles o proporcionar actualizaciones.

# Gestión de grupos y roles:
La aplicación deberá permitir la creación y gestión de grupos.
Los usuarios podrán ser asignados a uno o varios grupos dentro de un proyecto.
Se deberán definir roles (administrador, miembro, invitado) con diferentes permisos dentro de cada proyecto.

# Notificaciones:
La aplicación deberá enviar notificaciones a los usuarios cuando se les asignen tareas, cuando se modifiquen tareas en las que están involucrados, cuando reciban mensajes o cuando haya nuevos comentarios en las tareas.

# Interfaz de usuario:
La aplicación deberá tener una interfaz de usuario intuitiva y bien diseñada. Se recomienda utilizar HTML, CSS y JavaScript para el diseño y la interacción.

# Modelo de datos:
Define un modelo de datos en Django para representar los proyectos, las tareas, los mensajes, los comentarios, los usuarios y los grupos, incluyendo los campos necesarios y las relaciones entre ellos.

# Vistas, URLs y formularios:
Crea las vistas, URLs y formularios necesarios en Django para gestionar todas las funcionalidades de la aplicación.

# Autenticación y autorización:
Implementa autenticación de usuarios para que cada usuario tenga su propia cuenta y pueda acceder a la aplicación de forma segura.
Implementa un sistema de autorización basado en roles para controlar el acceso a las diferentes funcionalidades de la aplicación.

# Arquitectura y ejecucción
Proyecto desarrollado en Django utilizando vscode y cursor. Base de datos con SQLite. Se puede correr en cualquier navegador al ejecutarlo. Se han utilizado librerías de terceros como Bootstrap para mejorar la interfaz de usuario.

by Pedro Oria aka Phiphopheles
