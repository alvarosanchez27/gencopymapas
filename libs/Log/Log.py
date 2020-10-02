class Log():
    """
    Clase delegada el manejo del log de la aplicación.
    """

    def __init__(self, FileLog):
        """
        Constructor de la clase delegada del manejo de log de la aplicación.
        """
        self.FileLog = FileLog
        print(self.FileLog)