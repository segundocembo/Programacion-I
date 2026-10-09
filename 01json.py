import json

# json.load() convierte el contenido JSON en una lista de diccionarios de Python.
with open("alumnos.json", "r", encoding="utf-8") as archivo:
    alumnos = json.load(archivo)

# Función para calcular el promedio de una lista de notas
def calcular_promedio(notas):
    suma = sum(notas)
    cantidad = len(notas)
    promedio = suma / cantidad
    return promedio

# Función para determinar si un alumno está regular
# Criterio: Asistencia >= 70 Y Promedio >= 6
def evaluar_regularidad(alumno):
    promedio_notas = calcular_promedio(alumno["notas"])
    asistencia = alumno["asistencia"]
    
    if asistencia >= 70 and promedio_notas >= 6:
        return True
    else:
        return False

# Proceso principal para recorrer el arreglo de alumnos y mostrar el estado
print("ESTADO DE REGULARIDAD DE LOS ALUMNOS")
for alumno in alumnos:
    es_regular = evaluar_regularidad(alumno)
    promedio = calcular_promedio(alumno["notas"])
    
    print(f"Alumno: {alumno['nombre']}")
    print(f"Promedio de notas: {promedio}")
    print(f"Asistencia: {alumno['asistencia']}%")
    
    if es_regular:
        print("Estado: ESTÁ REGULAR")
    else:
        print("Estado: NO ESTÁ REGULAR")