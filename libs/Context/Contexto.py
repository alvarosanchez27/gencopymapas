import datetime
from random import randint

class Contexto():
    """
    Clase contexto de la aplicación.

    Contiene todos lo datos globales a transferir por el aplicativo.
    """
    def __init__(self, DirRootApp, ConfigApp):
        """
        Constructor de Contexto.

        Parametros de entrada:
            DirRootApp -> Directorio Principal de la Aplicación
            ConfigApp -> Instancia de la configuración de la Aplicación.
        """
        # Se genera un identificador único de sesion
        self.idSesion = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') +str(randint(1000,9999))
        # Directorio Principal de la Aplicación
        self.DirRootApp = DirRootApp
        # Instancia de Configuración de la aplicación.
        self.ConfigApp = ConfigApp
        # Hora acceso a la aplicación.
        self.FechaAcceso = datetime.datetime.now()
        # Directorio fichero de entrada.
        self.DirFileInput = ""
        # Ruta completa del fichero de entrada.
        self.RutaFileInput = ""
        # Ruta completa del fichero de salida.
        self.RutaFileOutput = ""
        # Usuario acceso aplicación.
        self.NomUser = ""
