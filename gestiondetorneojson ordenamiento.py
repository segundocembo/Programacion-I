import json

ARCHIVO_INSCRIPTOS = "inscriptos.json"
ARCHIVO_PAREJAS = "parejas.json"


# ---------------------------------------------------------------
# ACTIVIDAD 02: inscripción y armado de parejas (con JSON)
# ---------------------------------------------------------------

def registrar_jugadores():
  cantidad = int(input("¿Cuántos jugadores van a participar en el torneo?: "))
  jugadores = []

  for i in range(cantidad):
    print("\nRegistro del jugador", i + 1)
    nombre = input("Ingrese el nombre del jugador: ")
    categoria = input("Ingrese la categoría (ej. 4ª, 5ª, 6ª): ")
    jugadores.append({"nombre": nombre, "categoria": categoria})

  with open(ARCHIVO_INSCRIPTOS, "w", encoding="utf-8") as archivo:
    json.dump(jugadores, archivo, ensure_ascii=False, indent=2)


def leer_jugadores():
  nombres = []
  categorias = []

  with open(ARCHIVO_INSCRIPTOS, "r", encoding="utf-8") as archivo:
    jugadores = json.load(archivo)

  for jugador in jugadores:
    nombres.append(jugador["nombre"])
    categorias.append(jugador["categoria"])

  return nombres, categorias


def armar_parejas(nombres, categorias):
  cantidad_parejas = int(input("\n¿Cuántas parejas se van a armar?: "))
  parejas = []

  print("\n LISTA DE JUGADORES DISPONIBLES ")
  for i in range(len(nombres)):
    print("[", i, "]", nombres[i], "- Categoría:", categorias[i])

  for i in range(cantidad_parejas):
    print("\nArmando pareja", i + 1)
    nombre_pareja = input("Ingrese el nombre de la pareja (ej. 'Los Tanos'): ")
    print("Ingrese el número (índice) de los 2 jugadores que la integran:")
    indice1 = int(input("Índice del primer jugador: "))
    indice2 = int(input("Índice del segundo jugador: "))

    parejas.append({
      "nombre": nombre_pareja,
      "jugador1": nombres[indice1],
      "jugador2": nombres[indice2],
      "puntos": 0
    })

  guardar_parejas(parejas)
  print("\nRESUMEN DE PAREJAS INSCRIPTAS")
  for p in parejas:
    print("Pareja:", p["nombre"], "-> Integrantes:", p["jugador1"], "y", p["jugador2"])


# ---------------------------------------------------------------
# ACTIVIDAD 03: parejas y puntos en parejas.json
# ---------------------------------------------------------------

def guardar_parejas(parejas):
  with open(ARCHIVO_PAREJAS, "w", encoding="utf-8") as archivo:
    json.dump(parejas, archivo, ensure_ascii=False, indent=2)


def leer_parejas():
  with open(ARCHIVO_PAREJAS, "r", encoding="utf-8") as archivo:
    return json.load(archivo)


def cargar_puntos():
  parejas = leer_parejas()
  print("\nCARGA DE PUNTOS (se suman a los que ya tiene cada pareja)")
  for p in parejas:
    puntos = int(input("Puntos que gana " + p["nombre"] + " (tiene " + str(p["puntos"]) + "): "))
    p["puntos"] = p["puntos"] + puntos
  guardar_parejas(parejas)
  print("Puntos guardados en", ARCHIVO_PAREJAS)


# ---------------------------------------------------------------
# MÉTODOS DE ORDENAMIENTO (sin sort() ni sorted())
# Ambos reciben una COPIA de la lista y una función "va_antes(a, b)"
# que dice si a debe ir antes que b. Devuelven la lista ordenada y
# la cantidad de comparaciones e intercambios realizados.
# ---------------------------------------------------------------

def copiar_lista(lista):
  copia = []
  for elemento in lista:
    copia.append(elemento)
  return copia


def ordenar_seleccion(lista, va_antes):
  datos = copiar_lista(lista)
  comparaciones = 0
  intercambios = 0
  n = len(datos)

  for i in range(n - 1):
    pos_min = i
    for j in range(i + 1, n):
      comparaciones += 1
      if va_antes(datos[j], datos[pos_min]):
        pos_min = j
    # Como en la teoría: un intercambio por pasada (a veces consigo mismo)
    datos[i], datos[pos_min] = datos[pos_min], datos[i]
    intercambios += 1

  return datos, comparaciones, intercambios


