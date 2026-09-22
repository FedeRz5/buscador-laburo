#!/usr/bin/env python3
"""Entrada en español para buscar empleo en Argentina con los conectores incluidos."""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORTALES = {"linkedin": "linkedin-search", "freehire": "freehire-search", "getonbrd": "getonbrd-search"}
MODALIDADES = {"remoto": "remote", "hibrido": "hybrid", "presencial": "onsite"}


def positivo(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Ingresá un número entero positivo.")
    if number < 1:
        raise argparse.ArgumentTypeError("Ingresá un número mayor a cero.")
    return number


def crear_parser():
    parser = argparse.ArgumentParser(description="Buscador de Laburo: ofertas en Argentina.")
    parser.add_argument("puesto", help='Puesto o palabras clave, por ejemplo "administrativo"')
    parser.add_argument("--portal", choices=PORTALES, default="linkedin", help="Por defecto: linkedin")
    parser.add_argument("--ciudad", help='Ciudad argentina, por ejemplo "Córdoba"; omití para buscar en todo el país')
    parser.add_argument("--modalidad", choices=MODALIDADES, help="Sin esta opción se incluyen todas las modalidades")
    parser.add_argument("--dias", type=int, choices=[1, 7, 14, 30], default=14, help="Antigüedad máxima; por defecto: 14")
    parser.add_argument("--limite", type=positivo, default=10, help="Máximo de resultados de la página; por defecto: 10")
    parser.add_argument("--pagina", type=positivo, default=1)
    parser.add_argument("--formato", choices=["texto", "tabla", "json"], default="texto")
    return parser


def construir_comando(args, bun="bun"):
    puesto = args.puesto.strip()
    ciudad = (args.ciudad or "").strip()
    if not puesto or puesto.startswith("-"):
        raise ValueError("Escribí un puesto o palabras clave que no empiecen con un guion.")
    if args.ciudad is not None and (not ciudad or ciudad.startswith("-")):
        raise ValueError("Escribí una ciudad argentina válida.")
    if args.portal == "getonbrd" and (ciudad or args.modalidad in {"hibrido", "presencial"}):
        raise ValueError("Get on Board admite país y filtro remoto, pero no ciudad ni filtro híbrido/presencial. Usá LinkedIn para esos filtros.")
    script = ROOT / ".agents" / "skills" / PORTALES[args.portal] / "cli" / "src" / "cli.ts"
    cmd = [bun, "run", str(script), "search", "--query", puesto]
    if args.portal == "freehire":
        cmd += ["--country", "AR"]
        if ciudad:
            cmd += ["--city", ciudad]
    elif args.portal == "linkedin":
        cmd += ["--location", f"{ciudad}, Argentina" if ciudad else "Argentina"]
    else:
        cmd += ["--location", "Argentina"]
    if args.modalidad:
        cmd += ["--remote"]
        if args.portal != "getonbrd":
            cmd += [MODALIDADES[args.modalidad]]
    cmd += ["--jobage", str(args.dias), "--limit", str(args.limite), "--page", str(args.pagina),
            "--format", {"texto": "plain", "tabla": "table", "json": "json"}[args.formato]]
    return cmd


def main(argv=None):
    parser = crear_parser()
    args = parser.parse_args(argv)
    try:
        cmd = construir_comando(args)
    except ValueError as exc:
        parser.error(str(exc))
    bun = shutil.which("bun")
    if not bun:
        print("No se encontró Bun. Instalalo y volvé a abrir la terminal.", file=sys.stderr)
        return 1
    cmd[0] = bun
    try:
        return subprocess.run(cmd, cwd=ROOT, timeout=120).returncode
    except subprocess.TimeoutExpired:
        print("La consulta superó los dos minutos. Probá de nuevo más tarde.", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"No se pudo ejecutar la búsqueda: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Búsqueda cancelada.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
