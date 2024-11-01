# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:10:53 2024

@author: Marcell
"""

# -*- coding: utf-8 -*-
"""
Archivo principal para ejecutar el programa de gestión de inventario y empleados.
"""
from db import inicializar_db
from empleados import agregar_empleado
from inventario import agregar_producto, listar_inventario, reparar_producto, vender_producto
from ventas import ver_historial_ventas
from exportaciones import guardar_inventario_json, exportar_a_csv
import sys

def menu():
    inicializar_db()
    while True:
        print("\n--- Menú Principal ---")
        print("1. Agregar empleado")
        print("2. Agregar producto al inventario")
        print("3. Listar inventario")
        print("4. Reparar producto dañado")
        print("5. Vender producto")
        print("6. Ver historial de ventas")
        print("7. Guardar inventario en JSON")
        print("8. Exportar Datos en CSV")
        print("9. Salir")

        opcion = input("Selecciona una opción: ")
        
        opciones = {
            "1": agregar_empleado,
            "2": agregar_producto,
            "3": listar_inventario,
            "4": reparar_producto,
            "5": vender_producto,
            "6": ver_historial_ventas,
            "7": guardar_inventario_json,
            "8": exportar_a_csv,
            "9": salir
        }
        
        funcion = opciones.get(opcion)
        if funcion:
            funcion()
        else:
            print("Opción no válida. Intenta de nuevo.")

def salir():
    print("Saliendo del programa...")
    sys.exit()

if __name__ == "__main__":
    menu()
