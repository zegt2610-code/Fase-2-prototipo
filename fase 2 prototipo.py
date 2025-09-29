import time
from datetime import datetime
from threading import Thread

# Matriz de sesiones en memoria
# fila = [fecha(str), etiqueta(str), minutos(int), completada(bool)]
sesiones = []

# ---------------------------
# Utilidades de interfaz
# ---------------------------

def mostrar_menu():
    print("\n=== PROTOTIPO ANTI-DISTRACCIONES ===")
    print("1. Iniciar sesión de enfoque")
    print("2. Ver progreso acumulado")
    print("3. Ver historial de sesiones")
    print("4. Salir")
    return input("Elige una opción: ")

def checklist_previo():
    print("\nChecklist antes de empezar:")
    print(" Silenciar notificaciones")
    print(" Dejar el celular lejos")
    print(" Activar modo no molestar")
    input("\nPresiona ENTER para confirmar y empezar...")

def guardar_sesion(etiqueta, minutos, completada=True):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sesiones.append([fecha, etiqueta, int(minutos), bool(completada)])

def calcular_puntos():
    if len(sesiones) == 0:
        print("\nNo hay sesiones registradas todavía.")
        return
    total_min, sesiones_ok = 0, 0
    for fila in sesiones:
        if fila[3]:
            total_min += fila[2]
            sesiones_ok += 1
    puntos = total_min * 2
    print(f"\nHas completado {sesiones_ok} sesiones.")
    print(f"Tiempo total: {total_min} minutos.")
    print(f"Puntos acumulados: {puntos} ⭐")

def ver_historial():
    if len(sesiones) == 0:
        print("\nNo hay sesiones registradas todavía.")
        return
    print("\n--- Historial de sesiones ---")
    print("N° |        Fecha y hora        |   Etiqueta   | Min | Completada")
    print("---+----------------------------+-------------+-----+-----------")
    i = 1
    for fila in sesiones:
        fecha, etiqueta, minutos, completada = fila
        comp_txt = "SI" if completada else "NO"   # <<< MAYÚSCULAS COMO PEDISTE
        print(f"{i:>2} | {fecha:>26} | {etiqueta:^11} | {minutos:>3} | {comp_txt:^9}")
        i += 1

# ---------------------------
# Temporizador: terminar en cualquier momento con 's' + ENTER
# ---------------------------

def iniciar_temporizador(minutos_totales, etiqueta):
    """
    Cuenta hacia atrás segundo a segundo.
    Comando disponible:
      's' + ENTER -> terminar en cualquier momento.
    """
    print(f"\nIniciando sesión de {minutos_totales} minutos: {etiqueta}")
    print("Escribe 's' y presiona ENTER en cualquier momento para TERMINAR la sesión.")

    segundos_totales = minutos_totales * 60
    segundos_restantes = segundos_totales
    segundos_transcurridos = 0

    control = {"terminar": False}

    # Hilo que escucha el comando 's'
    def lector_comando():
        while (not control["terminar"]) and (segundos_restantes > 0):
            cmd = input().strip().lower()
            if cmd == "s":
                control["terminar"] = True
                print("\n Terminando sesión por solicitud del usuario...")

    th = Thread(target=lector_comando, daemon=True)
    th.start()

    # Bucle principal (sin while True)
    while (segundos_restantes > 0) and (not control["terminar"]):
        mins, secs = divmod(segundos_restantes, 60)
        print(f"\rTiempo restante: {mins:02d}:{secs:02d}  ", end="")
        time.sleep(1)
        segundos_restantes -= 1
        segundos_transcurridos += 1

    # Resumen y guardado
    minutos_reales = max(0, segundos_transcurridos // 60)

    if control["terminar"] and (segundos_restantes > 0):
        print("\nSesión terminada por el usuario antes de tiempo.")
        guardar_sesion(etiqueta, minutos_reales, completada=False)  #  NO
    elif segundos_restantes == 0:
        print("\n" + "="*58)
        print("   S E S I Ó N   C O M P L E T A D A   ¡Buen trabajo!")
        print("="*58 + "\n")
        guardar_sesion(etiqueta, minutos_totales, completada=True)  #  SI


# Programa principal
# ---------------------------

opcion = "0"
while opcion != "4":
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
