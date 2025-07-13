# archivo: gestion_conexion.py

class ConexionBaseDatos:
    def __init__(self, nombre_bd):
        """
        Constructor que se ejecuta automaticamente al crear una instancia de la clase.
        Inicializa la conexion a la base de datos (simulada).
        """
        self.nombre_bd = nombre_bd
        self.conectado = False
        self.conectar()

    def conectar(self):
        """
        Metodo que simula la conexion a una base de datos.
        """
        print(f"Conectando a la base de datos '{self.nombre_bd}'...")
        self.conectado = True
        print("Conexion establecida.")

    def ejecutar_consulta(self, consulta):
        """
        Simula la ejecucion de una consulta en la base de datos.
        """
        if self.conectado:
            print(f"Ejecutando consulta: {consulta}")
        else:
            print("No se puede ejecutar la consulta. No hay conexion.")

    def cerrar_conexion(self):
        """
        Metodo que simula el cierre de la conexion a la base de datos.
        """
        if self.conectado:
            print(f"Cerrando conexion con la base de datos '{self.nombre_bd}'...")
            self.conectado = False
            print("Conexion cerrada.")

    def __del__(self):
        """
        Destructor que se ejecuta automaticamente cuando el objeto se elimina o el programa termina.
        Libera recursos, como cerrar conexiones abiertas.
        """
        print("Destructor invocado...")
        self.cerrar_conexion()


# Bloque principal de prueba
if __name__ == "__main__":
    print("Inicio del programa")

    # Crear una instancia de la clase
    conexion = ConexionBaseDatos("clientes.db")

    # Usar el objeto
    conexion.ejecutar_consulta("SELECT * FROM usuarios")

    # Eliminar explicitamente el objeto (opcional, para ver el destructor en accion)
    del conexion

    print("Fin del programa")
