from modelos_distribuidoras import *


def normalizar(file, distribuidora):
    if distribuidora == "ACF":
        nuevo_archivo = modelo_ACF.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "AMAYA":
        nuevo_archivo = modelo_AMAYA.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "ARGENTINA":
        nuevo_archivo = modelo_ARGENTINA.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "CEDICA":
        nuevo_archivo = modelo_CEDICA.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "CFN_NISII":
        nuevo_archivo = modelo_CFN_NISII.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "DANIROX":
        nuevo_archivo = modelo_DANIROX.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "DIS_COS":
        nuevo_archivo = modelo_DIS_COS.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "FLAVIO":
        nuevo_archivo = modelo_FLAVIO.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "GUSTAVO_ELECT":
        nuevo_archivo = modelo_GUSTAVO_ELECT.normalizar_lista(
            file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "INTEGRAL":
        nuevo_archivo = modelo_INTEGRAL.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "LA_PLATA_LED":
        nuevo_archivo = modelo_LA_PLATA_LED.normalizar_lista(
            file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "LIMPIA_AVENIDA":
        nuevo_archivo = modelo_LIMPIA_AVENIDA.normalizar_lista(
            file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "LOS_PINOS":
        nuevo_archivo = modelo_LOS_PINOS.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "MASSOL":
        nuevo_archivo = modelo_MASSOL.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "MAURO_IMPORT":
        nuevo_archivo = modelo_MAURO_IMPORT.normalizar_lista(
            file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "SUPRABOND":
        nuevo_archivo = modelo_SUPRABOND.normalizar_lista(file, distribuidora)
        return nuevo_archivo
