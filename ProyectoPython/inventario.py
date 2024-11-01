# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:11:18 2024

@author: Marcell
"""

from db import cursor, conn
from datetime import datetime


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

# Funciones relacionadas al inventario
def agregar_producto():
    # Lógica de agregar producto
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
