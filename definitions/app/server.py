"""HTTP-Server der OKF-Projekt-Manager-SPA.

App-Factory ``create_app(bundle_root)`` liefert die statischen Dateien und einen
einheitlichen JSON-Fehlerhandler; ``main()`` startet den Server über
``BUNDLE_ROOT`` und ``PORT`` aus der Umgebung. Lokal und in Colab gleichermaßen.
"""

from __future__ import annotations

import os
import socket
import sys
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException, default_exceptions

import meta
import okf_bundle
import overview

STATIC_DIR = Path(__file__).resolve().parent / "static"

HOST = "0.0.0.0"
PORT_STANDARD = 5000

# Deutsche Standardtexte; eigene Beschreibungen (z. B. per ``abort``) haben Vorrang.
DEUTSCHE_MELDUNGEN = {
    400: "Ungültige Anfrage.",
    403: "Zugriff nicht erlaubt.",
    404: "Nicht gefunden.",
    405: "Methode nicht erlaubt.",
    500: "Interner Serverfehler.",
}


class StartFehler(ValueError):
    """Konfigurationsfehler beim Start; die Meldung geht verständlich nach stderr."""


def create_app(bundle_root: str | os.PathLike[str]) -> Flask:
    """Erzeugt die App für das Bundle unter ``bundle_root``.

    Setzt ``okf_bundle.BUNDLE_ROOT``, damit alle Fachmodule dieselbe Wurzel
    verwenden. Wirft :class:`StartFehler`, wenn die Wurzel kein Verzeichnis ist.
    """
    wurzel = _pruefe_bundle_root(bundle_root)
    okf_bundle.BUNDLE_ROOT = str(wurzel)

    app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="/static")
    app.config["BUNDLE_ROOT"] = str(wurzel)
    # Fehler werden immer als JSON beantwortet, nie als HTML-Traceback.
    app.config["PROPAGATE_EXCEPTIONS"] = False
    app.json.ensure_ascii = False

    @app.get("/")
    def index():
        return send_from_directory(STATIC_DIR, "index.html")

    @app.errorhandler(HTTPException)
    def http_fehler(fehler: HTTPException):
        return jsonify(error=_fehler_meldung(fehler)), fehler.code or 500

    @app.errorhandler(Exception)
    def unerwarteter_fehler(fehler: Exception):
        app.logger.exception("Unbehandelter Fehler")
        return jsonify(error="Interner Serverfehler"), 500

    for fehler_typ, code in _domaenen_fehler():
        app.register_error_handler(fehler_typ, _domaenen_handler(code))

    @app.get("/api/overview")
    def api_overview():
        return jsonify(overview.liste())

    @app.get("/api/file")
    def api_file():
        pfad = (request.args.get("path") or "").strip()
        if not pfad:
            abort(400, description="Parameter path fehlt")
        return jsonify(overview.details(pfad))

    @app.get("/api/aufgaben")
    def api_aufgaben():
        return jsonify(overview.liste("aufgaben"))

    @app.get("/api/wellen")
    def api_wellen():
        return jsonify(overview.liste("wellen"))

    return app


def main() -> int:
    """Startet den Server aus der Umgebung; Rückgabe ist der Exit-Code."""
    try:
        bundle_root = _bundle_root_aus_umgebung()
        port = _port_aus_umgebung()
        app = create_app(bundle_root)
    except StartFehler as fehler:
        print(f"Start abgebrochen: {fehler}", file=sys.stderr)
        return 1

    if _port_belegt(HOST, port):
        print(f"Start abgebrochen: Port {port} ist bereits belegt.", file=sys.stderr)
        return 1

    print(f"OKF Projekt-Manager startet auf http://{HOST}:{port}", flush=True)
    try:
        app.run(host=HOST, port=port, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("Server beendet.", flush=True)
    except OSError as fehler:
        print(f"Start abgebrochen: Port {port} ist bereits belegt ({fehler}).", file=sys.stderr)
        return 1
    return 0


def _fehler_meldung(fehler: HTTPException) -> str:
    """Eigene Beschreibung (aus ``abort``) vor dem deutschen Standardtext."""
    vorgabe = default_exceptions.get(fehler.code)
    eigene = fehler.description
    if eigene and (vorgabe is None or eigene != vorgabe.description):
        return eigene

    bekannt = DEUTSCHE_MELDUNGEN.get(fehler.code)
    if bekannt:
        return bekannt
    return f"Anfrage fehlgeschlagen ({fehler.code})."


def _domaenen_fehler() -> list[tuple[type[Exception], int]]:
    """Domänen-Exceptions mit HTTP-Code; optionale Typen nur, wenn vorhanden."""
    fehler: list[tuple[type[Exception], int]] = [
        (okf_bundle.BundlePfadFehler, 400),
        (okf_bundle.FrontmatterFehler, 400),
        (okf_bundle.EingabeFehler, 400),
        (meta.RechteFehler, 403),
        (FileNotFoundError, 404),
    ]

    reserviert = getattr(okf_bundle, "ReservierteDateiFehler", None)
    if reserviert is not None:
        fehler.append((reserviert, 403))
    return fehler


def _domaenen_handler(code: int):
    """JSON-Fehlerhandler für Domänen-Exceptions mit verständlicher Meldung."""

    def handler(fehler: Exception):
        meldung = str(fehler).strip() or DEUTSCHE_MELDUNGEN.get(code) or "Anfrage fehlgeschlagen"
        return jsonify(error=meldung), code

    return handler


def _pruefe_bundle_root(bundle_root: str | os.PathLike[str] | None) -> Path:
    """Liefert die absolute Bundle-Wurzel oder wirft :class:`StartFehler`."""
    if bundle_root is None or not str(bundle_root).strip():
        raise StartFehler("BUNDLE_ROOT ist nicht gesetzt (z. B. BUNDLE_ROOT=./wissen).")

    wurzel = Path(os.path.realpath(str(bundle_root).strip()))
    if not wurzel.is_dir():
        raise StartFehler(f"BUNDLE_ROOT ist kein Verzeichnis: {wurzel}")
    return wurzel


def _bundle_root_aus_umgebung() -> str:
    wert = os.environ.get("BUNDLE_ROOT")
    if wert is None or not wert.strip():
        raise StartFehler("BUNDLE_ROOT ist nicht gesetzt (z. B. BUNDLE_ROOT=./wissen).")
    return wert.strip()


def _port_aus_umgebung() -> int:
    roh = os.environ.get("PORT", "").strip()
    if not roh:
        return PORT_STANDARD
    try:
        port = int(roh)
    except ValueError:
        raise StartFehler(f"PORT ist keine Zahl: {roh!r}") from None
    if not 1 <= port <= 65535:
        raise StartFehler(f"PORT liegt außerhalb von 1–65535: {port}")
    return port


def _port_belegt(host: str, port: int) -> bool:
    """Prüft vorab, ob der Port belegt ist (Werkzeug meldet das sonst erst spät)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            probe.bind((host, port))
        except OSError:
            return True
    return False


if __name__ == "__main__":
    sys.exit(main())
