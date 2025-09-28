#Proyecto Algoritmos y Programación Básica
#Fase 2 - Prototipo funcional 

#Funcionalidades:
#1. Temporizador de estudio
#2. Puntos acumulados
#3. Historial de sesiones (matriz)


import time
from datetime import datetime

# Matriz para guardar sesiones
# Cada fila: [fecha, etiqueta, minutos, completada]
sesiones = []

# ---------------------------
# Funciones
# ---------------------------

def mostrar_menu():
    print("PROTOTIPO ANTI-DISTRACCIONES")
    print("1. Iniciar sesión de enfoque")
    print("2. Ver progreso acumulado")
    print("3. Ver historial de sesiones")
    print("4. Salir")
    opcion = input("Elige una opción: ")
    return opcion


def checklist_previo():
    print("\nChecklist antes de empezar:")
    print("Silenciar notificaciones")
    print("Dejar el celular lejos")
    print("Activar modo no molestar")
    input("\nPresiona ENTER para confirmar y empezar...")


def iniciar_temporizador(minutos, etiqueta):
    print(f"\nIniciando sesión de {minutos} minutos: {etiqueta}")
    segundos = minutos * 60
    for i in range(segundos, 0, -1):
        mins, secs = divmod(i, 60)
        tiempo = f"{mins:02d}:{secs:02d}"
        print(f"\rTiempo restante: {tiempo}", end="")
        time.sleep(1)
    print("\n¡Sesión completada!")


def guardar_sesion(etiqueta, minutos, completada=True):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sesiones.append([fecha, etiqueta, minutos, completada])


def calcular_puntos():
    if len(sesiones) == 0:
        print("\nNo hay sesiones registradas todavía.")
        return

    total_min = 0
    sesiones_ok = 0

    for fila in sesiones:
        if fila[3] is True:  # completada
            total_min += fila[2]
            sesiones_ok += 1

    puntos = total_min * 2
    print(f"\nHas completado {sesiones_ok} sesiones.")
    print(f"Tiempo total: {total_min} minutos.")
    print(f"Puntos acumulados: {puntos} ")


def ver_historial():
    if len(sesiones) == 0:
        print("\nNo hay sesiones registradas todavía.")
        return

    print("\n--- Historial de sesiones ---")
    print("N° |        Fecha y hora        |   Etiqueta   | Min | Completada")
    print("---+----------------------------+-------------+-----+-----------")
    for i, fila in enumerate(sesiones, start=1):
        fecha, etiqueta, minutos, completada = fila
        comp_txt = "Sí" if completada else "No"
        print(f"{i:>2} | {fecha:>26} | {etiqueta:^11} | {minutos:>3} | {comp_txt:^9}")


# ---------------------------
# Programa principal
# ---------------------------

opcion = "0"
while opcion != "4":   # se detiene cuando la opción es 4
    opcion = mostrar_menu()

    if opcion == "1":
        try:
            duracion = int(input("Duración de la sesión (minutos): "))
            if duracion <= 0:
                print("La duración debe ser positiva.")
                continue
            etiqueta = input("Etiqueta de la sesión (ej. Matemática, Química): ").strip()
            if etiqueta == "":
                etiqueta = "Estudio"
            checklist_previo()
            iniciar_temporizador(duracion, etiqueta)
            guardar_sesion(etiqueta, duracion, True)
        except ValueError:
            print("Por favor, ingresa un número válido.")

    elif opcion == "2":
        calcular_puntos()

    elif opcion == "3":
        ver_historial()

    elif opcion == "4":
        print("\nGracias por usar el prototipo. ¡Éxitos en tus estudios!")

    else:
        print("Opción no válida. Intenta otra vez.")
