import modelo_acf
import modelo_amaya
import modelo_argentina
import modelo_cedica
import modelo_cfn_nisii
import modelo_danirox
import modelo_dis_cos
import modelo_flavio
import modelo_gustavo_elect
import modelo_integral
import modelo_la_plata_led
import modelo_limpia_avenida
import modelo_los_pinos
import modelo_massol
import modelo_lucas_import
import modelo_suprabond

def normalizar(file, distribuidora):
    if distribuidora == "ACF":
        nuevo_archivo = modelo_acf.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "AMAYA":
        nuevo_archivo = modelo_amaya.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "ARGENTINA":
        nuevo_archivo = modelo_argentina.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "CEDICA":
        nuevo_archivo = modelo_cedica.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "CFN_NISII":
        nuevo_archivo = modelo_cfn_nisii.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "DANIROX":
        nuevo_archivo = modelo_danirox.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "DIS_COS":
        nuevo_archivo = modelo_dis_cos.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "FLAVIO":
        nuevo_archivo = modelo_flavio.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "GUSTAVO_ELECT":
        nuevo_archivo = modelo_gustavo_elect.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "INTEGRAL":
        nuevo_archivo = modelo_integral.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "LA_PLATA_LED":
        nuevo_archivo = modelo_la_plata_led.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "LIMPIA_AVENIDA":
        nuevo_archivo = modelo_limpia_avenida.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "LOS_PINOS":
        nuevo_archivo = modelo_los_pinos.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "MASSOL":
        nuevo_archivo = modelo_massol.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "LUCAS_IMPORT":
        nuevo_archivo = modelo_lucas_import.normalizar_lista(file, distribuidora)
        return nuevo_archivo

    elif distribuidora == "SUPRABOND":
        nuevo_archivo = modelo_suprabond.normalizar_lista(file, distribuidora)
        return nuevo_archivo
