"""Ejecuta casos SOAP 1.2 reales sobre HTTP local y guarda sus respuestas."""
from datetime import datetime
from getpass import getuser
from http.server import ThreadingHTTPServer
from pathlib import Path
from socket import gethostname
from threading import Thread
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

from server import Handler, SOAP, TIT

BASE = Path(__file__).parent
SALIDAS = BASE / "responses"
CASOS = (
    ("consulta_valida", 200, "VALIDO"),
    ("consulta_no_valida", 200, "NO_VALIDO"),
    ("consulta_sin_codigo", 500, "codigoRegistro es obligatorio."),
)


def enviar(puerto, nombre, espera=2):
    datos = (BASE / "requests" / (nombre + ".xml")).read_bytes()
    solicitud = Request(
        f"http://127.0.0.1:{puerto}/soap",
        data=datos,
        headers={"Content-Type": "application/soap+xml; charset=utf-8"},
        method="POST",
    )
    try:
        with urlopen(solicitud, timeout=espera) as respuesta:
            return respuesta.status, respuesta.read()
    except HTTPError as error:
        return error.code, error.read()


def run():
    # Puerto temporal: evita interferir con un servicio abierto en el puerto 8000.
    servicio = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    servicio.daemon_threads = True
    Thread(target=servicio.serve_forever, daemon=True).start()
    puerto = servicio.server_port
    SALIDAS.mkdir(exist_ok=True)
    lineas = [f"Fecha/hora local: {datetime.now().astimezone().isoformat(timespec='seconds')}",
              f"Equipo: {gethostname()} | Usuario: {getuser()}",
              "Demo local y sintética; no consulta un registro académico real."]
    try:
        with urlopen(f"http://127.0.0.1:{puerto}/wsdl", timeout=2) as respuesta:
            ET.fromstring(respuesta.read())
            assert respuesta.status == 200
        lineas.append("WSDL: HTTP 200, XML válido")
        for nombre, esperado_http, esperado_valor in CASOS:
            estado, datos = enviar(puerto, nombre)
            raiz = ET.fromstring(datos)
            cuerpo = raiz.find(f"{{{SOAP}}}Body")
            assert cuerpo is not None, nombre
            assert estado == esperado_http, f"{nombre}: HTTP {estado} != {esperado_http}"
            if estado == 200:
                valor = cuerpo.findtext(f"{{{TIT}}}ConsultarRegistroResponse/{{{TIT}}}resultado")
            else:
                valor = cuerpo.findtext(f"{{{SOAP}}}Fault/{{{SOAP}}}Reason/{{{SOAP}}}Text")
            assert valor == esperado_valor, f"{nombre}: {valor!r} != {esperado_valor!r}"
            ET.indent(raiz)
            (SALIDAS / f"{nombre}.xml").write_bytes(ET.tostring(raiz, encoding="utf-8", xml_declaration=True))
            lineas.append(f"{nombre}: HTTP {estado} | {valor} | OK")
        try:
            enviar(puerto, "consulta_lenta", espera=1)
            raise AssertionError("La consulta lenta debía superar un segundo")
        except (TimeoutError, URLError) as error:
            lineas.append(f"consulta_lenta: espera de 1 s agotada | OK ({type(error).__name__})")
        lineas.append("RESULTADO: 4 casos y WSDL comprobados")
    finally:
        servicio.shutdown()
        servicio.server_close()
    resultado = "\n".join(lineas) + "\n"
    (SALIDAS / "salida_pruebas.txt").write_text(resultado, encoding="utf-8")
    print(resultado, end="")


if __name__ == "__main__":
    run()
