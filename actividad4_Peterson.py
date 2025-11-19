import csv
from collections import defaultdict
fichero = "la-liga-2025-UTC.csv"
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