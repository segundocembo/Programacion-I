# LOGIX - Analisis de dependencias entre modulos
# Programa integrador de Ingenieria de Requerimientos y Matematica Discreta y programacion I
#
# Funcionalidades implementadas:
#   RF-03: Analizar los modulos afectados al modificar un modulo.
#   RF-04: Detectar dependencias circulares entre modulos.
#   Matematica discreta: matriz de adyacencia y algoritmo de Warshall..
#---
# DATOS DE LOGIX

modulos = ["PED", "CLI", "INV", "ROB", "ASG", "RUT", "SEG", "ENT", "REP"]

# matriz_dependencias[i][j] = 1 si el modulo i depende directamente del modulo j
matriz_dependencias = [
    [0, 1, 1, 0, 1, 0, 0, 0, 0],  # PED depende de CLI, INV y ASG
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # CLI no depende de nadie
    [0, 0, 0, 1, 0, 0, 0, 0, 0],  # INV depende de ROB
    [0, 0, 1, 0, 0, 0, 0, 0, 0],  # ROB depende de INV
    [0, 0, 1, 0, 0, 1, 0, 0, 0],  # ASG depende de INV y RUT
    [0, 0, 0, 0, 0, 0, 1, 0, 0],  # RUT depende de SEG
    [0, 0, 0, 0, 1, 0, 0, 0, 0],  # SEG depende de ASG
    [1, 0, 0, 0, 0, 0, 1, 0, 0],  # ENT depende de PED y SEG
    [1, 0, 1, 0, 0, 0, 0, 1, 0]   # REP depende de PED, INV y ENT
]

# FUNCIONES DE MATEMATICA DISCRETA

def calcular_alcanzabilidad(matriz):
    """
    Devuelve la matriz de alcanzabilidad usando el algoritmo de Warshall.

    Si i puede llegar a k y k puede llegar a j, entonces i puede llegar a j.
    La matriz original no se modifica.
    """
    n = len(matriz)
    alcanzabilidad = []

    for i in range(n):
        fila = []
        for j in range(n):
            fila.append(matriz[i][j])
        alcanzabilidad.append(fila)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if alcanzabilidad[i][k] == 1 and alcanzabilidad[k][j] == 1:
                    alcanzabilidad[i][j] = 1

    return alcanzabilidad


def mostrar_matriz(matriz):
    """Muestra una matriz con los nombres de los modulos."""
    print("\nMatriz de alcanzabilidad A*:")
    encabezado = "     " + "  ".join(modulos)
    print(encabezado)

    for i in range(len(matriz)):
        valores = "  ".join(str(valor) for valor in matriz[i])
        print(modulos[i].ljust(5) + valores)



# FUNCIONES DE ANALISIS DE IMPACTO


def obtener_modulos_afectados(matriz_a_estrella, modulo):
    """
    Devuelve los modulos que dependen directa o indirectamente del modulo dado.

    Como las dependencias se representan en las filas, se busca la columna
    correspondiente al modulo seleccionado.
    """
    posicion = modulos.index(modulo)
    afectados = []

    for i in range(len(modulos)):
        if matriz_a_estrella[i][posicion] == 1:
            afectados.append(modulos[i])

    return afectados


def obtener_grupos_circulares(matriz_a_estrella):
    """
    Detecta grupos de modulos que participan en dependencias circulares.

    Un modulo pertenece a un ciclo cuando puede alcanzarse a si mismo. Dos
    modulos pertenecen al mismo grupo si ambos pueden alcanzarse mutuamente.
    """
    grupos = []

    for i in range(len(modulos)):
        if matriz_a_estrella[i][i] == 1:
            grupo = []

            for j in range(len(modulos)):
                if (matriz_a_estrella[i][j] == 1 and
                        matriz_a_estrella[j][i] == 1):
                    grupo.append(modulos[j])

            if grupo not in grupos:
                grupos.append(grupo)

    return grupos


