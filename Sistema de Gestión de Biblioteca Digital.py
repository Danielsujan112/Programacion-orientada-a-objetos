from dataclasses import dataclass, field
from typing import Tuple, List, Dict, Optional

# --------------------------
# Clase Libro
# --------------------------
@dataclass
class Libro:
    # meta guarda (autor, título) como tupla inmutable según requisito
    meta: Tuple[str, str]  # (autor, título)
    categoria: str
    isbn: str
    is_borrowed: bool = field(default=False)  # indica si está prestado

    @property
    def autor(self) -> str:
        return self.meta[0]

    @property
    def titulo(self) -> str:
        return self.meta[1]

    def __repr__(self):
        estado = "Prestado" if self.is_borrowed else "Disponible"
        return f"<Libro {self.titulo!r} by {self.autor!r} | {self.categoria} | ISBN:{self.isbn} | {estado}>"

# --------------------------
# Clase Usuario
# --------------------------
@dataclass
class Usuario:
    nombre: str
    user_id: str
    # lista de ISBN de libros prestados (estructura mutable)
    libros_prestados: List[str] = field(default_factory=list)

    def __repr__(self):
        return f"<Usuario {self.nombre!r} (ID: {self.user_id}) | Prestados: {len(self.libros_prestados)}>"

# --------------------------
# Clase Biblioteca
# --------------------------
class Biblioteca:
    def __init__(self):
        # diccionario para acceso eficiente por ISBN
        self.libros: Dict[str, Libro] = {}
        # diccionario de usuarios por ID
        self.usuarios: Dict[str, Usuario] = {}
        # conjunto para IDs únicos
        self.user_ids: set = set()
        # mapa de préstamos: isbn -> user_id (None si disponible)
        self.prestamos: Dict[str, Optional[str]] = {}

    # --- Gestión de libros ---
    def añadir_libro(self, libro: Libro) -> bool:
        """Añade un libro al catálogo. Devuelve True si se añadió, False si ya existía ISBN."""
        if libro.isbn in self.libros:
            print(f"[Añadir libro] ERROR: ISBN {libro.isbn} ya existe en la biblioteca.")
            return False
        self.libros[libro.isbn] = libro
        self.prestamos[libro.isbn] = None
        print(f"[Añadir libro] Libro añadido: {libro}")
        return True

    def quitar_libro(self, isbn: str) -> bool:
        """Quita un libro del catálogo si existe y no está prestado."""
        if isbn not in self.libros:
            print(f"[Quitar libro] ERROR: ISBN {isbn} no encontrado.")
            return False
        if self.libros[isbn].is_borrowed:
            print(f"[Quitar libro] ERROR: ISBN {isbn} está actualmente prestado; no puede eliminarse.")
            return False
        del self.libros[isbn]
        del self.prestamos[isbn]
        print(f"[Quitar libro] Libro con ISBN {isbn} eliminado del catálogo.")
        return True

    # --- Gestión de usuarios ---
    def registrar_usuario(self, usuario: Usuario) -> bool:
        """Registra un usuario si su ID es único."""
        if usuario.user_id in self.user_ids:
            print(f"[Registrar usuario] ERROR: ID {usuario.user_id} ya registrado.")
            return False
        self.user_ids.add(usuario.user_id)
        self.usuarios[usuario.user_id] = usuario
        print(f"[Registrar usuario] Usuario registrado: {usuario}")
        return True

    def dar_baja_usuario(self, user_id: str) -> bool:
        """Da de baja a un usuario solo si no tiene libros prestados."""
        if user_id not in self.user_ids:
            print(f"[Dar de baja] ERROR: Usuario {user_id} no existe.")
            return False
        if self.usuarios[user_id].libros_prestados:
            print(f"[Dar de baja] ERROR: Usuario {user_id} tiene libros prestados; no puede darse de baja.")
            return False
        self.user_ids.remove(user_id)
        del self.usuarios[user_id]
        print(f"[Dar de baja] Usuario {user_id} ha sido dado de baja.")
        return True

    # --- Préstamos ---
    def prestar_libro(self, isbn: str, user_id: str) -> bool:
        """Presta un libro a un usuario si está disponible y ambos existen."""
        if isbn not in self.libros:
            print(f"[Prestar] ERROR: ISBN {isbn} no existe.")
            return False
        if user_id not in self.user_ids:
            print(f"[Prestar] ERROR: Usuario {user_id} no registrado.")
            return False
        libro = self.libros[isbn]
        if libro.is_borrowed:
            print(f"[Prestar] ERROR: Libro {isbn} ya está prestado a {self.prestamos[isbn]}.")
            return False
        # realizar préstamo
        libro.is_borrowed = True
        self.prestamos[isbn] = user_id
        self.usuarios[user_id].libros_prestados.append(isbn)
        print(f"[Prestar] Libro {libro.titulo!r} (ISBN {isbn}) prestado a usuario {user_id}.")
        return True

    def devolver_libro(self, isbn: str, user_id: str) -> bool:
        """Devuelve un libro: solo si está prestado a ese usuario."""
        if isbn not in self.libros:
            print(f"[Devolver] ERROR: ISBN {isbn} no existe en el catálogo.")
            return False
        if self.prestamos.get(isbn) != user_id:
            propietario = self.prestamos.get(isbn)
            print(f"[Devolver] ERROR: Libro {isbn} no está prestado a {user_id} (actual: {propietario}).")
            return False
        # realizar devolución
        self.libros[isbn].is_borrowed = False
        self.prestamos[isbn] = None
        self.usuarios[user_id].libros_prestados.remove(isbn)
        print(f"[Devolver] Libro ISBN {isbn} devuelto por usuario {user_id}.")
        return True

    # --- Búsquedas ---
    def buscar_por_titulo(self, texto: str) -> List[Libro]:
        txt = texto.lower()
        resultados = [lib for lib in self.libros.values() if txt in lib.titulo.lower()]
        print(f"[Buscar título] Encontrados {len(resultados)} resultados para '{texto}'.")
        return resultados

    def buscar_por_autor(self, autor: str) -> List[Libro]:
        txt = autor.lower()
        resultados = [lib for lib in self.libros.values() if txt in lib.autor.lower()]
        print(f"[Buscar autor] Encontrados {len(resultados)} resultados para '{autor}'.")
        return resultados

    def buscar_por_categoria(self, categoria: str) -> List[Libro]:
        txt = categoria.lower()
        resultados = [lib for lib in self.libros.values() if txt in lib.categoria.lower()]
        print(f"[Buscar categoría] Encontrados {len(resultados)} resultados para '{categoria}'.")
        return resultados

    # --- Listados ---
    def listar_prestados_usuario(self, user_id: str) -> List[Libro]:
        """Devuelve los objetos Libro prestados a un usuario."""
        if user_id not in self.user_ids:
            print(f"[Listar prestados] ERROR: Usuario {user_id} no existe.")
            return []
        isbns = self.usuarios[user_id].libros_prestados
        resultados = [self.libros[isbn] for isbn in isbns]
        print(f"[Listar prestados] Usuario {user_id} tiene {le_
