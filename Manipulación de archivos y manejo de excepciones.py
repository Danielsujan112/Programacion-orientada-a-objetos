"""
Sistema de Gestión de Inventarios (con archivos y manejo de excepciones)
-------------------------------------------------------------------------
- Persiste en un archivo CSV de texto (por defecto: "inventario.txt").
- Carga automáticamente el inventario al iniciar.
- Maneja excepciones comunes de E/S (FileNotFoundError, PermissionError, etc.).
- Interfaz de consola con mensajes claros de éxito/fracaso.
- Escrituras atómicas (archivo temporal + os.replace) para reducir corrupción.
- Incluye una opción de prueba para inyectar una línea corrupta en el archivo.

Formato del archivo (CSV UTF-8 con encabezados):
    id,nombre,cantidad,precio

Ejecutar:
    python inventario_archivos.py
"""
import csv
import os
from typing import Dict, List, Optional

CAMPOS = ["id", "nombre", "cantidad", "precio"]


class Inventario:
    def __init__(self, ruta_archivo: str = "inventario.txt") -> None:
        self.ruta = ruta_archivo
        self.productos: Dict[int, Dict] = {}
        self._crear_archivo_si_no_existe()
        self.cargar_desde_archivo()

    def _crear_archivo_si_no_existe(self) -> None:
        try:
            with open(self.ruta, "x", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=CAMPOS)
                writer.writeheader()
                print(f"[INFO] Archivo '{self.ruta}' creado.")
        except FileExistsError:
            pass
        except PermissionError as e:
            print(f"[ERROR] Sin permisos para crear '{self.ruta}': {e}")

    def cargar_desde_archivo(self) -> None:
        self.productos.clear()
        try:
            with open(self.ruta, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    try:
                        id_ = int(fila["id"])
                        self.productos[id_] = {
                            "id": id_,
                            "nombre": fila["nombre"],
                            "cantidad": int(fila["cantidad"]),
                            "precio": float(fila["precio"]),
                        }
                    except Exception:
                        print("[ADVERTENCIA] Línea inválida en el archivo. Se omitió.")
                print(f"[OK] Cargados {len(self.productos)} productos.")
        except FileNotFoundError:
            print(f"[INFO] Archivo '{self.ruta}' no encontrado. Se creará al guardar.")
        except PermissionError as e:
            print(f"[ERROR] Sin permisos para leer '{self.ruta}': {e}")

    def _guardar_en_archivo(self) -> None:
        tmp = self.ruta + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=CAMPOS)
                writer.writeheader()
                for p in self.productos.values():
                    writer.writerow(p)
            os.replace(tmp, self.ruta)
            print(f"[OK] Inventario guardado en '{self.ruta}'.")
        except PermissionError as e:
            print(f"[ERROR] Sin permisos para escribir en '{self.ruta}': {e}")

    def _siguiente_id(self) -> int:
        return max(self.productos.keys(), default=0) + 1

    def agregar_producto(self, nombre: str, cantidad: int, precio: float) -> None:
        id_nuevo = self._siguiente_id()
        self.productos[id_nuevo] = {
            "id": id_nuevo,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio,
        }
        self._guardar_en_archivo()

    def actualizar_producto(self, id_: int, nombre: Optional[str] = None,
                            cantidad: Optional[int] = None, precio: Optional[float] = None) -> None:
        if id_ not in self.productos:
            print("[INFO] Producto no encontrado.")
            return
        if nombre:
            self.productos[id_]["nombre"] = nombre
        if cantidad is not None:
            self.productos[id_]["cantidad"] = cantidad
        if precio is not None:
            self.productos[id_]["precio"] = precio
        self._guardar_en_archivo()

    def eliminar_producto(self, id_: int) -> None:
        if id_ in self.productos:
            self.productos.pop(id_)
            self._guardar_en_archivo()
            print(f"[OK] Producto {id_} eliminado.")
        else:
            print("[INFO] Producto no encontrado.")

    def listar(self) -> List[Dict]:
        return list(self.productos.values())


# =============================== Interfaz CLI =============================== #

def menu() -> None:
    inv = Inventario()
    while True:
        print("""
======= MENÚ =======
1) Agregar producto
2) Actualizar producto
3) Eliminar producto
4) Listar productos
0) Salir
====================
""")
        op = input("Seleccione opción: ").strip()
        if op == "1":
            nombre = input("Nombre: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))
            inv.agregar_producto(nombre, cantidad, precio)
        elif op == "2":
            id_ = int(input("ID a actualizar: "))
            nombre = input("Nuevo nombre (enter para omitir): ").strip() or None
            cantidad = input("Nueva cantidad (enter para omitir): ").strip()
            precio = input("Nuevo precio (enter para omitir): ").strip()
            inv.actualizar_producto(
                id_,
                nombre=nombre,
                cantidad=int(cantidad) if cantidad else None,
                precio=float(precio) if precio else None,
            )
        elif op == "3":
            id_ = int(input("ID a eliminar: "))
            inv.eliminar_producto(id_)
        elif op == "4":
            for p in inv.listar():
                print(p)
        elif op == "0":
            print("[INFO] Saliendo del programa.")
            break
        else:
            print("[INFO] Opción no válida.")


if __name__ == "__main__":
    menu()
