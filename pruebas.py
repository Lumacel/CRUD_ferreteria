import inspect

def funcion_a():
    print("Llamando a la función B desde la función", inspect.stack()[1].function)
    funcion_b()

def funcion_b():
    print("Esta es la función B")

funcion_a()