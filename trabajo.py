from abc import ABC, abstractmethod
import logging

# ============================================================
# 1. CONFIGURACIÓN DE ROBUSTEZ (LOGS)
# ============================================================
# Se asegura que el archivo se cree y registre todo el flujo
logging.basicConfig(
    filename="logs.txt",
    level=logging.DEBUG, # Cambiado a DEBUG para registrar éxito y errores
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode='w' # 'w' para que se limpie cada vez que inicias pruebas
)

# ============================================================
# 2. EXCEPCIONES PERSONALIZADAS
# ============================================================
class SistemaError(Exception):
    """Clase base para errores del sistema."""
    pass

class ClienteError(SistemaError):
    """Errores relacionados con la validación de clientes."""
    pass

class ReservaError(SistemaError):
    """Errores relacionados con la lógica de reservas."""
    pass

# ============================================================
# 3. MODELO ORIENTADO A OBJETOS (POO)
# ============================================================

class Entidad(ABC):
    @abstractmethod
    def mostrar_info(self):
        pass

class Cliente(Entidad):
    def __init__(self, tipo_doc, num_doc, nombre, correo, celular):
        self.__tipo_doc = tipo_doc
        self.__num_doc = num_doc
        self.__nombre = nombre
        self.__correo = correo
        self.__celular = celular
        # Validación automática
        self.validar_datos()

    def validar_datos(self):
        """Uso de encadenamiento de excepciones (Requisito Nivel Alto)."""
        try:
            if not self.__num_doc.isdigit() or len(self.__num_doc) < 5:
                raise ValueError("Número de documento no cumple longitud mínima.")
            if "@" not in self.__correo:
                raise ValueError("Falta el símbolo @ en el correo.")
            if len(self.__celular) != 10:
                raise ValueError("El celular no tiene 10 dígitos.")
        except ValueError as e:
            # ENCADENAMIENTO DE EXCEPCIONES
            mensaje = f"Error en cliente {self.__nombre}: {str(e)}"
            logging.error(mensaje)
            raise ClienteError(mensaje) from e

    def mostrar_info(self):
        return f"Cliente: {self.__nombre} | ID: {self.__num_doc}"

    def get_nombre(self): 
        return self.__nombre

# ============================================================
# 4. POLIMORFISMO EN SERVICIOS
# ============================================================

class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, duracion):
        pass

class ReservaSala(Servicio):
    def calcular_costo(self, horas):
        return self.precio_base * horas

class Asesoria(Servicio):
    def calcular_costo(self, horas):
        return (self.precio_base * horas) * 0.9

# ============================================================
# 5. SISTEMA PRINCIPAL CON 10 SIMULACIONES
# ============================================================

class SistemaGestion:
    def __init__(self):
        self.clientes = []

    def ejecutar_pruebas(self):
        # Lista de 10 casos de prueba (5 válidos, 5 inválidos)
        casos = [
            {"n": "Juan Perez", "id": "10123456", "mail": "juan@unad.edu", "cel": "3001234567"}, # Válido
            {"n": "Error Doc", "id": "12", "mail": "err@unad.edu", "cel": "3000000000"},       # Inválido (ID corto)
            {"n": "Ana Maria", "id": "20234567", "mail": "ana@unad.edu", "cel": "3101112233"},  # Válido
            {"n": "Error Mail", "id": "30345678", "mail": "sin_arroba", "cel": "3202223344"},   # Inválido (@)
            {"n": "Carlos Ruiz", "id": "40456789", "mail": "car@unad.edu", "cel": "3004445566"}, # Válido
            {"n": "Error Cel", "id": "50567890", "mail": "cel@unad.edu", "cel": "123"},         # Inválido (Celular)
            {"n": "Sonia Lopez", "id": "60678901", "mail": "son@unad.edu", "cel": "3156667788"}, # Válido
            {"n": "Doc Letras", "id": "ABC123", "mail": "let@unad.edu", "cel": "3117778899"},   # Inválido (ID Letras)
            {"n": "Luis Paez", "id": "70789012", "mail": "luis@unad.edu", "cel": "3228889900"},  # Válido
            {"n": "Mail Vacio", "id": "80890123", "mail": "", "cel": "3009990011"}              # Inválido (Email)
        ]

        print(f"{'--- SISTEMA DE GESTIÓN: COMPONENTE PRÁCTICO ---':^60}\n")
        
        for i, c in enumerate(casos, 1):
            print(f"SIMULACIÓN {i}: {c['n']}")
            try:
                # Bloque TRY: Intento de creación
                nuevo = Cliente("CC", c['id'], c['n'], c['mail'], c['cel'])
            except ClienteError as e:
                # Bloque EXCEPT: Captura error personalizado
                print(f"  [!] ERROR CAPTURADO: {e}")
            else:
                # Bloque ELSE: Se ejecuta si todo salió bien
                print(f"  [OK] Cliente creado: {nuevo.get_nombre()}")
                self.clientes.append(nuevo)
            finally:
                # Bloque FINALLY: Se ejecuta siempre (limpieza o log final)
                logging.debug(f"Finalizada simulación {i} para {c['n']}")
                print(f"  {'--' * 20}")

        print(f"\nResumen: Se registraron {len(self.clientes)} clientes exitosamente.")
        print("Revise el archivo 'logs.txt' para ver el detalle técnico.")

# ============================================================
# 6. ARRANQUE
# ============================================================
if __name__ == "__main__":
    sistema = SistemaGestion()
    sistema.ejecutar_pruebas()