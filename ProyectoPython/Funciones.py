# -*- coding: utf-8 -*-
"""
Proyecto: Tienda Informática - Gestión de Inventario y Empleados
@author: Marcell
"""

# Importaciones
import sys
import json # Para el manejo de archivos
import sqlite3 # Para las base de datos
import csv # Para la exportacion de archivos .csv
from datetime import datetime # Para especificar el tiempo en los archivos csv

# Conexion de Base de datos
conn = sqlite3.connect('Tienda.db') # Esto lo que hara sera crearnos nuestos archivo.db
cursor = conn.cursor()

# Creacion de tablas para la base de datos
def inicializar_db():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Empleados (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        edad INTEGER,
                        tipo TEXT,
                        salario REAL
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Inventario (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tipo TEXT,
                        nombre TEXT,
                        estado TEXT,
                        precio_compra REAL,
                        precio_venta REAL
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS HistorialVentas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto_id INTEGER,
                    nombre_producto TEXT,
                    precio_venta REAL,
                    fecha_venta TEXT,
                    FOREIGN KEY (producto_id) REFERENCES Inventario (id)
                  )''')
    conn.commit()

# Clases para empleados
class Empleado:
    def __init__(self, nombre, edad, tipo, salario):
        self.nombre = nombre
        self.edad = edad
        self.tipo = tipo
        self.salario = salario

    def registrar_en_db(self):
        cursor.execute("INSERT INTO Empleados (nombre, edad, tipo, salario) VALUES (?, ?, ?, ?)",
                       (self.nombre, self.edad, self.tipo, self.salario))
        conn.commit()

# Clases para inventario
class Producto:
    def __init__(self, tipo, nombre, estado, precio_compra, precio_venta):
        self.tipo = tipo
        self.nombre = nombre
        self.estado = estado
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta

    def registrar_en_db(self):
        cursor.execute("INSERT INTO Inventario (tipo, nombre, estado, precio_compra, precio_venta) VALUES (?, ?, ?, ?, ?)",
                       (self.tipo, self.nombre, self.estado, self.precio_compra, self.precio_venta))
        conn.commit()

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        cursor.execute("UPDATE Inventario SET estado = ? WHERE nombre = ?", (self.estado, self.nombre))
        conn.commit()

# Funciones principales
def agregar_empleado():
    nombre = input("Nombre del empleado: ")
    edad = int(input("Edad: "))
    tipos_permitidos = ["Asalariado", "Hora"]
    print("Tipos permitidos:", tipos_permitidos)
    tipo = input("Tipo (elige uno de los anteriores): ")
    while tipo not in tipos_permitidos:
        print("Tipo no válido. Intenta de nuevo.")
        tipo = input("Tipo (elige uno de los anteriores): ")
    salario = float(input("Salario mensual o por hora: "))
    
    empleado = Empleado(nombre, edad, tipo, salario)
    empleado.registrar_en_db()
    print(f"Empleado {nombre} registrado correctamente.")

def agregar_producto():
    tipos_permitidos_producto = ["Ordenador", "Componente"]
    print("Tipos de producto permitidos:", tipos_permitidos_producto)
    tipo = input("Tipo de producto (elige uno de los anteriores): ")
    while tipo not in tipos_permitidos_producto:
        print("Tipo de producto no válido. Intenta de nuevo.")
        tipo = input("Tipo de producto (elige uno de los anteriores): ")

    nombre = input("Nombre del producto: ")
    estados_permitidos = ["Nuevo", "Usado", "Dañado"]
    print("Estados permitidos:", estados_permitidos)
    estado = input("Estado (elige uno de los anteriores): ")
    while estado not in estados_permitidos:
        print("Estado no válido. Intenta de nuevo.")
        estado = input("Estado (elige uno de los anteriores): ")

    precio_compra = float(input("Precio de compra: "))
    precio_venta = float(input("Precio de venta: "))

    producto = Producto(tipo, nombre, estado, precio_compra, precio_venta)
    producto.registrar_en_db()
    print(f"Producto {nombre} agregado al inventario.")

def listar_inventario():
    cursor.execute("SELECT * FROM Inventario")
    productos = cursor.fetchall()
    if productos:
        for prod in productos:
            print(f"ID: {prod[0]}, Tipo: {prod[1]}, Nombre: {prod[2]}, Estado: {prod[3]}, Precio Compra: {prod[4]}, Precio Venta: {prod[5]}")
    else:
        print("No hay productos en el inventario.")

def reparar_producto():
    producto_id = int(input("ID del producto a reparar: "))
    cursor.execute("SELECT estado FROM Inventario WHERE id = ?", (producto_id,))
    producto = cursor.fetchone()
    
    if producto and producto[0] == "Dañado":
        cursor.execute("UPDATE Inventario SET estado = 'Reparado' WHERE id = ?", (producto_id,))
        conn.commit()
        print("Producto reparado y actualizado.")
    else:
        print("Producto no encontrado o no necesita reparación.")

def vender_producto():
    producto_id = int(input("ID del producto a vender: "))
    cursor.execute("SELECT * FROM Inventario WHERE id = ?", (producto_id,))
    producto = cursor.fetchone()

    if producto:
        fecha_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO HistorialVentas (producto_id, nombre_producto, precio_venta, fecha_venta) VALUES (?, ?, ?, ?)",
                       (producto[0], producto[2], producto[5], fecha_venta))
        conn.commit()
        
        cursor.execute("DELETE FROM Inventario WHERE id = ?", (producto_id,))
        conn.commit()
        print(f"Producto vendido: ID: {producto[0]}, Nombre: {producto[2]}, Precio de venta: {producto[5]}")
        print("Producto eliminado del inventario y registrado en el historial de ventas.")
    else:
        print("Producto no encontrado.")

def ver_historial_ventas():
    cursor.execute("SELECT * FROM HistorialVentas")
    ventas = cursor.fetchall()
    if ventas:
        print("\n--- Historial de Ventas ---")
        for venta in ventas:
            print(f"ID Venta: {venta[0]}, Producto ID: {venta[1]}, Nombre: {venta[2]}, Precio Venta: {venta[3]}, Fecha: {venta[4]}")
    else:
        print("No se han registrado ventas.")

# Gestión de archivos
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

# Menú principal
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
    conn.close()
    sys.exit()
# Ejecutar menú
menu()
