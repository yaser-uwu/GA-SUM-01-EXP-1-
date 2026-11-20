# Guía para probar la consulta REST

La prueba se hizo con nuestro sistema de Revisión Técnica Vehicular y su base PostgreSQL. Para repetirla tal como está se necesita ese proyecto, una cuenta habilitada y un turno asociado a su propietario. Descargar estos archivos por sí solos no pone en marcha todo el RTV.

## Si se utiliza otro proyecto

La idea que se puede adaptar es esta: iniciar sesión, identificar al usuario en el backend y consultar únicamente los registros que le corresponden. Para usarla en otro sistema hay que ajustar:

- La dirección del backend y las rutas de inicio de sesión y consulta en `index.html` y `ClienteConsulta.java`.
- Los nombres de los campos que recibe el inicio de sesión y los que devuelve la consulta.
- La relación entre la cuenta y el dueño del registro. En nuestro caso se usa la tabla `srtv_usuario_propietario`.
- La comprobación de sesión y los permisos del personal.
- Los registros de prueba y la configuración de CORS para el cliente.

El archivo `backend-consulta-turnos.patch` corresponde al código y a los paquetes de nuestro RTV. No se aplica directamente a un proyecto con otra estructura.

## Preparar el RTV

Se utiliza el proyecto RTV completo y su configuración local de PostgreSQL. Este directorio contiene el cliente y los cambios de este avance, no una copia de todo el sistema. Requisito: JDK 21.

El parche contiene únicamente los cambios para esta consulta. Desde la raíz de una copia del RTV que todavía no los tenga, comprobar y aplicar el archivo descargado:

```powershell
git apply --check RUTA/backend-consulta-turnos.patch
git apply RUTA/backend-consulta-turnos.patch
```

`RUTA` corresponde a la carpeta donde se descargó el parche. En el RTV donde se desarrolló esta demo, esos cambios ya están aplicados y no se repite su aplicación.

La administración de la base ejecuta `backend/scripts/consulta_turnos_vinculo_usuario_propietario.sql` y registra una vinculación verificada entre la cuenta del solicitante y el propietario. La cuenta necesita un rol activo sin permisos del personal. El usuario PostgreSQL de esa cuenta necesita lectura de las tablas y columnas consultadas, además de los permisos que el RTV requiere para registrar la sesión y su auditoría. La cuenta del solicitante no debe poder editar la tabla de vinculación ni asignarse permisos del personal.

La demo local emplea la cuenta ficticia `exp1_solicitante`, el propietario de prueba 27 y su turno 82. El turno 22 pertenece a otro propietario. Los identificadores de otra base pueden ser diferentes. Las contraseñas, los tokens y la configuración privada de la base se conservan fuera de este repositorio.

Desde `backend/`, ejecutar:

```powershell
.\mvnw.cmd spring-boot:run "-Dspring-boot.run.arguments=--server.port=8082 --server.address=127.0.0.1 --spring.jpa.hibernate.ddl-auto=none"
```

El backend conserva sus inicializadores y tareas habituales. El parámetro de Hibernate evita la actualización automática de su esquema, pero no desactiva los inicializadores propios del RTV.

## Ejecución del cliente web

Desde la carpeta `demos/kevin/`, en otra terminal:

```powershell
java -m jdk.httpserver -b 127.0.0.1 -p 4200 -d "$((Get-Location).Path)"
```

Abrir <http://localhost:4200/>. El origen coincide con la configuración CORS del RTV. Iniciar sesión con la cuenta de prueba y consultar el turno propio. La contraseña se limpia después de cada intento de inicio de sesión y el token permanece en memoria, sin guardarse en el navegador. Los procesos se detienen con `Ctrl+C` en sus terminales.

Para el cliente Java, proporcionar el JWT mediante la variable local `RTV_TOKEN` y ejecutar:

```powershell
java ClienteConsulta.java 82
```

En `peticiones.http`, `token` es una variable privada del cliente HTTP del IDE. No se sustituye por un token real en el archivo que se sube al repositorio.

## Qué probar

1. Iniciar sesión con la cuenta del solicitante.
2. Consultar un turno suyo: debe responder `200` y mostrar el estado y las fechas.
3. Cambiar el identificador por el de otro propietario: debe responder `404` sin mostrar sus datos.
4. Consultar sin sesión: debe responder `401`.
5. Intentar el listado interno con la cuenta del solicitante: debe responder `403`.
6. Consultar la ruta interna con una cuenta del personal que tenga permiso: debe responder `200`.

Los archivos `respuesta-200.http` y `respuesta-404.http` conservan las respuestas obtenidas en la prueba. Las dos capturas muestran lo que recibió el cliente.

## Pruebas del backend

Desde la carpeta `backend/` del RTV:

```powershell
.\mvnw.cmd -Dtest=ConsultaTurnoAccessTest test
```

El resultado guardado en `resultado-pruebas.txt` corresponde a diez pruebas sin fallos ni errores.
