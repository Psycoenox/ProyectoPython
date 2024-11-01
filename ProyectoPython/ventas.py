# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:11:21 2024

@author: Marcell
"""

from db import cursor

def ver_historial_ventas():
    cursor.execute("SELECT * FROM HistorialVentas")
    ventas = cursor.fetchall()
    if ventas:
        print("\n--- Historial de Ventas ---")
        for venta in ventas:
            print(f"ID Venta: {venta[0]}, Producto ID: {venta[1]}, Nombre: {venta[2]}, Precio Venta: {venta[3]}, Fecha: {venta[4]}")
    else:
        print("No se han registrado ventas.")
