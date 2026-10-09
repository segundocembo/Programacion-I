import json


def registrar_jugadores():
  cantidad = int(input("¿Cuántos jugadores van a participar en el torneo?: "))
  jugadores = []

  for i in range(cantidad):
    print("\nRegistro del jugador", i + 1)
    nombre = input("Ingrese el nombre del jugador: ")
    categoria = input("Ingrese la categoría (ej. 4ª, 5ª, 6ª): ")
    jugadores.append({"nombre": nombre, "categoria": categoria})

  with open("inscriptos.json", "w", encoding="utf-8") as archivo:
    json.dump(jugadores, archivo, ensure_ascii=False, indent=2)


def leer_jugadores():
  nombres = []
  categorias = []

  with open("inscriptos.json", "r", encoding="utf-8") as archivo:
    jugadores = json.load(archivo)

  for jugador in jugadores:
    nombres.append(jugador["nombre"])
    categorias.append(jugador["categoria"])

  return nombres, categorias


def armar_parejas(nombres, categorias):
  cantidad_parejas = int(input("\n¿Cuántas parejas se van a armar?: "))
  nombres_parejas = []
  jugadores1 = []
  jugadores2 = []
  categorias1 = []
  categorias2 = []

  print("\n LISTA DE JUGADORES DISPONIBLES ")
  for i in range(len(nombres)):
    print("[", i, "]", nombres[i], "- Categoría:", categorias[i])

  for i in range(cantidad_parejas):
    print("\nArmando pareja", i + 1)
    nombre_pareja = input("Ingrese el nombre de la pareja (ej. 'Los Tanos'): ")
    print("Ingrese el número (índice) de los 2 jugadores que la integran:")
    indice1 = int(input("Índice del primer jugador: "))
    indice2 = int(input("Índice del segundo jugador: "))

    nombres_parejas.append(nombre_pareja)
    jugadores1.append(nombres[indice1])
    jugadores2.append(nombres[indice2])
    categorias1.append(categorias[indice1])
    categorias2.append(categorias[indice2])

  return nombres_parejas, jugadores1, jugadores2, categorias1, categorias2


def main():
  print("SISTEMA DE GESTIÓN - TORNEO DE PÁDEL ")
  registrar_jugadores()
  nombres_jugadores, categorias_jugadores = leer_jugadores()
  nombres_parejas, j1, j2, categoria1, categoria2 = armar_parejas(nombres_jugadores, categorias_jugadores)

  print("      RESUMEN DE PAREJAS INSCRIPTAS     ")
  for i in range(len(nombres_parejas)):
    print("Pareja:", nombres_parejas[i], "-> Integrantes:", j1[i], "(Categoría:", categoria1[i], ") y", j2[i], "(Categoría:", categoria2[i], ")")


if __name__ == "__main__":
  main()