"""Demo SOAP 1.2 local; TEST-001/002 son datos ficticios."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from time import sleep
import xml.etree.ElementTree as ET

SOAP = "http://www.w3.org/2003/05/soap-envelope"
TIT = "urn:propuesta:verificacion-titulo"
ET.register_namespace("soap", SOAP)
ET.register_namespace("tit", TIT)


def envelopar(nodo):
    raiz = ET.Element(f"{{{SOAP}}}Envelope")
    ET.SubElement(raiz, f"{{{SOAP}}}Body").append(nodo)
    return ET.tostring(raiz, encoding="utf-8", xml_declaration=True)


def fallo(texto):
    fault = ET.Element(f"{{{SOAP}}}Fault")
    codigo = ET.SubElement(fault, f"{{{SOAP}}}Code")
    ET.SubElement(codigo, f"{{{SOAP}}}Value").text = "soap:Sender"
    razon = ET.SubElement(fault, f"{{{SOAP}}}Reason")
    ET.SubElement(razon, f"{{{SOAP}}}Text", {"{http://www.w3.org/XML/1998/namespace}lang": "es"}).text = texto
    return envelopar(fault)


class Handler(BaseHTTPRequestHandler):
    def responder(self, estado, datos, tipo="application/soap+xml; charset=utf-8"):
        self.send_response(estado)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        try:
            self.wfile.write(datos)
        except BrokenPipeError:
            pass

    def do_GET(self):
        if self.path.split("?", 1)[0] in ("/", "/wsdl"):
            self.responder(200, Path(__file__).with_name("verificar_titulo.wsdl").read_bytes(), "application/xml; charset=utf-8")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/soap":
            self.send_error(404)
            return
        if not self.headers.get("Content-Type", "").lower().startswith("application/soap+xml"):
            self.responder(415, fallo("Se requiere SOAP 1.2."))
            return
        try:
            longitud = int(self.headers.get("Content-Length", "0"))
            if not 0 < longitud <= 65536:
                self.responder(413, fallo("Tamaño de solicitud no permitido."))
                return
            raiz = ET.fromstring(self.rfile.read(longitud))
            if raiz.tag != f"{{{SOAP}}}Envelope":
                raise ValueError("Se esperaba Envelope SOAP 1.2.")
            cuerpo = raiz.find(f"{{{SOAP}}}Body")
            operacion = cuerpo.find(f"{{{TIT}}}ConsultarRegistro") if cuerpo is not None else None
            if operacion is None:
                raise ValueError("Se esperaba ConsultarRegistro.")
            codigo = (operacion.findtext(f"{{{TIT}}}codigoRegistro") or "").strip()
            if not codigo:
                raise ValueError("codigoRegistro es obligatorio.")
            if codigo == "TEST-LENTO":
                sleep(5)
            resultado = {"TEST-001": "VALIDO", "TEST-002": "NO_VALIDO"}.get(codigo, "NO_ENCONTRADO")
            nodo = ET.Element(f"{{{TIT}}}ConsultarRegistroResponse")
            ET.SubElement(nodo, f"{{{TIT}}}resultado").text = resultado
            self.responder(200, envelopar(nodo))
        except (ValueError, ET.ParseError) as error:
            self.responder(500, fallo(str(error)))


if __name__ == "__main__":
    print("Mock SOAP 1.2 local: http://127.0.0.1:8000/soap", flush=True)
    print("Contrato WSDL: http://127.0.0.1:8000/wsdl", flush=True)
    print("Solo usa datos ficticios; Ctrl+C para detenerlo.", flush=True)
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
