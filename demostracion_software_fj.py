"""
Demostracion automatica de las operaciones del sistema Software FJ.
Este modulo conserva los 20 casos de prueba originales.
"""

from software_fj_interactivo import (
    GestorSistema,
    Cliente,
    ReservaSala,
    AlquilerEquipo,
    Asesoria,
    ejecutar_operacion,
)

def ejecutar_demostracion():

    sistema = GestorSistema()

    print("=" * 55)
    print("     SOFTWARE FJ - SISTEMA INTEGRAL DE GESTION")
    print("=" * 55)

    # --------------------------------------------------------
    # OPERACION 1: Registrar un cliente correctamente.
    # --------------------------------------------------------

    cliente1 = Cliente(
        "C001",
        "Carlos Ramirez",
        "carlos@gmail.com",
        "3001234567",
        25
    )

    ejecutar_operacion(
        "Operacion 1: Registro de cliente",
        lambda: sistema.registrar_cliente(cliente1)
    )

    # --------------------------------------------------------
    # OPERACION 2: Intentar registrar un cliente invalido.
    # --------------------------------------------------------

    def cliente_invalido():

        cliente = Cliente(
            "C002",
            "Ana",
            "correo_incorrecto",
            "123",
            20
        )

        return sistema.registrar_cliente(cliente)

    ejecutar_operacion(
        "Operacion 2: Registro de cliente invalido",
        cliente_invalido
    )

    # --------------------------------------------------------
    # OPERACION 3: Registrar otro cliente correctamente.
    # --------------------------------------------------------

    cliente2 = Cliente(
        "C003",
        "Maria Gonzalez",
        "maria@gmail.com",
        "3109876543",
        30
    )

    ejecutar_operacion(
        "Operacion 3: Registro de segundo cliente",
        lambda: sistema.registrar_cliente(cliente2)
    )

    # --------------------------------------------------------
    # OPERACION 4: Crear y registrar una sala.
    # --------------------------------------------------------

    sala = ReservaSala(
        "S001",
        50000,
        20
    )

    ejecutar_operacion(
        "Operacion 4: Registro de sala",
        lambda: sistema.registrar_servicio(sala)
    )

    # --------------------------------------------------------
    # OPERACION 5: Crear y registrar equipos.
    # --------------------------------------------------------

    equipos = AlquilerEquipo(
        "E001",
        15000,
        3
    )

    ejecutar_operacion(
        "Operacion 5: Registro de alquiler de equipos",
        lambda: sistema.registrar_servicio(equipos)
    )

    # --------------------------------------------------------
    # OPERACION 6: Crear y registrar una asesoria.
    # --------------------------------------------------------

    asesoria = Asesoria(
        "A001",
        80000,
        "Desarrollo de software"
    )

    ejecutar_operacion(
        "Operacion 6: Registro de asesoria",
        lambda: sistema.registrar_servicio(asesoria)
    )

    # --------------------------------------------------------
    # OPERACION 7: Intentar crear un servicio incorrecto.
    # --------------------------------------------------------

    def servicio_invalido():

        servicio = ReservaSala(
            "S002",
            -5000,
            10
        )

        return sistema.registrar_servicio(servicio)

    ejecutar_operacion(
        "Operacion 7: Creacion de servicio invalido",
        servicio_invalido
    )

    # --------------------------------------------------------
    # OPERACION 8: Crear una reserva correctamente.
    # --------------------------------------------------------

    reserva1 = None

    def crear_reserva1():

        nonlocal reserva1

        reserva1 = sistema.crear_reserva(
            "R001",
            cliente1,
            sala,
            2
        )

        return reserva1.describir()

    ejecutar_operacion(
        "Operacion 8: Creacion de reserva",
        crear_reserva1
    )

    # --------------------------------------------------------
    # OPERACION 9: Confirmar la reserva.
    # --------------------------------------------------------

    ejecutar_operacion(
        "Operacion 9: Confirmacion de reserva",
        reserva1.confirmar
    )

    # --------------------------------------------------------
    # OPERACION 10: Procesar reserva con impuesto.
    # --------------------------------------------------------

    ejecutar_operacion(
        "Operacion 10: Procesamiento con impuesto",
        lambda: reserva1.procesar(
            impuesto=0.19
        )
    )

    # --------------------------------------------------------
    # OPERACION 11: Intentar cancelar una reserva procesada.
    # --------------------------------------------------------

    ejecutar_operacion(
        "Operacion 11: Cancelacion no permitida",
        reserva1.cancelar
    )

    # --------------------------------------------------------
    # OPERACION 12: Crear una reserva con duracion invalida.
    # --------------------------------------------------------

    def reserva_invalida():

        return sistema.crear_reserva(
            "R002",
            cliente2,
            asesoria,
            20
        )

    ejecutar_operacion(
        "Operacion 12: Reserva con duracion invalida",
        reserva_invalida
    )

    # --------------------------------------------------------
    # OPERACION 13: Intentar reservar un servicio no disponible.
    # --------------------------------------------------------

    reserva2 = None

    def crear_reserva2():

        nonlocal reserva2

        sala.cambiar_disponibilidad(False)

        reserva2 = sistema.crear_reserva(
            "R003",
            cliente2,
            sala,
            1
        )

        return reserva2.describir()

    ejecutar_operacion(
        "Operacion 13: Crear reserva para sala no disponible",
        crear_reserva2
    )

    # --------------------------------------------------------
    # OPERACION 14: Intentar confirmar el servicio no disponible.
    # --------------------------------------------------------

    ejecutar_operacion(
        "Operacion 14: Confirmacion de servicio no disponible",
        reserva2.confirmar
    )

    # --------------------------------------------------------
    # OPERACION 15: Calcular costo con descuento e impuesto.
    # --------------------------------------------------------

    ejecutar_operacion(
        "Operacion 15: Calculo de asesoria con descuento",
        lambda: asesoria.calcular_costo(
            2,
            impuesto=0.19,
            descuento=0.10
        )
    )

    # --------------------------------------------------------
    # OPERACION 16: Intentar procesar una reserva pendiente.
    # --------------------------------------------------------

    ejecutar_operacion(
        "Operacion 16: Procesamiento de reserva pendiente",
        reserva2.procesar
    )

    # --------------------------------------------------------
    # OPERACION 17: Mostrar todos los clientes.
    # --------------------------------------------------------

    ejecutar_operacion(
        "Operacion 17: Listado de clientes",
        lambda: "\n".join(sistema.listar_clientes())
    )

    # --------------------------------------------------------
    # OPERACION 18: Mostrar todos los servicios.
    # --------------------------------------------------------

    ejecutar_operacion(
        "Operacion 18: Listado de servicios",
        lambda: "\n".join(sistema.listar_servicios())
    )

    # --------------------------------------------------------
    # OPERACION 19: Mostrar todas las reservas.
    # --------------------------------------------------------

    ejecutar_operacion(
        "Operacion 19: Listado de reservas",
        lambda: "\n".join(sistema.listar_reservas())
    )

    # --------------------------------------------------------
    # OPERACION 20: Cancelar la segunda reserva.
    # --------------------------------------------------------

    ejecutar_operacion(
        "Operacion 20: Cancelacion de reserva pendiente",
        reserva2.cancelar
    )

    print("\n" + "=" * 55)
    print("SISTEMA SOFTWARE FJ FINALIZADO")
    print("El programa continuo funcionando ante los errores.")
    print("Revise el archivo software_fj.log para consultar eventos.")
    print("=" * 55)



if __name__ == "__main__":
    ejecutar_demostracion()
