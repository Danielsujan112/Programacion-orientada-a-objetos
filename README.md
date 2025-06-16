# Programacion-orientada-a-objetos
# Programación Tradicional

def ingresar_temperaturas():
    """Función para ingresar temperaturas diarias."""
    temperaturas = []
    print("Ingrese las temperaturas diarias de la semana:")
    for dia in range(7):
        temp = float(input(f"Día {dia + 1}: "))
        temperaturas.append(temp)
    return temperaturas

def calcular_promedio(temperaturas):
    """Función para calcular el promedio semanal."""
    return sum(temperaturas) / len(temperaturas)

def main_tradicional():
    """Función principal para la programación tradicional."""
    temperaturas = ingresar_temperaturas()
    promedio = calcular_promedio(temperaturas)
    print(f"El promedio semanal de temperatura es: {promedio:.2f}")

# Ejecutar el código tradicional
print("--- Programación Tradicional ---")
main_tradicional()

# Programación Orientada a Objetos (POO)

class ClimaDiario:
    """Clase para representar la información del clima diario."""

    def __init__(self):
        self.temperaturas = []

    def ingresar_temperaturas(self):
        """Método para ingresar temperaturas diarias."""
        print("Ingrese las temperaturas diarias de la semana:")
        for dia in range(7):
            temp = float(input(f"Día {dia + 1}: "))
            self.temperaturas.append(temp)

    def calcular_promedio(self):
        """Método para calcular el promedio semanal."""
        return sum(self.temperaturas) / len(self.temperaturas)

def main_poo():
    """Función principal para la programación orientada a objetos."""
    clima = ClimaDiario()
    clima.ingresar_temperaturas()
    promedio = clima.calcular_promedio()
    print(f"El promedio semanal de temperatura es: {promedio:.2f}")

# Ejecutar el código POO
print("\n--- Programación Orientada a Objetos (POO) ---")
main_poo()
