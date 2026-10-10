# Buffet de la Facultad - versión simple
#
# Datos:
#   codigos, nombres, precios -> 3 arrays paralelos (el producto i está en la posición i)
#   ventas[i][d]              -> matriz: unidades del producto i en el día d (0 = lunes)
# Archivos:
#   productos.txt -> código;nombre;precio   (maestro)
#   ventas.txt    -> día;código;cantidad    (movimientos, una línea por venta)

MAX = 20
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]


# ---------------- FUNCIONES (devuelven un valor) ----------------

def buscar(codigos, cant, codigo):
    # Devuelve la posición del código, o -1 si no está.
    # Recibe los arrays y cant porque necesita saber qué hay cargado.
    pos = -1
    for i in range(cant):
        if codigos[i] == codigo:
            pos = i
            break  # salida interna: ya lo encontré, no sigo
    return pos


def total_producto(ventas, i):
    # Suma la fila del producto i (los 5 días)
    total = 0
    for d in range(5):
        total = total + ventas[i][d]
    return total


def recaudacion_dia(ventas, precios, cant, d):
    # Suma la columna del día d, multiplicando cada cantidad por su precio
    total = 0
    for i in range(cant):
        total = total + ventas[i][d] * precios[i]
    return total


def cargar_producto(codigos, nombres, precios, cant, codigo, nombre, precio):
    # Agrega un producto. Devuelve la nueva cantidad (la misma si el código está repetido)
    if buscar(codigos, cant, codigo) != -1 or cant == MAX:
        return cant
    codigos[cant] = codigo
    nombres[cant] = nombre
    precios[cant] = precio
    return cant + 1


def leer_archivos(codigos, nombres, precios, ventas):
    # Lee los dos archivos al arrancar. Devuelve cuántos productos hay.
    cant = 0
    try:
        archivo = open("productos.txt", "r")
        for linea in archivo:
            partes = linea.strip().split(";")
            if len(partes) == 3:
                cant = cargar_producto(codigos, nombres, precios, cant,
                                       int(partes[0]), partes[1], int(partes[2]))
        archivo.close()
    except FileNotFoundError:
        print("Primer uso: no hay productos guardados.")

    try:
        archivo = open("ventas.txt", "r")
        for linea in archivo:
            partes = linea.strip().split(";")
            if len(partes) == 3:
                i = buscar(codigos, cant, int(partes[1]))
                if i != -1:
                    ventas[i][int(partes[0]) - 1] += int(partes[2])
        archivo.close()
    except FileNotFoundError:
        print("Primer uso: no hay ventas guardadas.")
    return cant


# ---------------- PROCEDIMIENTOS (no devuelven nada) ----------------

def mostrar_menu():
    print("\n1. Cargar producto")
    print("2. Registrar venta")
    print("3. Ver informes")
    print("4. Salir")


def registrar_venta(codigos, nombres, ventas, cant):
    dia = int(input("Día (1=lunes ... 5=viernes): "))
    codigo = int(input("Código del producto: "))
    cantidad = int(input("Cantidad: "))
    i = buscar(codigos, cant, codigo)
    if dia < 1 or dia > 5 or cantidad < 1:
        print("Día o cantidad inválidos.")
    elif i == -1:
        print("Ese producto no existe.")
    else:
        ventas[i][dia - 1] += cantidad  # si ya había ventas ese día, se suman
        archivo = open("ventas.txt", "a")  # se guarda enseguida
        archivo.write(str(dia) + ";" + str(codigo) + ";" + str(cantidad) + "\n")
        archivo.close()
        print("Venta registrada.")


def mostrar_informes(codigos, nombres, precios, ventas, cant):
    print("\n1) Unidades por producto")
    maximo = 0
    for i in range(cant):
        t = total_producto(ventas, i)
        print(nombres[i], ":", t)
        if t > maximo:
            maximo = t

    print("\n2) Recaudación por día")
    mejor = 0
    total_semana = 0
    for d in range(5):
        r = recaudacion_dia(ventas, precios, cant, d)
        print(DIAS[d], ": $", r)
        total_semana += r
        if r > mejor:
            mejor = r

    print("\n3) Más vendido y mejor día")
    if total_semana == 0:
        print("No hay ventas cargadas.")
    else:
        for i in range(cant):  # si hay empate se muestran todos
            if total_producto(ventas, i) == maximo:
                print("Más vendido:", nombres[i], "(", maximo, "unidades )")
        for d in range(5):
            if recaudacion_dia(ventas, precios, cant, d) == mejor:
                print("Mayor recaudación:", DIAS[d], "( $", mejor, ")")

    print("\n4) Productos sin ventas")
    for i in range(cant):
        if total_producto(ventas, i) == 0:
            print(nombres[i])

    print("\n5) Recaudación total: $", total_semana)


# ---------------- PROGRAMA PRINCIPAL ----------------

codigos = [0] * MAX
nombres = [""] * MAX
precios = [0] * MAX
ventas = [[0] * 5 for i in range(MAX)]

cant = leer_archivos(codigos, nombres, precios, ventas)

opcion = 0
while opcion != 4:  # while porque no se sabe cuántas veces va a usar el menú
    mostrar_menu()
    opcion = int(input("Opción: "))
    if opcion == 1:
        codigo = int(input("Código: "))
        nombre = input("Nombre: ")
        precio = int(input("Precio: "))
        nueva = cargar_producto(codigos, nombres, precios, cant, codigo, nombre, precio)
        if nueva == cant:
            print("Código repetido o no hay lugar.")
        else:
            cant = nueva
            archivo = open("productos.txt", "a")
            archivo.write(str(codigo) + ";" + nombre + ";" + str(precio) + "\n")
            archivo.close()
    elif opcion == 2:
        registrar_venta(codigos, nombres, ventas, cant)
    elif opcion == 3:
        mostrar_informes(codigos, nombres, precios, ventas, cant)

print("Datos guardados. Hasta mañana.")