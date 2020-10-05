import os
import re
from libs.Controllers.Controles.LoaderDefControlesController import LoaderDefControlesController
from libs.Models.Dom.ArbolDom import ArbolDom
from libs.Models.Controles.ControlModel import ControlModel
from libs.Models.Dom.NodoControlModel import NodoControlModel

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
        # Identificador del padre inicializado a -1

        ArbolTmp, IdPadre, CntrlActual, CntrlTmp = None, None, None, None
        loaderDefiniciones = LoaderDefControlesController(self.Contexto)
        DiccionarioCtrls = loaderDefiniciones.getDiccionarioControles()
        if DiccionarioCtrls is None:
            self.Contexto.escribeLog(__class__.__name__,self.Contexto.TipoMsg.ERROR, "Error!!! No se ha generado correctamente el Diccionario de definición de Controles.")
            raise Exception("Error!!! No se ha generado correctamente el Diccionario de definición de Controles.")
        fileXAMLHandler = open(self.FilePrincipal,'r') 
        for lineaFileXAML in fileXAMLHandler:
            CntrlTmp = self.__getControlLinea(DiccionarioCtrls,CntrlActual, lineaFileXAML)
            if CntrlTmp != CntrlActual:
                # si no existe el padre, inicializamos el arbol con la raiz 
                if IdPadre is None: 
                    ArbolTmp = ArbolDom(NodoControlModel(CntrlTmp))
                    IdPadre = CntrlTmp.ID
                else: 
                    if not CntrlActual.esSubControl and CntrlTmp.esSubControl: IdPadre =  CntrlActual.ID
                    ArbolTmp.agregaControlHijo(IdPadre, NodoControlModel(CntrlTmp))
                CntrlActual = CntrlTmp 
            if CntrlActual != None: CntrlActual.LineasOriginalesFileXAML.append(lineaFileXAML)                
        fileXAMLHandler.close()
        return ArbolTmp

    def __getControlLinea(self, DiccionarioCtrls, ControlActual, linea):
        """
        Método auxiliar que retorna el Control procesado en la linea actual.

        Recibe como parámetro el Diccionario de controles, la linea actual del fichero XAML y el ControlActual.
        """
        try:
            for itemDefControles in DiccionarioCtrls:
                PatronIdentificaControl = re.compile(itemDefControles['Regex'],flags=re.I)
                if PatronIdentificaControl.search(linea):
                    return ControlModel('1', itemDefControles['IdControl'], itemDefControles['NombreControl'],  'Nombre', itemDefControles['TemplateSalida'], itemDefControles['esSubControl'])
            return ControlActual
        except Exception as e:
            self.Contexto.escribeLog(__class__.__name__,self.Contexto.TipoMsg.ERROR, "Error en creacion de Control desde linea de fichero!!!  {} ".format(str(e)))
            raise Exception("Error en creacion de Control desde linea de fichero!!!  {} ".format(str(e)))
