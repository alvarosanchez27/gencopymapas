import json
import os
import re
import datetime


class TipoMensaje():
    """
    Clase que contiene la tipologia de Mensajes de log
    """
    ERROR="ERROR"
    AVISO="AVISO"
    INFORMACION="INFORMACION"

class LogModel():
    """
    Clase que contiene el formato de detalle de linea a escribir en el log.
    """
    # Delimitador de campos en formato string 
    __DELIMITADOR_CAMPO=";"

    def __init__(self, Clase, TipoError, DetalleError, Usuario):
        """
        Constructor del POJO de Modelo log
        """
        self.Usuario = Usuario 
        self.Clase = Clase
        self.TipoError = TipoError
        self.DetalleError = DetalleError

    def __str__(self):
        """
        Retorno del Modelo de Log en formato string. con delimitador de campos.
        """
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + LogModel.__DELIMITADOR_CAMPO + self.Usuario + LogModel.__DELIMITADOR_CAMPO  + self.TipoError + LogModel.__DELIMITADOR_CAMPO + self.Clase + LogModel.__DELIMITADOR_CAMPO + self.DetalleError + LogModel.__DELIMITADOR_CAMPO

    def getJSON(self):
        """
        Retorno del Modelo de Log en formato JSON.
        """
        return {

            "Fecha": datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'),
            "Usuario": self.Usuario ,
            "Clase": self.Clase,
            "TipoError": self.TipoError,
            "DetalleError": self.DetalleError         
        }

class LogController():
    """
    Clase delegada el manejo del log de la aplicación.
    """
    def __init__(self, Contexto, FileLog, FormatoLog):
        """
        Constructor de la clase delegada del manejo de log de la aplicación.

        Parametros de Constructor
            Contexto -> Contexto de la aplicacion.
            FileLog -> Ruta absoluta del fichero de log.
            FormatoLog -> Formatos admitidos de log (csv o json)
        """
        if not FormatoLog.lower() in ('csv','json'): raise Exception("Error!!! Configuracion de formato de log erronea {}. Solo admitidos formatos json y csv".format(FormatoLog))
        self.FormatoLog = FormatoLog.lower()
        self.Contexto = Contexto
        self.FileLog = FileLog
        self.__compruebaTipoMensajesActivos()
        self.escribeLog(__class__.__name__,TipoMensaje.INFORMACION, "Inicio de escritura log.")

    def __compruebaTipoMensajesActivos(self):
        """
        Método auxiliar que establece la tipologíaa de mensajes que estan activos según la parametrización.
        """
        # Validamos el tipo de mensajes que se encuentran activos en el configurador.
        if self.Contexto.ConfigApp['EscrituraMensajesLog']['Informacion'].lower() == 's': self.ActivadoEscrituraInformacion = True
        else: self.ActivadoEscrituraInformacion = False
        if self.Contexto.ConfigApp['EscrituraMensajesLog']['Error'].lower() == 's': self.ActivadoEscrituraErrores = True
        else: self.ActivadoEscrituraErrores = False
        if self.Contexto.ConfigApp['EscrituraMensajesLog']['Aviso'].lower() == 's': self.ActivadoEscrituraAviso = True
        else: self.ActivadoEscrituraAviso = False

    def escribeLog(self, Clase, TipoError, DetalleError):
        """
        Método que realiza la escritura del error en el fichero.
        """
        # Escribimos el mensaje si estan activos en el configurador
        if (   (TipoError == TipoMensaje.ERROR and self.ActivadoEscrituraErrores)
            or (TipoError == TipoMensaje.AVISO and self.ActivadoEscrituraAviso)
            or (TipoError == TipoMensaje.INFORMACION and self.ActivadoEscrituraInformacion )):
            # Creamos la instancia de modelo LOG.
            LogModelFormato = LogModel(Clase, TipoError, DetalleError, self.Contexto.User)
            if self.FormatoLog == 'json': self.__escribeFormatoJSON(LogModelFormato)                
            elif self.FormatoLog == 'csv': 
                with open(self.FileLog,"a") as fileLog: 
                    fileLog.write(str(LogModelFormato)+"\n")
            else: raise Exception("Error!!! Escribiendo un formato de Log no admitido {}".format(self.FormatoLog))

    def __escribeFormatoJSON(self, LogModelFormato):
        """
        Método de escritura del fichero de log en formato JSON.

        Se recibe como parámetro la linea a escribir en formato JSON
        """
        if not os.path.isfile(self.FileLog):
            with open(self.FileLog,"w") as fileLog:
                fileLog.write("[\n" + json.dumps(LogModelFormato.getJSON()) +"\n]\n")     
        else:
            lineasLog = list()
            fileHandler = open(self.FileLog, 'r', encoding='utf-8')
            for lineaLog in fileHandler: lineasLog.append(lineaLog)                
            fileHandler.close()
            lngFile = len(lineasLog)
            if lngFile ==0:
                with open(self.FileLog,"w") as fileLog:
                    fileLog.write("[\n" + json.dumps(LogModelFormato.getJSON()) +"\n]\n")     
            else: 
                lngFile -= 2
                lineasLog[lngFile] = re.sub("\\n",",\\n",lineasLog[lngFile])
                lineasLog[-1] = json.dumps(LogModelFormato.getJSON())+"\n"
                lineasLog.append("]")
                with open(self.FileLog,"w") as fileLog:
                    for itemLineaLog in lineasLog:
                        fileLog.write(itemLineaLog)