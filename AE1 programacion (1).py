#Deberás diseñar e implementar el sistema de un Cajero Automático que permita a un usuario gestionar su cuenta bancaria
saldo = 50000

opcion = 0

while opcion != 4:
    print("")
    print("      CAJERO AUTOMATICO")
    print("")
    print("1. Consultar saldo disponible")
    print("2. Depositar dinero")
    print("3. Extraer dinero")
    print("4. Salir del sistema")
    print("")

    opcion = int(input("Ingrese una opcion: "))

    if opcion == 1:
        print("Su saldo disponible es: $", saldo)

    elif opcion == 2:
        importe = float(input("Ingrese el importe a depositar: "))

        if importe > 0:
            saldo = saldo + importe
            print("Deposito realizado correctamente.")
            print("Su nuevo saldo es: $", saldo)
        else:
            print("El importe debe ser mayor a 0.")

    elif opcion == 3:
        importe = float(input("Ingrese el importe a extraer: "))

        if importe <= saldo and importe > 0:
            saldo = saldo - importe
            print("Extraccion realizada correctamente.")
            print("Su nuevo saldo es: $", saldo)
        elif importe > saldo:
            print("fondo insuficiente para realizar la operacion")
        else:
            print("El importe debe ser mayor a 0.")

    elif opcion == 4:
        print("Gracias por utilizar el cajero automatico.")

    else:
        print("Opcion invalida. Ingrese una opcion del 1 al 4.")