def encontrar_ciclo(matriz, grupo):
    """Encuentra y devuelve un recorrido representativo de un ciclo."""
    inicio = modulos.index(grupo[0])

    def buscar(actual, camino):
        for siguiente in range(len(modulos)):
            if matriz[actual][siguiente] != 1:
                continue

            if modulos[siguiente] not in grupo:
                continue

            if siguiente == inicio:
                return camino + [siguiente]

            if siguiente not in camino:
                resultado = buscar(siguiente, camino + [siguiente])
                if resultado is not None:
                    return resultado

        return None

    recorrido = buscar(inicio, [inicio])

    if recorrido is None:
        return grupo

    return [modulos[posicion] for posicion in recorrido]


def elegir_modulo():
    """Solicita un modulo valido al usuario y devuelve su codigo."""
    modulo = input("\nRF-03 - Modulo a modificar: ").strip().upper()

    while modulo not in modulos:
        print("Modulo invalido. Modulos disponibles: " + ", ".join(modulos))
        modulo = input("Ingrese un modulo valido: ").strip().upper()

    return modulo


def analizar_modulo(matriz_a_estrella, grupos):
    """Muestra el impacto de modificar un modulo y sus posibles ciclos."""
    modulo = elegir_modulo()
    afectados = obtener_modulos_afectados(matriz_a_estrella, modulo)

    if len(afectados) > 0:
        print(
            "Si se modifica " + modulo + ", pueden verse afectados "
            + str(len(afectados)) + " modulos: " + ", ".join(afectados)
        )
    else:
        print(
            "Si se modifica " + modulo
            + ", no se ve afectado ningun modulo."
        )

    for grupo in grupos:
        if modulo in grupo:
            ciclo = " -> ".join(encontrar_ciclo(matriz_dependencias, grupo))
            print(
                "Atencion: " + modulo
                + " forma parte de una dependencia circular: " + ciclo
            )


def mostrar_ciclos(matriz_a_estrella):
    """Muestra los grupos y recorridos de dependencias circulares."""
    grupos = obtener_grupos_circulares(matriz_a_estrella)

    if len(grupos) == 0:
        print("\nRF-04 - No se detectaron dependencias circulares.")
        return grupos

    involucrados = []
    for grupo in grupos:
        for modulo in grupo:
            if modulo not in involucrados:
                involucrados.append(modulo)

    print(
        "\nRF-04 - Modulos involucrados en dependencias circulares: "
        + ", ".join(involucrados)
    )
    print("Dependencias circulares detectadas: " + str(len(grupos)))

    for numero in range(len(grupos)):
        ciclo = encontrar_ciclo(matriz_dependencias, grupos[numero])
        print("  Ciclo " + str(numero + 1) + ": " + " -> ".join(ciclo))

    return grupos



# PROGRAMA PRINCIPAL


def menu_principal():
    """Ejecuta el menu principal del analisis de dependencias."""
    matriz_a_estrella = calcular_alcanzabilidad(matriz_dependencias)
    grupos = obtener_grupos_circulares(matriz_a_estrella)
    opcion = ""

    while opcion != "0":
        print("\n===== LOGIX - Analisis de dependencias =====")
        print("1. Mostrar matriz de alcanzabilidad A*")
        print("2. Analizar modulos afectados al modificar un modulo (RF-03)")
        print("3. Detectar dependencias circulares (RF-04)")
        print("0. Salir")
        opcion = input("Elegir opcion: ").strip()

        if opcion == "1":
            mostrar_matriz(matriz_a_estrella)
        elif opcion == "2":
            analizar_modulo(matriz_a_estrella, grupos)
        elif opcion == "3":
            mostrar_ciclos(matriz_a_estrella)
        elif opcion == "0":
            print("Fin del programa.")
        else:
            print("Opcion invalida. Ingrese 1, 2, 3 o 0.")


if __name__ == "__main__":
    menu_principal()
