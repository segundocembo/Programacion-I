# ==============================================================================
# TRABAJO INTEGRADOR FINAL (AE4 / TIFAS) - 1° ANO ISI - UCP CORRIENTES (2026)
# Caso 1: Navegador de Rutas (Servicio de Reparto Urbano)
# Integrantes: Segundo Cemborain (DNI: 48.341.862)
#              Lisandro Joel Maidana (DNI: 48.399.702)
# Comision: A
# Asignaturas: Matematica Discreta | Ingenieria de Requerimientos | Programacion I
# ==============================================================================
# Nota de diseno: Se utilizan unicamente estructuras basicas de Python (listas,
# listas de listas, diccionarios, condicionales, ciclos, funciones y archivos)
# sin bibliotecas externas, conforme a los contenidos de 1° ano.
# ==============================================================================

INFINITO = 999999  # Valor centinela para representar ausencia de conexion o infinito
ARCHIVO_POR_DEFECTO = "red_corrientes.txt"


def crear_red_por_defecto():
    """
    Crea y devuelve la red inicial de 6 nodos (Corrientes) como una lista de
    nombres de ubicaciones y una matriz de adyacencia ponderada (lista de listas).
    Un valor 0 en la matriz indica que no hay arista directa entre nodos distintos
    (ni lazos en la diagonal principal).
    """
    nodos = [
        "Centro Distribucion (Ruta 12)",
        "Sucursal Centro (Junin)",
        "Sucursal Ferre (Av. 3 de Abril)",
        "Sucursal Costanera Sur",
        "Sucursal Molina Punta",
        "Sucursal Laguna Seca",
    ]
    # Matriz de adyacencia 6x6 (grafo no dirigido ponderado en kilometros)
    matriz = [
        [0, 7, 3, 0, 0, 14],   # 0: Centro Distribucion
        [7, 0, 2, 4, 6, 0],    # 1: Sucursal Centro
        [3, 2, 0, 8, 0, 9],    # 2: Sucursal Ferre
        [0, 4, 8, 0, 3, 2],    # 3: Sucursal Costanera Sur
        [0, 6, 0, 3, 0, 5],    # 4: Sucursal Molina Punta
        [14, 0, 9, 2, 5, 0],   # 5: Sucursal Laguna Seca
    ]
    return nodos, matriz


def crear_matriz_vacia(cantidad_nodos):
    """Genera una matriz cuadrada de tamano N x N inicializada en ceros."""
    matriz = []
    for _ in range(cantidad_nodos):
        fila = []
        for _ in range(cantidad_nodos):
            fila.append(0)
        matriz.append(fila)
    return matriz


def mostrar_ubicaciones(nodos):
    """Opcion 1: Lista todas las ubicaciones (vertices) disponibles con su codigo."""
    print("\n--- UBICACIONES DISPONIBLES EN LA RED ---")
    if len(nodos) == 0:
        print("No hay ubicaciones cargadas en el sistema.")
        return
    for i in range(len(nodos)):
        print(f"  [{i}] {nodos[i]}")
    print(f"Total de vertices |V| = {len(nodos)}")


def mostrar_matriz_adyacencia(nodos, matriz):
    """Opcion 2: Imprime la matriz de adyacencia ponderada en formato tabular."""
    print("\n--- MATRIZ DE ADYACENCIA PONDERADA (pesos en km, 0 = sin enlace) ---")
    n = len(nodos)
    if n == 0:
        print("La matriz esta vacia.")
        return

    # Encabezado de columnas
    encabezado = "     "
    for j in range(n):
        encabezado += f"{j:>4}"
    print(encabezado)
    print("     " + "-" * (4 * n))

    # Filas de la matriz
    for i in range(n):
        linea = f"[{i}] |"
        for j in range(n):
            linea += f"{matriz[i][j]:>4}"
        print(linea)


def consultar_conexiones(nodos, matriz):
    """
    Opcion 3: Muestra los nodos adyacentes (vecinos directos) y el peso de cada
    arista incidente para una ubicacion seleccionada por el usuario.
    """
    print("\n--- CONSULTAR CONEXIONES DE UNA UBICACION ---")
    mostrar_ubicaciones(nodos)
    idx = pedir_indice_ubicacion("Ingrese el codigo de la ubicacion a consultar: ", nodos)
    if idx == -1:
        return

    print(f"\nConexiones directas desde [{idx}] {nodos[idx]}:")
    grado = 0
    for j in range(len(nodos)):
        peso = matriz[idx][j]
        if peso > 0:
            print(f"  -> [{j}] {nodos[j]} (distancia: {peso} km)")
            grado += 1

    if grado == 0:
        print("  (Esta ubicacion no posee conexiones directas; es un vertice aislado).")
    else:
        print(f"Grado del vertice delta(v{idx}) = {grado}")


