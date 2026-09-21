
# Lista de estudiantes con sus calificaciones y porcentaje de asistencia
estudiantes = [
    {"nombre": "Juan", "calificaciones": [7, 8, 9, 6], "asistencia": 90},
    {"nombre": "Maria", "calificaciones": [5, 6, 4, 7], "asistencia": 60},
    {"nombre": "Pedro", "calificaciones": [1, 9, 4, 7], "asistencia": 95},
    {"nombre": "Ana", "calificaciones": [6, 5, 7, 8], "asistencia": 85}
]

# Función para obtener el promedio
def obtener_promedio(calificaciones):
    total = sum(calificaciones)
    cantidad_notas = len(calificaciones)
    resultado = total / cantidad_notas
    return resultado

# Función para comprobar si el estudiante está regular
# Condiciones: asistencia >= 70 y promedio >= 6
def comprobar_regularidad(estudiante):
    promedio = obtener_promedio(estudiante["calificaciones"])
    porcentaje = estudiante["asistencia"]

    if porcentaje >= 70 and promedio >= 6:
        return True
    else:
        return False


# Mostrar el estado de cada estudiante
print("ESTADO DE LOS ESTUDIANTES")

for estudiante in estudiantes:

    regular = comprobar_regularidad(estudiante)
    promedio_final = obtener_promedio(estudiante["calificaciones"])

    print("Alumno:", estudiante["nombre"])
    print("Promedio:", promedio_final)
    print("Asistencia:", estudiante["asistencia"], "%")

    if regular:
        print("Estado: ESTÁ REGULAR")
    else:
        print("Estado: NO ESTÁ REGULAR")

    print("-------------------------")
