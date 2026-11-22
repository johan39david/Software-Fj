"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas.
Empresa: Software FJ
Descripción:
Aplicación orientada a objetos para gestionar clientes,
servicios y reservas de salas, alquiler de equipos y
asesorías especializadas.
El sistema utiliza almacenamiento en memoria, validaciones,
manejo de excepciones y registro de eventos mediante logs.
"""
import logging
from abc import ABC, abstractmethod
from datetime import datetime
import re


# ============================================================
# 1.CONFIGURACION DEL SISTEMA DE LOGS
# ============================================================

# Todos los eventos y errores se guardan en este archivo.
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("SoftwareFJ")


# ============================================================
# 2.EXCEPCIONES PERSONALIZADAS
# ============================================================

# Clase general para los errores propios del sistema.
class ErrorSistema(Exception):
    pass


# Se utiliza cuando un dato no cumple las validaciones.
class DatoInvalidoError(ErrorSistema):
    pass


# Se utiliza cuando una operacion no esta permitida.
class OperacionNoPermitidaError(ErrorSistema):
    pass


# Se utiliza cuando un servicio no esta disponible.
class ServicioNoDisponibleError(ErrorSistema):
    pass


# Se utiliza cuando ocurre un problema con una reserva.
class ReservaError(ErrorSistema):
    pass


# ============================================================
# 3. CLASE ABSTRACTA ENTIDAD
# ============================================================

# Representa una entidad general del sistema.
# No se pueden crear objetos directamente de esta clase.
class Entidad(ABC):

    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatoInvalidoError(
                "El identificador no puede estar vacio."
            )

        self._identificador = identificador.strip()
        self._fecha_creacion = datetime.now()

    @property
    def identificador(self):
        return self._identificador

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def describir(self):
        # Cada clase hija debe implementar este metodo.
        pass


# ============================================================
# 4. CLASE CLIENTE
# ============================================================

class Cliente(Entidad):

    def __init__(self, identificador, nombre, correo, telefono, edad):

        super().__init__(identificador)

        # Encapsulacion de los atributos.
        self._nombre = self._validar_nombre(nombre)
        self._correo = self._validar_correo(correo)
        self._telefono = self._validar_telefono(telefono)
        self._edad = self._validar_edad(edad)

    def _validar_nombre(self, nombre):

        if not isinstance(nombre, str) or len(nombre.strip()) < 2:
            raise DatoInvalidoError("Nombre invalido.")

        return nombre.strip()

    def _validar_correo(self, correo):

        if not isinstance(correo, str):
            raise DatoInvalidoError("El correo debe ser texto.")

        patron = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

        if not re.match(patron, correo):
            raise DatoInvalidoError("Formato de correo invalido.")

        return correo.strip()

    def _validar_telefono(self, telefono):

        if not isinstance(telefono, str):
            raise DatoInvalidoError("El telefono debe ser texto.")

        if not telefono.isdigit() or len(telefono) < 7:
            raise DatoInvalidoError("Telefono invalido.")

        return telefono

    def _validar_edad(self, edad):

        try:
            edad = int(edad)
        except (ValueError, TypeError) as exc:
            # Encadenamiento de excepciones.
            raise DatoInvalidoError(
                "La edad debe ser un numero entero."
            ) from exc

        if edad < 18 or edad > 100:
            raise DatoInvalidoError(
                "La edad debe estar entre 18 y 100."
            )

        return edad

    # Propiedades para consultar los datos privados.
    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    @property
    def telefono(self):
        return self._telefono

    @property
    def edad(self):
        return self._edad

    def describir(self):
        return (
            f"Cliente: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Telefono: {self.telefono}"
        )


# ============================================================
# 5. CLASE ABSTRACTA SERVICIO
# ============================================================

# Todos los servicios deben heredar de esta clase.
class Servicio(Entidad):

    def __init__(self, identificador, nombre, tarifa):

        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalidoError("Nombre del servicio invalido.")

        if isinstance(tarifa, bool) or not isinstance(tarifa, (int, float)):
            raise DatoInvalidoError("La tarifa debe ser numerica.")

        if tarifa <= 0:
            raise DatoInvalidoError("La tarifa debe ser positiva.")

        self._nombre = nombre.strip()
        self._tarifa = float(tarifa)
        self._disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa(self):
        return self._tarifa

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):

        if not isinstance(estado, bool):
            raise DatoInvalidoError(
                "La disponibilidad debe ser True o False."
            )

        self._disponible = estado

    # Metodo que simula diferentes variantes de calculo.
    # Los parametros opcionales permiten adaptar la operacion.
    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    @abstractmethod
    def describir(self):
        pass

    # Metodo comun para validar y calcular el precio final.
    def precio_final(self, duracion, impuesto=0, descuento=0):

        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
            raise DatoInvalidoError("Impuesto invalido.")

        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
            raise DatoInvalidoError("Descuento invalido.")

        if not 0 <= impuesto <= 1:
            raise DatoInvalidoError("El impuesto debe estar entre 0 y 1.")

        if not 0 <= descuento <= 1:
            raise DatoInvalidoError("El descuento debe estar entre 0 y 1.")

        return self.calcular_costo(duracion, impuesto, descuento)


# ============================================================
# 6. SERVICIO DE RESERVA DE SALAS
# ============================================================

class ReservaSala(Servicio):

    def __init__(self, identificador, tarifa, capacidad):

        super().__init__(
            identificador,
            "Reserva de sala",
            tarifa
        )

        if isinstance(capacidad, bool) or not isinstance(capacidad, int):
            raise DatoInvalidoError("La capacidad debe ser entera.")

        if capacidad <= 0:
            raise DatoInvalidoError("Capacidad invalida.")

        self._capacidad = capacidad

    def validar_parametros(self, duracion):

        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise DatoInvalidoError("La duracion debe ser numerica.")

        if duracion <= 0 or duracion > 12:
            raise DatoInvalidoError(
                "Una sala puede reservarse entre 0 y 12 horas."
            )

        return True

    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        self.validar_parametros(duracion)

        subtotal = self.tarifa * duracion
        total = subtotal * (1 - descuento)
        total += total * impuesto

        return round(total, 2)

    def describir(self):

        return (
            f"{self.nombre} | "
            f"Capacidad: {self._capacidad} personas | "
            f"Tarifa por hora: ${self.tarifa}"
        )


# ============================================================
# 7. SERVICIO DE ALQUILER DE EQUIPOS
# ============================================================

class AlquilerEquipo(Servicio):

    def __init__(self, identificador, tarifa, cantidad):

        super().__init__(
            identificador,
            "Alquiler de equipos",
            tarifa
        )

        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise DatoInvalidoError("La cantidad debe ser entera.")

        if cantidad <= 0:
            raise DatoInvalidoError("Cantidad de equipos invalida.")

        self._cantidad = cantidad

    def validar_parametros(self, duracion):

        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise DatoInvalidoError("La duracion debe ser numerica.")

        if duracion <= 0 or duracion > 168:
            raise DatoInvalidoError(
                "El alquiler debe durar entre 0 y 168 horas."
            )

        return True

    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        self.validar_parametros(duracion)

        subtotal = self.tarifa * duracion * self._cantidad
        total = subtotal * (1 - descuento)
        total += total * impuesto

        return round(total, 2)

    def describir(self):

        return (
            f"{self.nombre} | "
            f"Cantidad: {self._cantidad} equipos | "
            f"Tarifa por equipo/hora: ${self.tarifa}"
        )


# ============================================================
# 8. SERVICIO DE ASESORIAS ESPECIALIZADAS
# ============================================================

class Asesoria(Servicio):

    def __init__(self, identificador, tarifa, especialidad):

        super().__init__(
            identificador,
            "Asesoria especializada",
            tarifa
        )

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatoInvalidoError("Especialidad invalida.")

        self._especialidad = especialidad.strip()

    def validar_parametros(self, duracion):

        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise DatoInvalidoError("La duracion debe ser numerica.")

        if duracion <= 0 or duracion > 8:
            raise DatoInvalidoError(
                "La asesoria debe durar entre 0 y 8 horas."
            )

        return True

    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        self.validar_parametros(duracion)

        subtotal = self.tarifa * duracion
        total = subtotal * (1 - descuento)
        total += total * impuesto

        return round(total, 2)

    def describir(self):

        return (
            f"{self.nombre} | "
            f"Especialidad: {self._especialidad} | "
            f"Tarifa por hora: ${self.tarifa}"
        )


# ============================================================
# 9. CLASE RESERVA
# ============================================================

class Reserva(Entidad):

    def __init__(self, identificador, cliente, servicio, duracion):

        super().__init__(identificador)

        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Debe proporcionar un cliente valido.")

        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Debe proporcionar un servicio valido.")

        # Se valida la duracion antes de crear la reserva.
        servicio.validar_parametros(duracion)

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "Pendiente"
        self._costo = 0

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    def describir(self):

        return (
            f"Reserva {self.identificador} | "
            f"Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | "
            f"Estado: {self.estado}"
        )

    # Confirma la reserva si el servicio esta disponible.
    def confirmar(self):

        if self._estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                "El servicio seleccionado no esta disponible."
            )

        self._estado = "Confirmada"

        logger.info(
            "Reserva %s confirmada.",
            self.identificador
        )

    # Cancela una reserva pendiente o confirmada.
    def cancelar(self):

        if self._estado not in ("Pendiente", "Confirmada"):
            raise OperacionNoPermitidaError(
                "No se puede cancelar esta reserva."
            )

        self._estado = "Cancelada"

        logger.info(
            "Reserva %s cancelada.",
            self.identificador
        )

    # Procesa una reserva confirmada y calcula su costo.
    def procesar(self, impuesto=0, descuento=0):

        if self._estado != "Confirmada":
            raise ReservaError(
                "La reserva debe estar confirmada para procesarse."
            )

        try:
            self._costo = self._servicio.precio_final(
                self._duracion,
                impuesto,
                descuento
            )

            if self._costo <= 0:
                raise ReservaError("El costo calculado no es valido.")

            self._estado = "Procesada"

            logger.info(
                "Reserva %s procesada. Costo: $%s",
                self.identificador,
                self._costo
            )

            return self._costo

        except ErrorSistema:
            logger.exception(
                "Error procesando reserva %s",
                self.identificador
            )
            raise

        except Exception as exc:
            logger.exception("Error inesperado procesando reserva.")

            raise ReservaError(
                "No fue posible procesar la reserva."
            ) from exc

        finally:
            # Se ejecuta exista o no exista un error.
            logger.info(
                "Finalizo intento de procesamiento de reserva %s.",
                self.identificador
            )


# ============================================================
# 10. CLASE GESTOR DEL SISTEMA
# ============================================================

class GestorSistema:

    def __init__(self):

        # Listas internas: no se utiliza ninguna base de datos.
        self._clientes = []
        self._servicios = []
        self._reservas = []

    # REGISTRO DE CLIENTES
    def registrar_cliente(self, cliente):

        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Objeto cliente invalido.")

        if any(c.identificador == cliente.identificador
               for c in self._clientes):
            raise OperacionNoPermitidaError(
                "El cliente ya se encuentra registrado."
            )

        self._clientes.append(cliente)

        logger.info(
            "Cliente registrado: %s",
            cliente.identificador
        )

        return cliente

    # REGISTRO DE SERVICIOS
    def registrar_servicio(self, servicio):

        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Servicio invalido.")

        if any(s.identificador == servicio.identificador
               for s in self._servicios):
            raise OperacionNoPermitidaError(
                "El servicio ya se encuentra registrado."
            )

        self._servicios.append(servicio)

        logger.info(
            "Servicio registrado: %s",
            servicio.identificador
        )

        return servicio

    # CREACION DE RESERVAS
    def crear_reserva(self, identificador, cliente, servicio, duracion):

        if cliente not in self._clientes:
            raise DatoInvalidoError(
                "El cliente no esta registrado."
            )

        if servicio not in self._servicios:
            raise DatoInvalidoError(
                "El servicio no esta registrado."
            )

        reserva = Reserva(
            identificador,
            cliente,
            servicio,
            duracion
        )

        if any(r.identificador == identificador
               for r in self._reservas):
            raise OperacionNoPermitidaError(
                "Ya existe una reserva con ese identificador."
            )

        self._reservas.append(reserva)

        logger.info(
            "Reserva creada: %s",
            identificador
        )

        return reserva


    # BUSQUEDA DE ELEMENTOS POR IDENTIFICADOR
    def obtener_cliente(self, identificador):
        """Busca un cliente registrado por su identificador."""
        for cliente in self._clientes:
            if cliente.identificador == identificador:
                return cliente
        raise DatoInvalidoError("No existe un cliente con ese identificador.")

    def obtener_servicio(self, identificador):
        """Busca un servicio registrado por su identificador."""
        for servicio in self._servicios:
            if servicio.identificador == identificador:
                return servicio
        raise DatoInvalidoError("No existe un servicio con ese identificador.")

    def obtener_reserva(self, identificador):
        """Busca una reserva registrada por su identificador."""
        for reserva in self._reservas:
            if reserva.identificador == identificador:
                return reserva
        raise DatoInvalidoError("No existe una reserva con ese identificador.")

    # CONSULTAR CLIENTES
    def listar_clientes(self):

        return [c.describir() for c in self._clientes]

    # CONSULTAR SERVICIOS
    def listar_servicios(self):

        return [s.describir() for s in self._servicios]

    # CONSULTAR RESERVAS
    def listar_reservas(self):

        return [r.describir() for r in self._reservas]


# ============================================================
# 11. FUNCION PARA EJECUTAR OPERACIONES DE FORMA SEGURA
# ============================================================

# Esta funcion permite que un error no detenga el programa.
def ejecutar_operacion(descripcion, operacion):

    print(f"\n--- {descripcion} ---")

    try:
        resultado = operacion()

    except ErrorSistema as error:

        print(f"[ERROR CONTROLADO] {error}")

        logger.error(
            "%s: %s",
            descripcion,
            error,
            exc_info=True
        )

    except Exception as error:

        print(f"[ERROR INESPERADO] {error}")

        logger.exception(
            "Error inesperado durante: %s",
            descripcion
        )

    else:
        # Se ejecuta solamente cuando no hay excepciones.
        print("[OK] Operacion realizada correctamente.")

        if resultado is not None:
            print(resultado)

    finally:
        # Se ejecuta siempre, haya error o no.
        print("[FIN] Operacion finalizada.")


# ============================================================
# 12. PRUEBAS Y DEMOSTRACION DEL SISTEMA
# ============================================================


# ============================================================
# 13. FUNCIONES AUXILIARES PARA EL MENU INTERACTIVO
# ============================================================

def leer_texto(mensaje):
    """Solicita un texto no vacio al usuario."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("El dato no puede estar vacio.")