def pedir_indice_ubicacion(mensaje, nodos):
    """
    Solicita un codigo entero de ubicacion y valida que sea numerico y exista
    en la lista de nodos. Retorna el indice valido o -1 si la red esta vacia.
    """
    if len(nodos) == 0:
        print("Error: No hay ubicaciones cargadas.")
        return -1

    while True:
        entrada = input(mensaje).strip()
        if entrada == "":
            print("Error: Debe ingresar un numero de ubicacion.")
            continue
        # Validacion manual para aceptar solo digitos enteros no negativos
        es_entero = True
        for caracter in entrada:
            if caracter < "0" or caracter > "9":
                es_entero = False
                break
        if not es_entero:
            print("Error: Ingrese un numero entero valido (ej. 0, 1, 2...).")
            continue

        codigo = int(entrada)
        if 0 <= codigo < len(nodos):
            return codigo
        print(f"Error: Ubicacion inexistente. Ingrese un codigo entre 0 y {len(nodos) - 1}.")


def ingresar_origen(nodos):
    """Opcion 4: Permite seleccionar y validar el nodo de origen."""
    print("\n--- SELECCIONAR PUNTO DE ORIGEN ---")
    mostrar_ubicaciones(nodos)
    origen = pedir_indice_ubicacion("Ingrese el codigo del punto de origen: ", nodos)
    if origen != -1:
        print(f"Origen seleccionado: [{origen}] {nodos[origen]}")
    return origen


def ingresar_destino(nodos):
    """Opcion 5: Permite seleccionar y validar el nodo de destino."""
    print("\n--- SELECCIONAR PUNTO DE DESTINO ---")
    mostrar_ubicaciones(nodos)
    destino = pedir_indice_ubicacion("Ingrese el codigo del punto de destino: ", nodos)
    if destino != -1:
        print(f"Destino seleccionado: [{destino}] {nodos[destino]}")
    return destino


def dijkstra(matriz, origen, destino):
    """
    Implementacion desde cero del algoritmo de Dijkstra sobre matriz de adyacencia.
    Entradas:
      - matriz: lista de listas con pesos positivos (>0 si hay arista, 0 si no).
      - origen: indice del vertice inicial.
      - destino: indice del vertice final.
    Retorna un diccionario con:
      - 'encontrado': True si existe camino, False si no hay conexion.
      - 'camino': lista ordenada de indices desde origen hasta destino.
      - 'costo': costo total acumulado del camino minimo (o INFINITO si no existe).
      - 'pasos': lista de registros de cada iteracion para auditoria/validacion.
    """
    n = len(matriz)
    distancias = [INFINITO] * n       # L(v): etiqueta de distancia minima actual
    visitados = [False] * n           # Controla los vertices ya fijados (fuera de T)
    predecesores = [-1] * n           # Guarda el nodo previo en el camino optimo
    distancias[origen] = 0
    pasos = []

    for iteracion in range(n):
        # Paso 1: Seleccionar el vertice no visitado v con menor etiqueta L(v)
        menor_dist = INFINITO
        u = -1
        for i in range(n):
            if not visitados[i] and distancias[i] < menor_dist:
                menor_dist = distancias[i]
                u = i

        # Si no queda ningun vertice alcanzable, detener el algoritmo
        if u == -1:
            break

        visitados[u] = True
        pasos.append({
            "iteracion": iteracion + 1,
            "nodo_fijado": u,
            "distancia_fijada": distancias[u],
            "etiquetas": list(distancias),
        })

        # Si ya fijamos el destino, su distancia minima es definitiva
        if u == destino:
            break

        # Paso 2: Relajar todas las aristas adyacentes a u hacia nodos no visitados
        for v in range(n):
            peso = matriz[u][v]
            if peso > 0 and not visitados[v]:
                nueva_dist = distancias[u] + peso
                if nueva_dist < distancias[v]:
                    distancias[v] = nueva_dist
                    predecesores[v] = u

    # Verificar si el destino es alcanzable
    if distancias[destino] >= INFINITO:
        return {
            "encontrado": False,
            "camino": [],
            "costo": INFINITO,
            "pasos": pasos,
        }

    # Reconstruir el camino desde destino hacia origen usando predecesores
    camino_invertido = []
    actual = destino
    while actual != -1:
        camino_invertido.append(actual)
        actual = predecesores[actual]

    camino = []
    for i in range(len(camino_invertido) - 1, -1, -1):
        camino.append(camino_invertido[i])

    return {
        "encontrado": True,
        "camino": camino,
        "costo": distancias[destino],
        "pasos": pasos,
    }


