import modelo_ACF
import modelo_AMAYA
import modelo_ARGENTINA
import modelo_CFN_NISII
import modelo_DANIROX
import modelo_DIS_COS
import modelo_FLAVIO
import modelo_GUSTAVO_ELECT
import modelo_INTEGRAL
import modelo_LA_PLATA_LED
import modelo_LIMPIA_AVENIDA
import modelo_MASSOL
import modelo_MAURO_IMPORT

def normalizar(file, distribuidora):
    if distribuidora == "ACF":
        modelo_ACF.normalizar_lista(file, distribuidora)

    elif distribuidora == "AMAYA":
        modelo_AMAYA.normalizar_lista(file, distribuidora)

    elif distribuidora == "ARGENTINA":
        modelo_ARGENTINA.normalizar_lista(file, distribuidora)

    elif distribuidora == "CFN_NISII":
        modelo_CFN_NISII.normalizar_lista(file, distribuidora)
    
    elif distribuidora == "DANIROX":
        modelo_DANIROX.normalizar_lista(file, distribuidora)
    
    elif distribuidora == "DIS_COS":
        modelo_DIS_COS.normalizar_lista(file, distribuidora)

    elif distribuidora == "FLAVIO":
        modelo_FLAVIO.normalizar_lista(file, distribuidora)

    elif distribuidora == "GUSTAVO_ELECT":
        modelo_GUSTAVO_ELECT.normalizar_lista(file, distribuidora)
    
    elif distribuidora == "INTEGRAL":
        modelo_INTEGRAL.normalizar_lista(file, distribuidora)

    elif distribuidora == "LA_PLATA_LED":
        modelo_LA_PLATA_LED.normalizar_lista(file, distribuidora)

    elif distribuidora == "LIMPIA_AVENIDA":
        modelo_LIMPIA_AVENIDA.normalizar_lista(file, distribuidora)

    elif distribuidora == "MASSOL":
        modelo_MASSOL.normalizar_lista(file, distribuidora)

    elif distribuidora == "MAURO_IMPORT":
        modelo_MAURO_IMPORT.normalizar_lista(file, distribuidora)

    