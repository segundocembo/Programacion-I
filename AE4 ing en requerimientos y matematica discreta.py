MODULOS = ["PED", "CLI", "INV", "ROB", "ASG", "RUT", "SEG", "ENT", "REP"]
DEPENDENCIAS = {
    "PED": ["CLI", "INV", "ASG"],
    "CLI": [],
    "INV": ["ROB"],
    "ROB": ["INV"],
    "ASG": ["RUT", "INV"],
    "RUT": ["SEG"],
    "SEG": ["ASG"],
    "ENT": ["PED", "SEG"],
    "REP": ["PED", "ENT", "INV"],
}


def construir_matriz():
    n = len(MODULOS)
    A = [[0] * n for _ in range(n)]
    for origen, destinos in DEPENDENCIAS.items():
        for destino in destinos:
            A[MODULOS.index(origen)][MODULOS.index(destino)] = 1
    return A


def warshall(A):
    n = len(A)
    R = [fila[:] for fila in A]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if R[i][k] == 1 and R[k][j] == 1:
                    R[i][j] = 1
    return R


def modulos_afectados(R, modulo):
    j = MODULOS.index(modulo)
    return [MODULOS[i] for i in range(len(MODULOS)) if R[i][j] == 1]


def grupos_circulares(R):
    grupos = []
    for i in range(len(MODULOS)):
        if R[i][i] == 1:
            grupo = [MODULOS[j] for j in range(len(MODULOS)) if R[i][j] == 1 and R[j][i] == 1]
            if grupo not in grupos:
                grupos.append(grupo)
    return grupos


def encontrar_ciclo(A, grupo):
    inicio = MODULOS.index(grupo[0])

    def buscar(actual, camino):
        for j in range(len(MODULOS)):
            if A[actual][j] == 1 and MODULOS[j] in grupo:
                if j == inicio:
                    return camino + [j]
                if j not in camino:
                    resultado = buscar(j, camino + [j])
                    if resultado:
                        return resultado
        return None

    return [MODULOS[i] for i in buscar(inicio, [inicio])]


def main():
    A = construir_matriz()
    R = warshall(A)

    print("Matriz de alcanzabilidad A*:")
    print("     " + " ".join(MODULOS))
    for i, fila in enumerate(R):
        print(MODULOS[i] + "  " + "   ".join(str(x) for x in fila))

    grupos = grupos_circulares(R)
    if grupos:
        involucrados = [m for grupo in grupos for m in grupo]
        print("\nRF4 - Módulos involucrados en dependencias circulares:", ", ".join(involucrados))
        print("Dependencias circulares detectadas:", len(grupos))
        for numero, grupo in enumerate(grupos, start=1):
            print(f"  Ciclo {numero}: {' -> '.join(encontrar_ciclo(A, grupo))}")
    else:
        print("\nRF4 - No se detectaron dependencias circulares.")

    modulo = input("\nRF3 - Módulo a modificar: ").strip().upper()
    while modulo not in MODULOS:
        modulo = input("Módulo inválido, probá de nuevo: ").strip().upper()
    afectados = modulos_afectados(R, modulo)
    if afectados:
        print(f"Si se modifica {modulo} pueden verse afectados {len(afectados)} módulos: {', '.join(afectados)}")
    else:
        print(f"Si se modifica {modulo} no se ve afectado ningún módulo (ningún módulo depende de él).")
    for grupo in grupos:
        if modulo in grupo:
            print(f"Atención: {modulo} forma parte de la dependencia circular {' -> '.join(encontrar_ciclo(A, grupo))}")


main()
