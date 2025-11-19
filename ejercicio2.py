try:
    n = int(input("Introduce un número: "))
    if n < 0:
        raise ValueError("El número no puede ser negativo.")

    resultado = 1
    while n > 1:
        resultado *= n
        n -= 2

    print("El doble factorial es:", resultado)

    