def calcular_camino_optimo(nodos, matriz, origen, destino):
    """
    Opcion 6: Valida origen y destino y ejecuta Dijkstra para calcular el
    recorrido de menor costo.
    """
    print("\n--- CALCULO DEL CAMINO DE MENOR COSTO (DIJKSTRA) ---")
    if origen is None or destino is None:
        print("Error: Debe ingresar tanto el origen (opcion 4) como el destino (opcion 5) antes de calcular.")
        return None

    if origen == destino:
        print(f"Aviso: El origen y el destino coinciden en [{origen}] {nodos[origen]}.")
        print("No se requiere desplazamiento: el costo del recorrido es 0 km.")
        return {
            "encontrado": True,
            "camino": [origen],
            "costo": 0,
            "pasos": [],
        }

    resultado = dijkstra(matriz, origen, destino)
    if not resultado["encontrado"]:
        print(f"Resultado: NO EXISTE CONEXION entre [{origen}] {nodos[origen]} y [{destino}] {nodos[destino]}.")
    else:
        print("Calculo completado con exito.")
        print("Utilice las opciones 7 y 8 del menu para consultar el recorrido y su costo total.")
    return resultado


def mostrar_recorrido(nodos, matriz, resultado):
    """Opcion 7: Muestra el detalle tramo por tramo del recorrido encontrado."""
    print("\n--- RECORRIDO ENCONTRADO ---")
    if resultado is None:
        print("Aun no se ha calculado ninguna ruta. Ejecute la opcion 6 primero.")
        return
    if not resultado["encontrado"]:
        print("No existe un recorrido posible para el origen y destino seleccionados.")
        return

    camino = resultado["camino"]
    if len(camino) == 1:
        idx = camino[0]
        print(f"Origen y destino identicos: [{idx}] {nodos[idx]} (0 tramos).")
        return

    nombres_ruta = []
    for idx in camino:
        nombres_ruta.append(f"[{idx}] {nodos[idx]}")
    print("Ruta optima: " + "  ->  ".join(nombres_ruta))
    print("\nDetalle de tramos:")
    for i in range(len(camino) - 1):
        u = camino[i]
        v = camino[i + 1]
        peso = matriz[u][v]
        print(f"  Tramo {i + 1}: [{u}] {nodos[u]} -> [{v}] {nodos[v]} = {peso} km")


def mostrar_costo_total(resultado):
    """Opcion 8: Muestra el costo total acumulado del recorrido calculado."""
    print("\n--- COSTO TOTAL DEL RECORRIDO ---")
    if resultado is None:
        print("Aun no se ha calculado ninguna ruta. Ejecute la opcion 6 primero.")
        return
    if not resultado["encontrado"]:
        print("Costo total: Infinito (no existe camino entre las ubicaciones).")
        return
    print(f"Costo minimo acumulado: {resultado['costo']} km")


def guardar_red_en_archivo(nombre_archivo, nodos, matriz):
    """Guarda los nodos y las aristas (triangulo superior de la matriz) en un archivo."""
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write("# Red de rutas - Sistema Navegador de Rutas\n")
            archivo.write("NODOS\n")
            for i in range(len(nodos)):
                archivo.write(f"{i};{nodos[i]}\n")
            archivo.write("ARISTAS\n")
            n = len(nodos)
            for i in range(n):
                for j in range(i + 1, n):
                    if matriz[i][j] > 0:
                        archivo.write(f"{i};{j};{matriz[i][j]}\n")
        print(f"Red guardada correctamente en '{nombre_archivo}'.")
        return True
    except OSError as error:
        print(f"Error al guardar el archivo '{nombre_archivo}': {error}")
        return False


def cargar_red_desde_archivo(nombre_archivo):
    """Lee un archivo de red y reconstruye la lista de nodos y la matriz de adyacencia."""
    try:
        nodos_dict = {}
        aristas = []
        seccion = ""

        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea == "" or linea.startswith("#"):
                    continue
                if linea == "NODOS":
                    seccion = "NODOS"
                    continue
                if linea == "ARISTAS":
                    seccion = "ARISTAS"
                    continue

                partes = linea.split(";")
                if seccion == "NODOS" and len(partes) == 2:
                    idx = int(partes[0])
                    nombre = partes[1].strip()
                    nodos_dict[idx] = nombre
                elif seccion == "ARISTAS" and len(partes) == 3:
                    u = int(partes[0])
                    v = int(partes[1])
                    peso = int(partes[2])
                    if peso <= 0:
                        raise ValueError("Los pesos de las aristas deben ser positivos.")
                    aristas.append((u, v, peso))

        if len(nodos_dict) == 0:
            raise ValueError("El archivo no contiene nodos validos.")

        nodos = []
        for i in range(len(nodos_dict)):
            if i not in nodos_dict:
                raise ValueError(f"Falta el indice de nodo {i} en la secuencia.")
            nodos.append(nodos_dict[i])

        matriz = crear_matriz_vacia(len(nodos))
        for u, v, peso in aristas:
            if 0 <= u < len(nodos) and 0 <= v < len(nodos) and u != v:
                matriz[u][v] = peso
                matriz[v][u] = peso
            else:
                raise ValueError(f"Arista invalida ({u}, {v}).")

        print(f"Red cargada correctamente desde '{nombre_archivo}' ({len(nodos)} nodos, {len(aristas)} aristas).")
        return nodos, matriz
    except (OSError, ValueError) as error:
        print(f"Error al cargar el archivo '{nombre_archivo}': {error}")
        return None, None