def leer_entero(mensaje):
    """Solicita un numero entero y valida la entrada."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Entrada invalida. Escriba un numero entero.")


def leer_decimal(mensaje):
    """Solicita un numero decimal y valida la entrada."""
    while True:
        try:
            return float(input(mensaje).replace(",", "."))
        except ValueError:
            print("Entrada invalida. Escriba un numero.")


def mostrar_menu():
    """Muestra las opciones principales del sistema."""
    print("\n" + "=" * 55)
    print("       SOFTWARE FJ - MENU PRINCIPAL")
    print("=" * 55)
    print("1. Registrar cliente")
    print("2. Registrar servicio")
    print("3. Consultar clientes")
    print("4. Consultar servicios")
    print("5. Crear reserva")
    print("6. Consultar reservas")
    print("7. Gestionar una reserva")
    print("8. Ejecutar demostracion automatica")
    print("0. Salir")
    print("=" * 55)


# ============================================================
# 14. OPERACIONES INTERACTIVAS
# ============================================================

def registrar_cliente_interactivo(sistema):
    """Solicita los datos y registra un cliente."""
    print("\n--- REGISTRO DE CLIENTE ---")
    identificador = leer_texto("Identificador: ")
    nombre = leer_texto("Nombre completo: ")
    correo = leer_texto("Correo electronico: ")
    telefono = leer_texto("Telefono: ")
    edad = leer_entero("Edad: ")

    cliente = Cliente(identificador, nombre, correo, telefono, edad)
    sistema.registrar_cliente(cliente)
    return f"Cliente {cliente.nombre} registrado correctamente."


def registrar_servicio_interactivo(sistema):
    """Permite seleccionar y registrar uno de los tres tipos de servicio."""
    print("\n--- REGISTRO DE SERVICIO ---")
    print("1. Reserva de sala")
    print("2. Alquiler de equipos")
    print("3. Asesoria especializada")

    tipo = leer_texto("Seleccione el tipo de servicio: ")
    identificador = leer_texto("Identificador: ")
    tarifa = leer_decimal("Tarifa: ")

    if tipo == "1":
        capacidad = leer_entero("Capacidad de la sala: ")
        servicio = ReservaSala(identificador, tarifa, capacidad)
    elif tipo == "2":
        cantidad = leer_entero("Cantidad de equipos: ")
        servicio = AlquilerEquipo(identificador, tarifa, cantidad)
    elif tipo == "3":
        especialidad = leer_texto("Especialidad de la asesoria: ")
        servicio = Asesoria(identificador, tarifa, especialidad)
    else:
        raise DatoInvalidoError("Tipo de servicio no reconocido.")

    sistema.registrar_servicio(servicio)
    return f"Servicio registrado: {servicio.describir()}"


def consultar_elementos(titulo, elementos):
    """Muestra los elementos recibidos o informa si no hay registros."""
    print(f"\n--- {titulo} ---")
    if not elementos:
        print("No hay elementos registrados.")
        return
    for elemento in elementos:
        print(elemento)


def crear_reserva_interactiva(sistema):
    """Solicita los datos necesarios para crear una reserva."""
    print("\n--- CREACION DE RESERVA ---")
    identificador = leer_texto("Identificador de la reserva: ")
    id_cliente = leer_texto("Identificador del cliente: ")
    id_servicio = leer_texto("Identificador del servicio: ")
    duracion = leer_decimal("Duracion (horas): ")

    cliente = sistema.obtener_cliente(id_cliente)
    servicio = sistema.obtener_servicio(id_servicio)
    reserva = sistema.crear_reserva(
        identificador, cliente, servicio, duracion
    )
    return reserva.describir()


def gestionar_reserva_interactiva(sistema):
    """Permite confirmar, cancelar o procesar una reserva."""
    print("\n--- GESTION DE RESERVA ---")
    identificador = leer_texto("Identificador de la reserva: ")
    reserva = sistema.obtener_reserva(identificador)

    print(f"Reserva seleccionada: {reserva.describir()}")
    print("1. Confirmar")
    print("2. Cancelar")
    print("3. Procesar")
    opcion = leer_texto("Seleccione una operacion: ")

    if opcion == "1":
        reserva.confirmar()
        return "Reserva confirmada correctamente."
    if opcion == "2":
        reserva.cancelar()
        return "Reserva cancelada correctamente."
    if opcion == "3":
        impuesto = leer_decimal(
            "Impuesto (ejemplo: 0.19 para 19 %): "
        )
        descuento = leer_decimal(
            "Descuento (ejemplo: 0.10 para 10 %): "
        )
        costo = reserva.procesar(impuesto=impuesto, descuento=descuento)
        return f"Reserva procesada. Costo total: ${costo:.2f}"

    raise DatoInvalidoError("Operacion de reserva no reconocida.")


# ============================================================
# 15. MENU PRINCIPAL INTERACTIVO
# ============================================================

def main():
    """Inicia el sistema y mantiene el menu hasta que el usuario salga."""
    sistema = GestorSistema()

    print("=" * 55)
    print("     SOFTWARE FJ - SISTEMA INTEGRAL DE GESTION")
    print("=" * 55)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            ejecutar_operacion(
                "Registro de cliente",
                lambda: registrar_cliente_interactivo(sistema)
            )
        elif opcion == "2":
            ejecutar_operacion(
                "Registro de servicio",
                lambda: registrar_servicio_interactivo(sistema)
            )
        elif opcion == "3":
            ejecutar_operacion(
                "Listado de clientes",
                lambda: consultar_elementos(
                    "CLIENTES", sistema.listar_clientes()
                )
            )
        elif opcion == "4":
            ejecutar_operacion(
                "Listado de servicios",
                lambda: consultar_elementos(
                    "SERVICIOS", sistema.listar_servicios()
                )
            )
        elif opcion == "5":
            ejecutar_operacion(
                "Creacion de reserva",
                lambda: crear_reserva_interactiva(sistema)
            )
        elif opcion == "6":
            ejecutar_operacion(
                "Listado de reservas",
                lambda: consultar_elementos(
                    "RESERVAS", sistema.listar_reservas()
                )
            )
        elif opcion == "7":
            ejecutar_operacion(
                "Gestion de reserva",
                lambda: gestionar_reserva_interactiva(sistema)
            )
        elif opcion == "8":
            from demostracion_software_fj import ejecutar_demostracion
            ejecutar_demostracion()
        elif opcion == "0":
            print("\nGracias por utilizar Software FJ.")
            logger.info("El usuario cerro el sistema.")
            break
        else:
            print("Opcion no valida. Intente nuevamente.")



# Punto de entrada principal del programa.
if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Error critico en el programa principal.")
        print("Ocurrio un error critico. Consulte el archivo de logs.")
