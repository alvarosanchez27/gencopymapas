import os


def loadFileAppConfig():
    """
    Función para el cargado de la configuración de la aplicación desde el archivo JSON.
    """
    pass


def validacionParamsEntrada(args):
    """
    Función delegada en la validación de parámetros de entrada
    """
    ############################################
    # Validación de los argumentos de entrada
    ############################################
    if len(args.fichero) == 0 : 
        print("Error!!! Debe informar el archivo que desea tratar.")
        print("Puede obtener más información consultando la ayuda del script.(-h)")
        exit(10)

if __name__ == "__main__":
 # Cargamos la libreria de parseo de argumentos de entraada
    import argparse
    # Textos de ayuda mostrados con opción -h
    helpFichero='''
        (Obligatorio) Nombre de la copy xaml.
        Se indica exclusivamente el nombre del archivo
    '''
    helpDirectorio='''
        (Opcional) Directorio de trabajo.
        Directorio donde encontrar el fuente del archivo copy pantalla XAML.
        En caso de no informarse se va a tomar por defecto el directorio que 
        se encuentra en la configuracion.
    '''
    # Se realiza un parseo de los argumentos de entrada
    parser = argparse.ArgumentParser()
    parser.add_argument('--fichero', '-f', help=helpFichero, type= str, default= "")
    parser.add_argument('--directorio', '-d', help=helpDirectorio, type= str, default= "")    
    # Llamada a validación de los parametros de entrada
    validacionParamsEntrada(parser.parse_args())

