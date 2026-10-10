
import json
import os

ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "asistencias_datos.json")
MINIMO = 75  # porcentaje mínimo para estar regular


# ---------- Archivo ----------
def cargar_datos(ruta):
    if not os.path.exists(ruta):
        return {}, [], {}  # el archivo no existe
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return datos["alumnos"], datos["clases"], datos["asistencia"]
    except ValueError:
        return {}, [], {}  # el archivo está vacío o dañado


def guardar_datos(ruta, alumnos, clases, asistencia):
    datos = {"alumnos": alumnos, "clases": clases, "asistencia": asistencia}
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=2)


# ---------- Alumnos ----------
def agregar_alumno(alumnos, clases, asistencia, nro, nombre):
    if nro == "" or nombre == "":
        print("El número de estudiante y el nombre no pueden estar vacíos.")
        return False
    if nro in alumnos:
        print("El número de estudiante", nro, "ya existe.")
        return False
    alumnos[nro] = nombre
    asistencia[nro] = ["-"] * len(clases)  # "-" en las clases anteriores
    print("Alumno agregado.")
    return True


def listar_alumnos(alumnos):
    if len(alumnos) == 0:
        print("No hay alumnos cargados.")
    for nro in alumnos:
        print(nro, "-", alumnos[nro])


# ---------- Clases y asistencia ----------
def fecha_valida(fecha):
    # formato AAAA-MM-DD
    return len(fecha) == 10 and fecha[4] == "-" and fecha[7] == "-"


def registrar_clase(alumnos, clases, asistencia, fecha, presentes):
    if not fecha_valida(fecha):
        print("Fecha inválida (use AAAA-MM-DD).")
        return False
    if fecha in clases:
        print("Ya existe una clase en esa fecha.")
        return False
    for nro in presentes:
        if nro not in alumnos:
            print("El número de estudiante", nro, "no existe.")
            return False
    clases.append(fecha)
    for nro in alumnos:
        if nro in presentes:
            asistencia[nro].append("P")
        else:
            asistencia[nro].append("A")
    print("Clase registrada.")
    return True


def porcentaje_alumno(asistencia, nro):
    presentes = asistencia[nro].count("P")
    ausentes = asistencia[nro].count("A")
    if presentes + ausentes == 0:
        return None  # todavía no hay clases para este alumno
    return presentes * 100 / (presentes + ausentes)


def presentes_en_clase(asistencia, clases, fecha):
    if fecha not in clases:
        return None
    i = clases.index(fecha)
    cantidad = 0
    for nro in asistencia:
        if asistencia[nro][i] == "P":
            cantidad = cantidad + 1
    return cantidad


def alumnos_en_riesgo(alumnos, asistencia):
    riesgo = []
    for nro in alumnos:
        p = porcentaje_alumno(asistencia, nro)
        if p is not None and p < MINIMO:
            riesgo.append(nro)
    return riesgo


def reporte_general(alumnos, clases, asistencia):
    print("Clases dictadas:", len(clases))
    for nro in alumnos:
        p = porcentaje_alumno(asistencia, nro)
        if p is None:
            print(nro, alumnos[nro], "- sin datos")
        elif p >= MINIMO:
            print(nro, alumnos[nro], "-", round(p, 1), "% - Regular")
        else:
            print(nro, alumnos[nro], "-", round(p, 1), "% - EN RIESGO")


# ---------- Menú ----------
def menu():
    alumnos, clases, asistencia = cargar_datos(ARCHIVO)
    while True:
        print()
        print("=== REGISTRO DE ASISTENCIAS ===")
        print("1. Agregar alumno")
        print("2. Ver alumnos")
        print("3. Tomar asistencia (nueva clase)")
        print("4. Porcentaje de asistencia de un alumno")
        print("5. Presentes en una clase")
        print("6. Reporte general")
        print("0. Guardar y salir")
        try:
            opcion = int(input("Opción: "))
        except ValueError:
            print("Ingrese un número.")
            continue

        if opcion == 1:
            nro = input("Número de estudiante: ")
            nombre = input("Nombre y apellido: ")
            agregar_alumno(alumnos, clases, asistencia, nro, nombre)
        elif opcion == 2:
            listar_alumnos(alumnos)
        elif opcion == 3:
            fecha = input("Fecha de la clase (AAAA-MM-DD): ")
            if not fecha_valida(fecha) or fecha in clases:
                print("Fecha inválida o ya registrada.")
            else:
                presentes = []
                for nro in alumnos:
                    r = ""
                    while r != "s" and r != "n":
                        r = input(alumnos[nro] + " (" + nro + ") ¿presente? (s/n): ")
                    if r == "s":
                        presentes.append(nro)
                registrar_clase(alumnos, clases, asistencia, fecha, presentes)
        elif opcion == 4:
            nro = input("Número de estudiante: ")
            if nro not in alumnos:
                print("El número de estudiante no existe.")
            else:
                p = porcentaje_alumno(asistencia, nro)
                if p is None:
                    print("Todavía no hay clases registradas.")
                else:
                    print(alumnos[nro], ":", round(p, 1), "% de asistencia")
        elif opcion == 5:
            fecha = input("Fecha (AAAA-MM-DD): ")
            n = presentes_en_clase(asistencia, clases, fecha)
            if n is None:
                print("No hay clase registrada en esa fecha.")
            else:
                print("Presentes:", n, "de", len(alumnos))
        elif opcion == 6:
            reporte_general(alumnos, clases, asistencia)
        elif opcion == 0:
            break
        else:
            print("Opción inexistente.")

    guardar_datos(ARCHIVO, alumnos, clases, asistencia)
    print("Datos guardados. ¡Hasta luego!")


menu()