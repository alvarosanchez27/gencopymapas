import json

class ArbolDom():
    """
    Estructura de tipo Árbol contenedora de los Controles XAML.
    """
    def __init__(self, NodoRaiz):
        """
        Constructor de la estructura ArbolDom XAML.
        """
        self.NodoRaiz = NodoRaiz
    
    def agregaControlHijo(self, IdPadre, NodoControlHijo):
        """
        Método que agrega un control a un Control Padre.

        Parámetros:
            IdPadre -> Identificador del Control al que se agrega el hijo
            NodoControlHijo -> NodoControl a agregar al NodoPadre.
        """
        NodoControl = self.buscaNodoControl(IdPadre)
        if NodoControl is None:  raise Exception("Error!!! No se ha encontrado el Nodo Padre al que agregar el control")
        # Asignamos el idPadre al control hijo a agregar
        NodoControlHijo.IdPadre = IdPadre
        NodoControl.ListaNodoControlesHijos.append(NodoControlHijo)

    def toList(self, idControl):
        """
        Método que convierte el árbol a estructura lista de Controles desde un idControl. El idControl
        se incluye como el primer elemento de la lista.

        Parámetros:
            IdControl -> identificador del Control a partir del cual se retorna la lista de controles hijos,
                         si se informa a None, se toma por defecto el NodoRaiz.
        Retorno:
            list -> Lista de Controles hijos.
        """
        listaControlesHijos = list()
        if idControl is None:
            if self.NodoRaiz is None: raise Exception("Error!!! No existe un Nodo Raiz dentro del Arbol DOM.")
            if self.NodoRaiz.Control is None: raise Exception("Error!!! No existe un Control asociado al NodoRaiz del Arbol DOM")
            idControl = self.NodoRaiz.Control.ID
        NodoControl = self.buscaNodoControl(idControl)
        if NodoControl is None:  raise Exception("Error!!! No se ha encontrado el Nodo Con identificador {}".format(idControl))
        # Agregamos como primer elemento de la lista el NodoControl encontrado
        listaControlesHijos.append(NodoControl)
        return self.__listarNodosHijo(NodoControl,listaControlesHijos)

    def __listarNodosHijo(self,NodoControl,listaControlesHijos):
        """
        Método auxiliar que agrega a una lista todos los Nodos Hijos de un Control.
        El tratamiento es recursivo, y se agregaŕan a la lista todos los Nodos con ancestro común NodoControl.
        """
        if not NodoControl is None: 
            for ItemNodoHijo in NodoControl.ListaNodoControlesHijos:
                listaControlesHijos.append(ItemNodoHijo)
                if ItemNodoHijo.ListaNodoControlesHijos != None: 
                    listaControlesHijos = self.__listarNodosHijo(ItemNodoHijo,listaControlesHijos)                   
        return listaControlesHijos
        
    def buscaNodoControl(self,IdControl):
        """
        Método que retorna el NodoControl encontrado en el Árbol.

        Parámetros:
            IdControl -> identificador del Control a buscar
        Retorno:
            NodoControl -> NodoControl encontrado, o None en caso de no encontrarse el idControl
        """
        if not self.NodoRaiz is None: 
            if not self.NodoRaiz.Control is None:
                if self.NodoRaiz.Control.ID == IdControl: return self.NodoRaiz
                else: 
                    return self.__buscarNodosHijo(IdControl,self.NodoRaiz)
        return None

    def __buscarNodosHijo(self,IdControl, NodoControlPadre):
        """
        Método auxiliar para búsqueda de un control dentro de la lista de hijos.
        """
        if not IdControl is None: 
            for ItemNodoHijo in NodoControlPadre.ListaNodoControlesHijos:
                if ItemNodoHijo.Control.ID == IdControl: return ItemNodoHijo
                ItemFind = self.__buscarNodosHijo(IdControl, ItemNodoHijo)  
                if ItemFind != None: return ItemFind
        return None

    def getJSON(self):
        """
        Devolvemos el arbol en formato JSON
        """
        listaNodosArbol = list()
        if self.NodoRaiz != None:
            if self.NodoRaiz.Control != None:
                for itemNodoControl in self.toList(self.NodoRaiz.Control.ID):
                    listaNodosArbol.append(itemNodoControl.getJSON())
        return json.dumps({
                "Nodos": listaNodosArbol
            })