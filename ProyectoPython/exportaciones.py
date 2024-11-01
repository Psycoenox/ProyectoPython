# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:11:22 2024

@author: Marcell
"""

import json
import csv
from db import cursor, conn
from datetime import datetime

def guardar_inventario_json():
    cursor.execute("SELECT * FROM Inventario")
    inventario = cursor.fetchall()
    with open("inventario.json", "w") as file:
        json.dump([{"ID": p[0], "Tipo": p[1], "Nombre": p[2], "Estado": p[3], "PrecioCompra": p[4], "PrecioVenta": p[5]} for p in inventario], file)
    print("Inventario guardado en inventario.json")

def exportar_a_csv():
    # Generar una marca de tiempo en el formato "YYYYMMDD_HHMMSS"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Exportar la tabla de Empleados a un archivo CSV con la marca de tiempo
    cursor.execute("SELECT * FROM Empleados")
    empleados = cursor.fetchall()
    with open(f"empleados_{timestamp}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Nombre", "Edad", "Tipo", "Salario"])
        writer.writerows(empleados)

    # Exportar la tabla de Inventario a un archivo CSV con la marca de tiempo
    cursor.execute("SELECT * FROM Inventario")
    inventario = cursor.fetchall()
    with open(f"inventario_{timestamp}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Tipo", "Nombre", "Estado", "Precio Compra", "Precio Venta"])
        writer.writerows(inventario)

    print(f"Datos exportados a empleados_{timestamp}.csv e inventario_{timestamp}.csv")