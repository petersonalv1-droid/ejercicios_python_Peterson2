ano = int(input("Escribe un número: "))
if (ano%4 == 0 & ano%100 != 0) or (ano%400):
    print(f"{ano} es un año bisiesto!")
else:
    print(f"{ano} no es un año bisiesto!")
