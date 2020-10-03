import json

class NodoControlModel():
    """
    Nodo Contenedor de Control XAML.
    """    
    def __init__(self, Control):
        """
        Constructor del Nodo Control.

        Para instanciar un Nodo se deben informar los parametros:
            IdPadre -> Identificador del nodo Padre
            Control -> Objeto Contenedor del Control      
        """
        self.IdPadre = None
        self.Control = Control
        self.ListaNodoControlesHijos = list()

    def getJSON(self):
        """
        Devolvemos el objeto en formato JSON
        """
        if self.Control != None:
            return {
                "IDPadre": self.IdPadre,
                "DetalleControl": self.Control.getJSON()
            }
        return ''