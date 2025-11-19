import csv
from collections import defaultdict
fichero = "la-liga-2025-UTC.csv"
def cargar_Resultados(ruta_csv: str) -> list:
    partidos = []
    print("Carga el fichero:", ruta_csv)
    with open(ruta_csv, newline='', encoding="utf-8") as f:
        lector = csv.DictReader(f)
        i = 0
        for fila in lector:
            i += 1
            partidos.append(fila)
    print("Partidos cargados:", i)
    return partidos
def procesar_estadisticas(partidos):
    equipos = defaultdict(lambda: {
        "GF": 0, "GC": 0,
        "Puntos": 0,
        "DG": 0,
        "FairPlay": 0,
        "Directos": defaultdict(lambda: {"GF": 0, "GC": 0})
    })
    for p in partidos:
        home = p["Home Team"]
        away = p["Away Team"]
        resultado = p["Result"].strip()
        if "-" not in resultado or resultado.strip() == "" or resultado.count("-") != 1:
            print("Resultado no valido encontrado:", resultado)
            continue
        gh, ga = map(int, resultado.split('-'))
        equipos[home]["GF"] += gh
        equipos[home]["GC"] += ga
        equipos[away]["GF"] += ga
        equipos[away]["GC"] += gh
        equipos[home]["DG"] = equipos[home]["GF"] - equipos[home]["GC"]
        equipos[away]["DG"] = equipos[away]["GF"] - equipos[away]["GC"]
        if gh > ga:
            equipos[home]["Puntos"] += 3
        elif ga > gh:
            equipos[away]["Puntos"] += 3
        else:
            equipos[home]["Puntos"] += 1
            equipos[away]["Puntos"] += 1
        equipos[home]["Directos"][away]["GF"] += gh
        equipos[home]["Directos"][away]["GC"] += ga
        equipos[away]["Directos"][home]["GF"] += ga
        equipos[away]["Directos"][home]["GC"] += gh
    return equipos
def comparar(e1, e2, equipos):
    if e2 in equipos[e1]["Directos"]:
        dg1 = equipos[e1]["Directos"][e2]["GF"] - equipos[e1]["Directos"][e2]["GC"]
        dg2 = equipos[e2]["Directos"][e1]["GF"] - equipos[e2]["Directos"][e1]["GC"]
        if dg1 != dg2:
            return dg2 - dg1
    if equipos[e1]["DG"] != equipos[e2]["DG"]:
        return equipos[e2]["DG"] - equipos[e1]["DG"]
    if equipos[e1]["GF"] != equipos[e2]["GF"]:
        return equipos[e2]["GF"] - equipos[e1]["GF"]
    return equipos[e1]["FairPlay"] - equipos[e2]["FairPlay"]
def mostrar_clasificacion(equipos):
    from functools import cmp_to_key
    lista = list(equipos.keys())
    lista.sort(key=lambda e: -equipos[e]["Puntos"])
    lista.sort(key=cmp_to_key(lambda a, b: comparar(a, b, equipos)))
    print("\n_-_-_CLASIFICACION FINAL_-_-_")
    for pos, equipo in enumerate(lista, 1):
        e = equipos[equipo]
        print(f"{pos}. {equipo} - {e['Puntos']} pts | DG: {e['DG']} | GF: {e['GF']} | FP: {e['FairPlay']}")

def imprimir_goles(equipos):
    print("\n=== GOLES A FAVOR POR EQUIPO ===")
    for k, v in equipos.items():
        print(f"{k}: {v['GF']} goles")


def main():
    partidos = cargar_Resultados(fichero)
    equipos = procesar_estadisticas(partidos)

    imprimir_goles(equipos)
    mostrar_clasificacion(equipos)


if __name__ == "__main__":
    main()
