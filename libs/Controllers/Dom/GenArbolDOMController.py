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
    # Identificador por defecto del nodo raiz del DOM. (Pantalla)
    __IDX_DEFAULT_RAIZ_DOM = 1
    # Palabra reservada para localizar el IDX.
    __CTE_LOCALIZADOR_ID_CONTROL = 'IDX'

    def __init__(self, Contexto):
        """
        Constructor del Controlador Generador del Arbol DOM.
        """
        if not os.path.isfile(Contexto.RutaFileInput):
            Contexto.escribeLog(__class__.__name__,Contexto.TipoMsg.ERROR, "Error!!! No existe el fichero de entrada {} ".format(Contexto.RutaFileInput))
            raise Exception("Error!!! No existe el fichero de entrada {} ".format(Contexto.RutaFileInput))
        self.FilePrincipal = Contexto.RutaFileInput
        self.Contexto = Contexto

    def generaArbolDOM(self):
        """
        Método principal encargado de la generación del Arbol DOM.
        Se genera inicialmente el árbol con todos sus controles.
        Una vez generado el árbol se recorre cargando las propiedades.
        """
        ArbolTmp = self.__generaEstructuraControlesHijos()
        self.__generaPropiedadesControles(ArbolTmp)
        #ArbolTmp = 
        return ArbolTmp

    def __generaEstructuraControlesHijos(self):
        """
        Método delegado en la generación de la estructura de Controles en el Árbol DOM.
        """
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
                    # Validamos que el Nodo sea un Control que pueda ser raiz del DOM.
                    # Inicialmente solo el Control Pantalla esta definido como un nodo raiz.
                    if not CntrlTmp.esRaizDOM:
                        self.Contexto.escribeLog(__class__.__name__,self.Contexto.TipoMsg.ERROR, "Error!!! El control: {} cuyo tipo de control es: {} no puede ser un control raiz del DOM.".format(CntrlTmp.Nombre,CntrlTmp.TipoControl ))
                        raise Exception("Error!!! El control: {} cuyo tipo de control es: {} no puede ser un control raiz del DOM.".format(CntrlTmp.Nombre,CntrlTmp.TipoControl ))
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
                # Se ha encontrado una linea que identifica un nuevo control
                if PatronIdentificaControl.search(linea):
                    esSubControlBool = itemDefControles['esSubControl'].lower() == 's'
                    esRaizDOMBool =  itemDefControles['esRaizDOM'].lower() == 's'
                    # Buscamos el nombre en la linea procesada.
                    NombreCtrl = self.__getNombreControlEnlinea(itemDefControles['TipoControl'],linea)                                     
                    # Buscamos el idx en la linea procesada.
                    IDX = self.__getIDXControlEnlinea(linea)
                    # Si el IDX retornado es espacios y se trata de un control que puede ser Raiz del DOM,
                    # Asignamos un IDX por defecto, si no es un control raiz DOM, damos error por 
                    # IDX no encontrado.
                    if IDX == '': 
                        if esRaizDOMBool: 
                            IDX = GenArbolDOMController.__IDX_DEFAULT_RAIZ_DOM                     
                        else:
                            self.Contexto.escribeLog(__class__.__name__,self.Contexto.TipoMsg.ERROR, "Error!!! No se ha encontrado el idx para el control: {} tipoControl: {}".format(NombreCtrl,itemDefControles['TipoControl']))
                            raise Exception("Error!!! No se ha encontrado el idx para el control: {} tipoControl: {}".format(NombreCtrl,itemDefControles['TipoControl']))
                    return ControlModel(IDX, itemDefControles['IdControl'], itemDefControles['TipoControl'],  NombreCtrl , itemDefControles['TemplateSalida'], esSubControlBool , esRaizDOMBool, itemDefControles['PropiedadesDefault'])
            return ControlActual
        except Exception as e:
            self.Contexto.escribeLog(__class__.__name__,self.Contexto.TipoMsg.ERROR, "Error en creacion de Control desde linea de fichero!!!  {} ".format(str(e)))
            raise Exception("Error en creacion de Control desde linea de fichero!!!  {} ".format(str(e)))

    def __getNombreControlEnlinea(self,TipoControl, lineaFileXAML):
        """
        Método que obtiene el nombre de un control en la linea pasada por parámetro.

        El nombre de un control puede encontrarse con dos expresiones regulares:
            1 - TipoControl+' '+NombreControl
            2 - TipoControl+'='+NombreControl
        """
        NombreControl = ""
        patronControl = re.compile(TipoControl,flags=re.I)
        patronControlConIgual = re.compile(TipoControl+'\\s*=\\s*',flags=re.I)
        # Se realiza la validacion de formato TipoControl+'='+NombreControl
        patronNombreControlConAsignacion = re.compile('^\\s*'+TipoControl+'\\s*=\\s*'+'\\b(\\w)+\\b',flags=re.I)
        resultBqConAsignacion = patronNombreControlConAsignacion.search(lineaFileXAML)
        if resultBqConAsignacion: 
            NombreControl = patronControlConIgual.sub('',resultBqConAsignacion.group()).strip()            
        else:
            patronNombreControlConEspacio = re.compile('^\\s*'+TipoControl+'\\s+'+'\\b(\\w|=)+\\b',flags=re.I)
            resultBqConEspacio = patronNombreControlConEspacio.search(lineaFileXAML)
            if resultBqConEspacio: 
                NombreControl = patronControl.sub('',resultBqConEspacio.group()).strip()    
                if '=' in NombreControl:
                    self.Contexto.escribeLog(__class__.__name__,self.Contexto.TipoMsg.ERROR, "Error!!! Detectado un nombre de control con formato no admitido. NombreControl:  {} . Linea: {} ".format(NombreControl, lineaFileXAML))
                    raise Exception("Error!!! Detectado un nombre de control con formato no admitido. NombreControl:  {} ".format(NombreControl))
            else:
                self.Contexto.escribeLog(__class__.__name__,self.Contexto.TipoMsg.ERROR, "Error!!! No se ha podido determinar el nombre de control en la linea: {}".format(lineaFileXAML))
                raise Exception("Error!!! No se ha podido determinar el nombre de control en la linea: {}".format(lineaFileXAML))
        return NombreControl

    def __getIDXControlEnlinea(self,linea):
        """
        Método que obtiene el identificador único de cada control

        Un identificador de control es localizado por tener el formato IDX=''
        """
        IDX=''
        patronIDX = re.compile(GenArbolDOMController.__CTE_LOCALIZADOR_ID_CONTROL+'\\s*=\\s*',flags=re.I)
        # Se realiza la validacion de formato TipoControl+'='+NombreControl
        patronIDXASignacion = re.compile('\\s*'+GenArbolDOMController.__CTE_LOCALIZADOR_ID_CONTROL+'\\s*=\\s*'+'\\b(\\w)+\\b',flags=re.I)
        resultBqIDX = patronIDXASignacion.search(linea)
        if resultBqIDX: IDX = patronIDX.sub('',resultBqIDX.group()).strip() 
        return IDX

    def __generaPropiedadesControles(self, ArbolTmp):
        """
        Método delegado en la generación de las propiedades para los controles del Árbol.
        """
        PatronIdentificadorPropiedades = re.compile('\\b(\\w)+\\s*=\\s*(\\w)+\\b',flags=re.I)
        if ArbolTmp is None:
            self.Contexto.escribeLog(__class__.__name__,self.Contexto.TipoMsg.ERROR, "Error!!! No se pueden generar las propiedades de los controles al llegar una instancia de arbol nula")
            raise Exception("Error!!! No se pueden generar las propiedades de los controles al llegar una instancia de arbol nula")
        listaNodosControles = ArbolTmp.toList(None)
        for itemNodoControl in listaNodosControles:
            if not itemNodoControl.Control is None:
                # Se recorren las lineas originales del fichero XAML, generando objetos 
                # de propiedades dinámicas.
                for lineaInFileCtrl in itemNodoControl.Control.LineasOriginalesFileXAML:
                    resultBqPropiedad = PatronIdentificadorPropiedades.search(lineaInFileCtrl)
                    if resultBqPropiedad: 
                        PropiedadTmp = resultBqPropiedad.group().strip().split('=')
                        self.__agregaPropiedadAControl(PropiedadTmp[0].strip(), PropiedadTmp[1].strip(), itemNodoControl.Control.listaPropiedades)

    def __agregaPropiedadAControl(self, KeyPropiedad, ValuePropiedad, listaPropiedadesControl):
        """
        Método encargado de la carga de las propiedades de un control.

        Se valida si existe ya la propiedad dentro del control, en caso de existir se reemplaza por la última propiedad insertada.
        """
        # Se genera dinámicamente la propiedad del control
        ObjPropiedad= eval("{'"+KeyPropiedad+"':'"+ValuePropiedad+ "'}")
        listaPropiedadesControl.append(ObjPropiedad)