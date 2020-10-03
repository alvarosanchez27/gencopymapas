import os
from libs.Controllers.Controles.LoaderDefControlesController import LoaderDefControlesController
from libs.Models.Dom.ArbolDom import ArbolDom

class GenArbolDOMController():
    """
    Clase Delegada en la generación de una estructura de tipo árbol, a partir de un
    fichero de definición XAML.
    """
    def __init__(self, Contexto):
        """
        Constructor del Controlador Generador del Arbol DOM.
        """
        if not os.path.isfile(Contexto.RutaFileInput):
            Contexto.escribeLog(__class__.__name__,Contexto.TipoMsg.ERROR, "Error!!! No existe el fichero de entrada {} ".format(Contexto.RutaFileInput))
            raise Exception("Error!!! No existe el fichero de entrada {} ".format(Contexto.RutaFileInput))
        self.FilePrincipal = Contexto.RutaFileInput
        self.Contexto = Contexto

    def generaArbol(self):
        """
        Método principal encargado de la generación del Arbol DOM.
        """
        loaderDefiniciones = LoaderDefControlesController(self.Contexto)
        DiccionarioCtrls = loaderDefiniciones.getDiccionarioControles()
        if DiccionarioCtrls is None:
            self.Contexto.escribeLog(__class__.__name__,self.Contexto.TipoMsg.ERROR, "Error!!! No se ha generado correctamente el Diccionario de definición de Controles.")
            raise Exception("Error!!! No se ha generado correctamente el Diccionario de definición de Controles.")
        return ""