def ordenar_burbuja(lista, va_antes):
  # Burbuja mejorada: con bandera, termina si una pasada no hace intercambios
  datos = copiar_lista(lista)
  comparaciones = 0
  intercambios = 0
  n = len(datos)
  i = 0
  hubo_intercambio = True

  while i < n - 1 and hubo_intercambio:
    hubo_intercambio = False
    for j in range(n - 1 - i):
      comparaciones += 1
      if va_antes(datos[j + 1], datos[j]):
        datos[j], datos[j + 1] = datos[j + 1], datos[j]
        intercambios += 1
        hubo_intercambio = True
    i = i + 1

  return datos, comparaciones, intercambios


# Criterios de ordenamiento

def alfabetico(a, b):
  return a["nombre"].lower() < b["nombre"].lower()


def categoria_y_nombre(a, b):
  if a["categoria"] != b["categoria"]:
    return a["categoria"] < b["categoria"]
  return a["nombre"].lower() < b["nombre"].lower()


def mayor_puntaje(a, b):
  return a["puntos"] > b["puntos"]


def leer_inscriptos():
  # Se lee del JSON en el orden de inscripción; el archivo NO se modifica.
  with open(ARCHIVO_INSCRIPTOS, "r", encoding="utf-8") as archivo:
    return json.load(archivo)


# ---------------------------------------------------------------
# PEDIDOS DEL CLIENTE
# ---------------------------------------------------------------

def pedido1_lista_alfabetica():
  ordenados, comp, inter = ordenar_seleccion(leer_inscriptos(), alfabetico)
  print("\nINSCRIPTOS EN ORDEN ALFABÉTICO (Selección)")
  for i in range(len(ordenados)):
    print(i + 1, "-", ordenados[i]["nombre"], "- Categoría:", ordenados[i]["categoria"])


def pedido2_lista_por_categoria():
  ordenados, comp, inter = ordenar_burbuja(leer_inscriptos(), categoria_y_nombre)
  print("\nJUGADORES POR CATEGORÍA (Burbuja)")
  categoria_actual = ""
  for jugador in ordenados:
    if jugador["categoria"] != categoria_actual:
      categoria_actual = jugador["categoria"]
      print("\nCategoría", categoria_actual)
    print("  -", jugador["nombre"])


def pedido3_tabla_posiciones():
  # Método elegido por el grupo: Selección (con va_antes = mayor puntaje)
  ordenadas, comp, inter = ordenar_seleccion(leer_parejas(), mayor_puntaje)
  print("\nTABLA DE POSICIONES")
  print("Puesto | Pareja | Puntos")
  for i in range(len(ordenadas)):
    print(i + 1, "|", ordenadas[i]["nombre"], "|", ordenadas[i]["puntos"])


def pedido4_comparar_metodos():
  inscriptos = leer_inscriptos()

  _, c1, i1 = ordenar_seleccion(inscriptos, alfabetico)
  _, c2, i2 = ordenar_burbuja(inscriptos, categoria_y_nombre)

  print("\nCOMPARACIÓN DE MÉTODOS (", len(inscriptos), "jugadores )")
  print("Pedido                  | Método    | Comparaciones | Intercambios")
  print("1. Orden alfabético     | Selección |", c1, "|", i1)
  print("2. Por categoría        | Burbuja   |", c2, "|", i2)

  # Extra: el otro método en cada pedido, para poder comparar en igualdad de condiciones
  _, c3, i3 = ordenar_burbuja(inscriptos, alfabetico)
  _, c4, i4 = ordenar_seleccion(inscriptos, categoria_y_nombre)
  print("\nMismo pedido con el otro método:")
  print("1. Orden alfabético     | Burbuja   |", c3, "|", i3)
  print("2. Por categoría        | Selección |", c4, "|", i4)


# ---------------------------------------------------------------
# MENÚ PRINCIPAL
# ---------------------------------------------------------------

def main():
  print("SISTEMA DE GESTIÓN - TORNEO DE PÁDEL")
  opcion = ""
  while opcion != "0":
    print("\n1. Inscribir jugadores")
    print("2. Armar parejas")
    print("3. Cargar puntos")
    print("4. Lista alfabética de inscriptos (Selección)")
    print("5. Lista por categoría (Burbuja)")
    print("6. Tabla de posiciones")
    print("7. Comparar métodos (comparaciones e intercambios)")
    print("0. Salir")
    opcion = input("Opción: ")

    try:
      if opcion == "1":
        registrar_jugadores()
      elif opcion == "2":
        nombres, categorias = leer_jugadores()
        armar_parejas(nombres, categorias)
      elif opcion == "3":
        cargar_puntos()
      elif opcion == "4":
        pedido1_lista_alfabetica()
      elif opcion == "5":
        pedido2_lista_por_categoria()
      elif opcion == "6":
        pedido3_tabla_posiciones()
      elif opcion == "7":
        pedido4_comparar_metodos()
    except FileNotFoundError:
      print("Falta un archivo JSON: primero inscribí jugadores y armá las parejas.")


if __name__ == "__main__":
  main()
