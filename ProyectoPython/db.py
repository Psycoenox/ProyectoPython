# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:11:16 2024

@author: Marcell
"""

import sqlite3

conn = sqlite3.connect('Tienda.db')
cursor = conn.cursor()

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
