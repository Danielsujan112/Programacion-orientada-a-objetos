import json

class Producto:
    """
    Clase que representa un producto con atributos:
    ID (unico), nombre, cantidad y precio.
    """
    def __init__(self, id, nombre, cantidad, precio):
        self._id = id
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # Metodos para obtener y establecer atributos
    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    def get_cantidad(self):
        return self._cantidad

    def set_cantidad(self, nueva_cantidad):
        self._cantidad = nueva_cantidad

    def get_precio(self):
        return self._precio

    def set_precio(self, nuevo_precio):
        self._precio = nuevo_precio

    def __str__(self):
        return f"ID: {self._id}, Nombre: {self._nombre}, Cantidad: {self._cantidad}, Precio: {self._precio}"

class Inventario:
    """
    Clase que gestiona un inventario de productos.
    Utiliza un diccionario para almacenar productos con ID como clave.
    """
    def __init__(self):
        # Diccionario: clave = ID del producto, valor = objeto Producto
        self.productos = {}

    def agregar_producto(self, producto):
        """Agrega un producto al inventario si el ID no existe."""
        if producto.get_id() in self.productos:
            print("Ya existe un producto con ese ID.")
        else:
            self.productos[producto.get_id()] = producto
            print("Producto agregado exitosamente.")

    def eliminar_producto(self, id_producto):
        """Elimina un producto del inventario por su ID."""
        if id_producto in self.productos:
            del self.productos[id_producto]
            print("Producto eliminado.")
        else:
            print("Producto no encontrado.")

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        """
        Actualiza la cantidad y/o precio de un producto dado su ID.
        Se pueden pasar valores None para no modificar ese campo.
        """
        if id_producto in self.productos:
            if nueva_cantidad is not None:
                self.productos[id_producto].set_cantidad(nueva_cantidad)
            if nuevo_precio is not None:
                self.productos[id_producto].set_precio(nuevo_precio)
            print("Producto actualizado.")
        else:
            print("Producto no encontrado.")

    def buscar_por_nombre(self, nombre):
        """
        Busca productos cuyo nombre contenga la cadena dada (case-insensitive).
        Muestra los resultados encontrados.
        """
        encontrados = [p for p in self.productos.values() if nombre.lower() in p.get_nombre().lower()]
        if encontrados:
            print(f"Resultados de la búsqueda de '{nombre}':")
            for p in encontrados:
                print(p)
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_todos(self):
        """Muestra todos los productos en el inventario."""
        if self.productos:
            print("Inventario actual:")
            for p in self.productos.values():
                print(p)
        else:
            print("El inventario está vacío.")

    def guardar_en_archivo(self, nombre_archivo):
        """
        Guarda el inventario en un archivo JSON.
        Serializa la colección (lista de diccionarios de productos).
        """
        try:
            lista_productos = []
            for p in self.productos.values():
                # Convertir objeto Producto a diccionario
                lista_productos.append({
                    'id': p.get_id(),
                    'nombre': p.get_nombre(),
                    'cantidad': p.get_cantidad(),
                    'precio': p.get_precio()
                })
            with open(nombre_archivo, 'w') as f:
                json.dump(lista_productos, f, indent=4)
            print("Inventario guardado en archivo.")
        except IOError:
            print("Error al guardar el archivo.")

    def cargar_desde_archivo(self, nombre_archivo):
        """
        Carga el inventario desde un archivo JSON.
        Deserializa la información y reconstruye los objetos Producto.
        """
        try:
            with open(nombre_archivo, 'r') as f:
                lista_productos = json.load(f)
                for item in lista_productos:
                    producto = Producto(item['id'], item['nombre'], item['cantidad'], item['precio'])
                    self.productos[producto.get_id()] = producto
            print("Inventario cargado desde archivo.")
        except FileNotFoundError:
            print("No se encontró el archivo de inventario. Se creará uno nuevo al guardar.")
        except json.JSONDecodeError:
            print("Error al leer el archivo. El formato es incorrecto.")

def main():
    inventario = Inventario()
    inventario.cargar_desde_archivo('inventario.json')

    while True:
        print("\n--- Men\u00fa de Inventario ---")
        print("1. Agregar producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Guardar inventario en archivo")
        print("7. Salir")
        opcion = input("Selecciona una opci\u00f3n: ")

        if opcion == '1':
            id_producto = input("ID del producto: ")
            nombre = input("Nombre del producto: ")
            try:
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
            except ValueError:
                print("Cantidad o precio inválido.")
                continue
            producto = Producto(id_producto, nombre, cantidad, precio)
            inventario.agregar_producto(producto)

        elif opcion == '2':
            id_producto = input("ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)

        elif opcion == '3':
            id_producto = input("ID del producto a actualizar: ")
            cantidad_input = input("Nueva cantidad (dejar en blanco para no cambiar): ")
            precio_input = input("Nuevo precio (dejar en blanco para no cambiar): ")
            nueva_cantidad = None
            nuevo_precio = None
            if cantidad_input.strip() != '':
                try:
                    nueva_cantidad = int(cantidad_input)
                except ValueError:
                    print("Cantidad inválida.")
                    continue
            if precio_input.strip() != '':
                try:
                    nuevo_precio = float(precio_input)
                except ValueError:
                    print("Precio inválido.")
                    continue
            inventario.actualizar_producto(id_producto, nueva_cantidad, nuevo_precio)

        elif opcion == '4':
            nombre = input("Nombre del producto a buscar: ")
            inventario.buscar_por_nombre(nombre)

        elif opcion == '5':
            inventario.mostrar_todos()

        elif opcion == '6':
            inventario.guardar_en_archivo('inventario.json')

        elif opcion == '7':
            inventario.guardar_en_archivo('inventario.json')
            print("Saliendo del programa.")
            break

        else:
            print("Opc\u00edon no v\u00e1lida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
