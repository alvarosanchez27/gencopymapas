import json

class ControlModel():
    """
    Clase definición de Control UI de la aplicación.
    """
    def __init__(self, ID, IDControl, NombreControl,  Nombre, Template, LineasOriginalesFileXAML):
        """
        Constructor del control UI.
        """
        self.ID = ID
        self.IDControl = IDControl
        self.NombreControl = NombreControl
        self.Nombre = Nombre
        self.Template = Template
        self.LineasOriginalesFileXAML =  LineasOriginalesFileXAML
        self.listaPropiedades = list()

    def getJSON(self):
        """
        Devolvemos el objeto en formato JSON
        """
        return {
            "ID": self.ID,
            "Nombre" : self.Nombre,
            "IDControl" : self.IDControl,
            "NombreControl" : self.NombreControl,
            "Template" : self.Template,
            "LineasOriginales" : self.LineasOriginalesFileXAML ,
            "listaPropiedades" : self.listaPropiedades 
        }