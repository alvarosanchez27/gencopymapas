import json

class ControlModel():
    """
    Clase definición de Control UI de la aplicación.
    """
    def __init__(self, ID, IDControl, TipoControl,  Nombre, Template, esSubControl, esRaizDOM, PropiedadesDefault):
        """
        Constructor del control UI.
        """
        self.ID = ID
        self.IDControl = IDControl
        self.TipoControl = TipoControl
        self.Nombre = Nombre
        self.Template = Template
        self.esSubControl = esSubControl
        self.esRaizDOM = esRaizDOM
        self.LineasOriginalesFileXAML =  list()
        # El control se inicializa con las propiedades por default
        self.listaPropiedades = PropiedadesDefault

    def getJSON(self):
        """
        Devolvemos el objeto en formato JSON
        """
        return {
            "ID": self.ID,
            "Nombre" : self.Nombre,
            "IDControl" : self.IDControl,
            "TipoControl" : self.TipoControl,
            "Template" : self.Template,
            "esSubControl": self.esSubControl,
            "esRaizDOM": self.esRaizDOM,
            "LineasOriginales" : self.LineasOriginalesFileXAML ,
            "listaPropiedades" : self.listaPropiedades 
        }