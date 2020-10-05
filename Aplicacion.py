from libs.Controllers.Dom.GenArbolDOMController import GenArbolDOMController

class Aplicacion():
    """
    Clase principal de la aplicación para generación de copy cobol desde copy xaml.
    """
    def __init__(self, Contexto):
        """
        Clase constructor de la Aplicación.

        Recibe como parámetro un contexto inicializado.
        """
        if Contexto is None: 
            raise Exception("Error Grave!!! No se puede instanciar la aplicacion sin su contexto.")
        self.Contexto = Contexto

    def runAplicacion(self):
        """
        """
        self.Contexto.escribeLog(__class__.__name__,self.Contexto.TipoMsg.INFORMACION, "Se realiza el arranque de la aplicacion.")
        self.Contexto.escribeLog(__class__.__name__,self.Contexto.TipoMsg.INFORMACION, "Generacion de copy Cobol con origen file: {}".format(self.Contexto.RutaFileInput))
        # Se llama a la generación del árbol DOM.
        genArbolControlador = GenArbolDOMController(self.Contexto)
        ArbolDomGenerado = genArbolControlador.generaArbol()
        print(ArbolDomGenerado.getJSON())
