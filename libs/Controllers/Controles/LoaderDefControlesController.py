import os
import json

class LoaderDefControlesController():
    """
    Clase delegada en la carga de la definición de controles del fichero JSON.
    """
    def __init__(self, Contexto):
        """
        Método Constructor del cargador de definición de controles.

        Se valida la existencia del fichero de definicion de controles
        """
        self.DiccionarioControles = None
        FileDefinicionControles = os.path.join(Contexto.ConfigApp['DirData'],Contexto.ConfigApp['FileDefControles'] )
        if not os.path.isfile(FileDefinicionControles):
            Contexto.escribeLog(__class__.__name__,Contexto.TipoMsg.ERROR, "Error!!! No existe el fichero de definicion de controles {} ".format(FileDefinicionControles))
            raise Exception("Error!!! No existe el fichero de definicion de controles  {} ".format(FileDefinicionControles))
        try:
            with open(FileDefinicionControles,'r') as FileDefiniciones:
                self.DiccionarioControles = json.loads(FileDefiniciones.read())
        # Capturamos la excepción para escribir en el log y volver a propagarla
        except Exception as e:
            Contexto.escribeLog(__class__.__name__,Contexto.TipoMsg.ERROR, str(e))
            raise Exception(str(e))     

    def getDiccionarioControles(self):
        """
        Método getter del diccionario de controles
        """
        return self.DiccionarioControles
