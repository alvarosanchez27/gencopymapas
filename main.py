import os
import json
from libs.Models.Context.ContextModel import ContextModel
from libs.Controllers.Logs.LogController import LogController, TipoMensaje
from Aplicacion import Aplicacion
# Ruta relativa desde el fichero actual, hasta el fichero de configuración de la app.
__FILE__CONFIG = 'aplicacion.config.json'

def loadFileAppConfig(DirRootApp):
    """
    Función para el cargado de la configuración de la aplicación desde el archivo JSON.

    Parametros de entrada:
        DirRootApp -> Directorio Root en el que se está ejecutando la aplicación.

    Retorna un diccionario con los datos del fichero de configuracion
    """
    DiccionarioCfg = None
    FileConfig = os.path.join(DirRootApp,__FILE__CONFIG)
    if not os.path.isfile(FileConfig): raise Exception ("Error Grave!! No existe el fichero de configuracion {}".format(FileConfig))
    with open(FileConfig, 'r', encoding='utf-8') as FileConfigTmp:
        DiccionarioCfg = json.loads(FileConfigTmp.read())   
    if DiccionarioCfg is None: raise Exception ("Error Grave!! No se ha podido cargar el diccionario configuracion de la aplcicacion.")        
    return DiccionarioCfg

def validacionParamsEntrada(Args, Contexto):
    """
    Función delegada en la validación de parámetros de entrada.

    Parametros de entrada:
        Args -> Argumentos de entrada a la aplicación
        Contexto -> Contexto en el que se cargan dichos parametros de la aplicación.
    """
    ############################################
    # Validación de los argumentos de entrada
    ############################################
    if len(Args.fichero) == 0 : raise Exception("Error!!! Debe informar un nombre de fichero de entrada.")
    if len(Args.user) == 0 : raise Exception("Error!!! Se debe informar el usuario que inicia la aplicacion")
    Contexto.User = Args.user
    # En caso de informarse un directorio, este debe existir
    if len(Args.directorio) > 0 :
        if os.path.isdir(Args.directorio): raise Exception("Error!!! El directorio {} no es un directorio valido.".format(Args.directorio))
        Contexto.DirFileInput = Args.directorio
    # Si no se especifica un directorio de entrada, se pone como directorio el que se encuentra en la configuración.
    else: Contexto.DirFileInput = os.path.join(Contexto.DirRootApp , Contexto.ConfigApp["DirInput"])
    # Validacion de existencia del fichero de entrada
    FileInputCompleto = os.path.join(Contexto.DirFileInput, Args.fichero)
    if not os.path.isfile(FileInputCompleto ): raise Exception("Error!!! El fichero de entrada indicado {} no existe.".format(FileInputCompleto))
    Contexto.RutaFileInput = FileInputCompleto 
    Contexto.NameFileInput = Args.fichero
    # Si se informa un nombre de fichero de salida, lo cargamos al contexto.
    if len(Args.out) > 0 : Contexto.RutaFileOutput = Args.out
    else: Contexto.RutaFileOutput = os.path.join(Contexto.DirRootApp , Contexto.ConfigApp["DirOutput"],Args.fichero)
 
if __name__ == "__main__":
 # Cargamos la libreria de parseo de argumentos de entraada
    import argparse
    # Textos de ayuda mostrados con opción -h
    helpFichero='''
        (Obligatorio) Nombre de la copy xaml.
        Se indica exclusivamente el nombre del archivo
    '''
    helpUser='''
        (Obligatorio) Usuario que inicia el proceso.
    '''
    helpDirectorio='''
        (Opcional) Directorio de trabajo.
        Directorio donde encontrar el fuente del archivo copy pantalla XAML.
        En caso de no informarse se va a tomar por defecto el directorio que 
        se encuentra en la configuracion.
    '''
    helpOut='''
        (Opcional) Nombre del fichero copy cobol.
        En caso de no informarse el fichero de salida se genera, en el 
        directorio de salida parametrizado en la aplicacion, con el nombre
        del fichero de entrada.
    '''
    # Se realiza un parseo de los argumentos de entrada
    Parser = argparse.ArgumentParser()
    Parser.add_argument('--fichero', '-f', help=helpFichero, type= str, default= "")
    Parser.add_argument('--directorio', '-d', help=helpDirectorio, type= str, default= "")  
    Parser.add_argument('--out', '-o', help=helpOut, type= str, default= "")  
    Parser.add_argument('--user', '-u', help=helpUser, type= str, default= "")  
    try:  

        # Cargamos la ruta raiz de la app
        DirRootApp = os.path.dirname(os.path.realpath(__file__))
        # Cargamos en memoria la configuración especificada en el fichero JSON.
        ConfigApp = loadFileAppConfig(DirRootApp)
        # Se realiza el instanciado del contexto de la aplicación.
        Ctx = ContextModel(DirRootApp,ConfigApp )
        # Llamada a validación de los parametros de entrada.
        validacionParamsEntrada( Parser.parse_args(), Ctx )
        # Instanciamos el Log de la aplicación y lo cargamos al contexto.
        FileLogSesion = os.path.join(DirRootApp, ConfigApp['DirLog'], Ctx.NameFileInput.split('.')[0] + "_" + Ctx.idSesion + "." + ConfigApp['FormatoLog'] )
        # Creamos una instancia del log, y pasamos al contexto la funcion delegada en la escritura de log.
        logTmp = LogController( Ctx, FileLogSesion, ConfigApp['FormatoLog'] )
        Ctx.escribeLog = logTmp.escribeLog
        Ctx.TipoMsg = TipoMensaje
        # Se realiza el arranque de la aplicación, pasando el contexto como parámetro.
        AplicacionMain = Aplicacion(Ctx)
        AplicacionMain.runAplicacion()
    except Exception as e:
        print(str(e))
        exit(99)