#Proyecto Algoritmos y Programación Básica
#Fase 2 - Prototipo funcional

#Idea: App sencilla de consola para ayudar a concentrarse en el estudio.
#Funciones:
#1. Temporizador (modo enfoque).
#2. Sistema de puntos por completar sesiones.
#3. Registro básico de sesiones en archivo CSV.


import time
import csv
import os
from datetime import datetime

# ----------------------------
# Funciones principales
# ----------------------------

def mostrar_menu():
    print("\n=== PROTOTIPO ANTI-DISTRACCIONES ===")
    print("1. Iniciar sesión de enfoque")
    print("2. Ver progreso acumulado")
    print("3. Salir")
    opcion = input("Elige una opción: ")
    return opcion


def checklist_previo():
    print("\nChecklist antes de empezar:")
    print(" Silenciar notificaciones")
    print(" Dejar el celular lejos")
    print(" Activar modo no molestar\n")
    input("Presiona ENTER para confirmar y empezar...")


def iniciar_temporizador(minutos, etiqueta):
    print(f"\nIniciando sesión de {minutos} minutos: {etiqueta}")
    segundos = minutos * 60
    for i in range(segundos, 0, -1):
        mins, secs = divmod(i, 60)
        tiempo = f"{mins:02d}:{secs:02d}"
        print(f"\rTiempo restante: {tiempo}", end="")
        time.sleep(1)
    print("\n¡Sesión completada! 🎉")


def guardar_sesion(etiqueta, minutos, completada=True):
    archivo = "sesiones.csv"
    existe = os.path.isfile(archivo)

    with open(archivo, mode="a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        if not existe:
            escritor.writerow(["fecha", "etiqueta", "minutos", "completada"])
        escritor.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           etiqueta, minutos, completada])


def calcular_puntos():
    archivo = "sesiones.csv"
    if not os.path.isfile(archivo):
        print("\nNo hay sesiones registradas todavía.")
        return

    total_min = 0
    sesiones = 0

    with open(archivo, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            if fila["completada"] == "True":
                total_min += int(fila["minutos"])
                sesiones += 1

    puntos = total_min * 2  # 2 puntos por cada minuto completado
    print(f"\nHas completado {sesiones} sesiones.")
    print(f"Tiempo total: {total_min} minutos.")
    print(f"Puntos acumulados: {puntos} ")


# ----------------------------
# Programa principal
# ----------------------------
while True:
    opcion = mostrar_menu()

    if opcion == "1":
        try:
            duracion = int(input("Duración de la sesión (minutos): "))
            etiqueta = input("Etiqueta de la sesión (ej. Matemática, Química): ")
            checklist_previo()
            iniciar_temporizador(duracion, etiqueta)
            guardar_sesion(etiqueta, duracion, True)
        except ValueError:
            print("Por favor, ingresa un número válido para la duración.")

    elif opcion == "2":
        calcular_puntos()

    elif opcion == "3":
        print("\nGracias por usar el prototipo. ¡Éxitos en tus estudios! 📚")
        break

    else:
        print("Opción no válida. Intenta otra vez.")