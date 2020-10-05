import unittest

from libs.Models.Dom.ArbolDom import ArbolDom
from libs.Models.Controles.ControlModel import ControlModel
from libs.Models.Dom.NodoControlModel import NodoControlModel

class TestArbolDOM(unittest.TestCase):

    def test_crea_arbol(self):
        """
        Test Creación de Arbol.

        Validación de instanciación distinta de None del NodoRaiz.
        """
        # Creamos el control que es el NodoRaiz
        NodoRaiz = NodoControlModel(ControlModel(1,1,'Pantalla','Pantalla1','Pantalla.template',False))
        ArbolTmp = ArbolDom(NodoRaiz)
        self.assertTrue(ArbolTmp!=None)
    
    def test_find_nodoRaiz(self):
        """
        Test Búsqueda NodoRaiz.
        
        Validación de instanciación distinta de Nodo buscado.
        """
        # Creamos el control que es el NodoRaiz
        NodoRaiz = NodoControlModel(ControlModel(1,1,'Pantalla','Pantalla1','Pantalla.template',False))
        ArbolTmp = ArbolDom(NodoRaiz)
        self.assertTrue(ArbolTmp.buscaNodoControl(1)!=None)

    def test_find_nodoRaizNombre(self):
        """
        Test Búsqueda NodoRaiz con validación por Nombre.
        
        Se valida que el Nombre del Nodo, es igual al Nombre del nodo que 
        buscamos por identificador.
        """
        # Creamos el control que es el NodoRaiz
        NodoRaiz = NodoControlModel(ControlModel(1,1,'Pantalla','PantallaPrueba','Pantalla.template',False))
        ArbolTmp = ArbolDom(NodoRaiz)
        self.assertEqual(ArbolTmp.buscaNodoControl(1).Control.Nombre,'PantallaPrueba')

    def test_agregaNodoHijo(self):
        """
        Test Agregación Nodo Hijo
        
        Se valida que el Nodo hijo insertado, se encuentra dentro del árbol.
        """
        # Creamos el control que es el NodoRaiz
        NodoRaiz = NodoControlModel(ControlModel(1,1,'Pantalla','PantallaPrueba','Pantalla.template',False))
        # Creamos el control que será el nodo hijo de nodo raiz
        NodoHijo = NodoControlModel(ControlModel(2,2,'Boton','Boton1','Boton.template',False))
        # Creamos el árbol con un NodoRaiz
        ArbolTmp = ArbolDom(NodoRaiz)
        # Se agrega el control hijo
        ArbolTmp.agregaControlHijo(1,NodoHijo)
        self.assertEqual(ArbolTmp.buscaNodoControl(2).Control.Nombre,'Boton1') 

    def test_findNodoHijo(self):
        """
        Test Búsqueda de Nodos hijos con profundidad 2
        
        Se realiza la búsqueda de un Nodo que se encuentra en profundidad Nivel 2
        """
        # Creamos el control que es el NodoRaiz
        NodoRaiz = NodoControlModel(ControlModel(1,1,'Pantalla','PantallaPrueba','Pantalla.template',False))
        # Creamos el control que será el nodo hijo de nodo raiz
        NodoHijo = NodoControlModel(ControlModel(2,2,'Lista','Lista1','Lista.template',False))
        NodoHijo2 = NodoControlModel(ControlModel(3,3,'Boton','Boton1','Boton.template',True))
        # Creamos el control que será el nodo hijo de nodo raiz
        NodoHijo3 = NodoControlModel(ControlModel(4,4,'Lista','Lista2','Lista.template',False))
        NodoHijo4 = NodoControlModel(ControlModel(5,5,'Boton','Boton2','Boton.template',True))
        # Creamos el árbol con un NodoRaiz
        ArbolTmp = ArbolDom(NodoRaiz)
        # Se agrega el control hijo
        ArbolTmp.agregaControlHijo(1,NodoHijo)
        ArbolTmp.agregaControlHijo(2,NodoHijo2)
        ArbolTmp.agregaControlHijo(1,NodoHijo3)
        ArbolTmp.agregaControlHijo(4,NodoHijo4)
        self.assertFalse(ArbolTmp.buscaNodoControl(5)==None) 

    def test_toListArbol(self):
        """
        Test Conversion del Arbol a Lista de Nodos
        
        Se comprueba que la longitud de la lista obtenida es igual al ńumero de nodos del árbol.
        """
        # Creamos el control que es el NodoRaiz
        NodoRaiz = NodoControlModel(ControlModel(1,1,'Pantalla','PantallaPrueba','Pantalla.template',False))
        # Creamos el control que será el nodo hijo de nodo raiz
        NodoHijo = NodoControlModel(ControlModel(2,2,'Boton','Boton1','Boton.template',False))
        # Creamos el árbol con un NodoRaiz
        ArbolTmp = ArbolDom(NodoRaiz)
        # Se agrega el control hijo
        ArbolTmp.agregaControlHijo(1,NodoHijo)
        # Se valida que la longitud de la lista es igual al número de nodos del árbol.
        self.assertEqual(len(ArbolTmp.toList(None)),2)

    def test_toListArbol1(self):
        """
        Test Conversion del Arbol a Lista de Nodos
        
        Se comprueba que la longitud de la lista obtenida es igual al ńumero de nodos del árbol.
        """
        # Creamos el control que es el NodoRaiz
        NodoRaiz = NodoControlModel(ControlModel(1,1,'Pantalla','PantallaPrueba','Pantalla.template',False))
        # Creamos el control que será el nodo hijo de nodo raiz
        NodoHijo = NodoControlModel(ControlModel(2,2,'Lista','Lista1','Lista.template',False))
        NodoHijo2 = NodoControlModel(ControlModel(3,3,'Boton','Boton1','Boton.template',True))
        # Creamos el control que será el nodo hijo de nodo raiz
        NodoHijo3 = NodoControlModel(ControlModel(4,4,'Lista','Lista2','Lista.template',False))
        NodoHijo4 = NodoControlModel(ControlModel(5,5,'Boton','Boton2','Boton.template',True))
        # Creamos el árbol con un NodoRaiz
        ArbolTmp = ArbolDom(NodoRaiz)
        # Se agrega el control hijo
        ArbolTmp.agregaControlHijo(1,NodoHijo)
        ArbolTmp.agregaControlHijo(2,NodoHijo2)
        ArbolTmp.agregaControlHijo(1,NodoHijo3)
        ArbolTmp.agregaControlHijo(4,NodoHijo4)
        # Se valida que la longitud de la lista es igual al número de nodos del árbol.
        self.assertEqual(len(ArbolTmp.toList(None)),5)

if __name__ == "__main__":
    unittest.main()