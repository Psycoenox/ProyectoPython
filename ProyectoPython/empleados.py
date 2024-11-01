# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:11:17 2024

@author: Marcell
"""

from db import cursor, conn

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