def gestionar_archivos(nodos, matriz):
    """Opcion 9: Submenu para guardar la red actual o cargar una red desde archivo."""
    print("\n--- GESTION DE ARCHIVOS DE RED ---")
    print("  1. Guardar red actual en archivo")
    print("  2. Cargar red desde archivo")
    subopcion = input("Seleccione una opcion (1 o 2): ").strip()

    if subopcion == "1":
        nombre = input(f"Nombre del archivo [{ARCHIVO_POR_DEFECTO}]: ").strip()
        if nombre == "":
            nombre = ARCHIVO_POR_DEFECTO
        guardar_red_en_archivo(nombre, nodos, matriz)
        return nodos, matriz, False
    elif subopcion == "2":
        nombre = input(f"Nombre del archivo [{ARCHIVO_POR_DEFECTO}]: ").strip()
        if nombre == "":
            nombre = ARCHIVO_POR_DEFECTO
        nuevos_nodos, nueva_matriz = cargar_red_desde_archivo(nombre)
        if nuevos_nodos is not None:
            return nuevos_nodos, nueva_matriz, True
        return nodos, matriz, False
    else:
        print("Subopcion no valida. Regresando al menu principal.")
        return nodos, matriz, False


def mostrar_menu():
    """Imprime las 9 opciones requeridas del sistema y la opcion de salida."""
    print("\n============================================================")
    print("     NAVEGADOR DE RUTAS - CORRIENTES EXPRESS LOGISTICA")
    print("============================================================")
    print("  1. Mostrar todas las ubicaciones disponibles")
    print("  2. Mostrar la matriz de adyacencia")
    print("  3. Consultar las conexiones entre ubicaciones")
    print("  4. Ingresar un punto de origen")
    print("  5. Ingresar un punto de destino")
    print("  6. Calcular el camino de menor costo")
    print("  7. Mostrar el recorrido encontrado")
    print("  8. Mostrar el costo total del recorrido")
    print("  9. Guardar o cargar los datos de la red desde un archivo")
    print("  0. Salir")
    print("============================================================")


def ejecutar_programa():
    """Funcion principal que coordina el ciclo de ejecucion del menu."""
    # Al iniciar, intenta cargar el archivo por defecto; si no existe, usa la red base
    nodos, matriz = cargar_red_desde_archivo(ARCHIVO_POR_DEFECTO)
    if nodos is None:
        nodos, matriz = crear_red_por_defecto()
        print("Se inicializo la red urbana por defecto (6 ubicaciones en Corrientes).")

    origen = None
    destino = None
    ultimo_resultado = None

    while True:
        mostrar_menu()
        if origen is not None:
            print(f"  [Estado actual] Origen: [{origen}] {nodos[origen]}", end="")
        else:
            print("  [Estado actual] Origen: (sin definir)", end="")
        if destino is not None:
            print(f" | Destino: [{destino}] {nodos[destino]}")
        else:
            print(" | Destino: (sin definir)")

        opcion = input("\nSeleccione una opcion (0-9): ").strip()

        if opcion == "1":
            mostrar_ubicaciones(nodos)
        elif opcion == "2":
            mostrar_matriz_adyacencia(nodos, matriz)
        elif opcion == "3":
            consultar_conexiones(nodos, matriz)
        elif opcion == "4":
            origen = ingresar_origen(nodos)
            ultimo_resultado = None
        elif opcion == "5":
            destino = ingresar_destino(nodos)
            ultimo_resultado = None
        elif opcion == "6":
            ultimo_resultado = calcular_camino_optimo(nodos, matriz, origen, destino)
        elif opcion == "7":
            mostrar_recorrido(nodos, matriz, ultimo_resultado)
        elif opcion == "8":
            mostrar_costo_total(ultimo_resultado)
        elif opcion == "9":
            nodos, matriz, recargada = gestionar_archivos(nodos, matriz)
            if recargada:
                origen = None
                destino = None
                ultimo_resultado = None
        elif opcion == "0":
            print("\nGracias por utilizar el Navegador de Rutas. Hasta luego.")
            break
        else:
            print("Error: Opcion invalida. Por favor ingrese un numero entre 0 y 9.")


if __name__ == "__main__":
    ejecutar_programa()
