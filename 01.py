#¿ Alumnos = ["Juan", "Maria", "Pedro", "Ana", "Luis"] pero yo quiero saber si esos estan o no estan regular ?

#¿ Que dictamina si un alumno esta o no esta regular ?

#Necesitamos tener las 4 notas alumnos para poder determinar si estan regulares o no.

#Y saber el % de asistencia de cada alumno.

# Definición del conjunto de alumnos utilizando registros (diccionarios) y arreglos (listas)
alumnos = [
    {"nombre": "Juan", "notas": [7, 8, 9, 6], "asistencia": 90},
    {"nombre": "Maria", "notas": [5, 6, 4, 7], "asistencia": 60},
    {"nombre": "Pedro", "notas": [1, 9, 4, 7], "asistencia": 95},
    {"nombre": "Ana", "notas": [6, 5, 7, 8], "asistencia": 85}
]

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