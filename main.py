import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser

# Importar clientes utiles
from mensaje import Client
from registro import registro, Eliminar
from roster import Rosters, AddRoster
from group import ChatGroup
from file import File

if __name__ == '__main__':
    parser = ArgumentParser(description=Client.__doc__)

    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")

    parser.add_argument("-s", "--show", dest="show",
                        help="show to use")
    parser.add_argument("-t", "--status", dest="status",
                        help="status to use")
    parser.add_argument("-r", "--register", dest="register",
                        help="Is new user")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')
    
    posible_status = {
        "1": "chat",
        "2": "away",
        "3": "dnd",
        "4": "xa",
    }

    print("""
    *************************************************
    ¡HOLA! Esto es ALUMCHAT v.20.21
    1. ¿Deseas crear una cuenta?
    2. ¿Deseas ingresar a tu cuenta?
    *************************************************
    """)
    opcion = input("Escribe aca la opcion que deseas: ")

    if opcion == "1" or opcion == "2":
        if args.jid is None:
            args.jid = input("Ingrese su nombre de usuario: ")
        if args.password is None:
            args.password = getpass("Ingrese su contraseña: ")
        args.show = "1"
        args.status = ""

    if opcion == "1":
        if registro(args.jid, args.password):
            print("¡Excelente! Ya tienes una cuenta en ALUMCHAT v.20.21 \n")
            opcion = input("¿Deseas iniciar sesion? y/n: ")
        else:
            print("Un error inesperado ha ocurrido")

    if opcion == "2" or opcion.lower() == "y":
        corriendo = True
        while corriendo:
            if (opcion != "8" and opcion != "9"):
                xmpp = File(args.jid, args.password, posible_status[args.show], args.status)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                xmpp.register_plugin('xep_0096') # Jabber Search
                xmpp.register_plugin('xep_0085') # Chat State Notifications
                xmpp.connect()
                xmpp.process(timeout=25)
                xmpp.disconnect()
            print("""
            *************************************************
                            ALUMCHAT v.20.21                
            *************************************************
            0. Mensajeria privada
            1. Mensaje de presencia
            2. Mensajeria de grupo
            3. Modificar mi estado
            4. Mis contactos
            5. Añadir contacto
            6. Mostrar perfil de un contacto
            7. Envio/recepcion de archivos
            8. Salir
            9. Borrar mi cuenta // CUIDADO //
            *************************************************
            """)
            opcion = input("Ingresa el ## de accion que deseas realizar: ") 
            if(opcion == "0"):
                recipient = input("¿A quien le quieres escribir hoy? ") 
                message = input("Mensaje... ")
                xmpp = Client(args.jid, args.password, recipient, message, posible_status[args.show], args.status)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                xmpp.register_plugin('xep_0096') # Jabber Search
                xmpp.register_plugin('xep_0085') # Chat State Notifications
                xmpp.connect()
                xmpp.process(forever=False)
            if(opcion == "1"):
                m_presencia = input("¿Que mensaje le quieres enviar a tus amig@s? ")
                xmpp = Rosters(args.jid, args.password, posible_status[args.show], args.status, show=False, message=m_presencia)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                xmpp.register_plugin('xep_0096') # Jabber Search
                xmpp.register_plugin('xep_0085') # Chat State Notifications
                xmpp.connect()
                xmpp.process(forever=False)
            if(opcion == "2"):
                room = input("¿A que room te quieres unir? ") 
                nick_name = input("¿Cual sobrenombre quieres para tu grupo? ")
                if '@conference.alumchat.xyz' in room:
                    xmpp = ChatGroup(args.jid, args.password, room, nick_name)
                    xmpp.register_plugin('xep_0030') # Service Discovery
                    xmpp.register_plugin('xep_0199') # XMPP Ping
                    xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                    xmpp.register_plugin('xep_0096') # Jabber Search
                    xmpp.register_plugin('xep_0085') # Chat State Notifications
                    xmpp.connect()
                    xmpp.process(forever=False)
            if(opcion == "3"):
                print("""
                1. Disponible
                2. No disponible
                3. No molestar
                4. Ausente
                """)
                args.show = input("¿En que estado te encuentras? ")
                stat = input("¿Deseas ingresar un estado personalizado? y/n: ")
                if stat.lower() == "y":
                    args.status = input("SUGERENCIA: Utiliza una frase divertida. \nEscribe aqui tu frase... ")
                xmpp = AddRoster(args.jid, args.password, posible_status[args.show], args.status)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                xmpp.register_plugin('xep_0096') # Jabber Search
                xmpp.register_plugin('xep_0085') # Chat State Notifications
                xmpp.connect()
                xmpp.process(forever=False)
            if(opcion == "4"):
                xmpp = Rosters(args.jid, args.password, posible_status[args.show], args.status)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                xmpp.register_plugin('xep_0096') # Jabber Search
                xmpp.register_plugin('xep_0085') # Chat State Notifications
                xmpp.connect()
                xmpp.process(forever=False)
            if(opcion == "5"):
                contact = input("¿Quien quieres que sea tu amig@? ") 
                xmpp = AddRoster(args.jid, args.password, posible_status[args.show], args.status, contact)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                xmpp.register_plugin('xep_0096') # Jabber Search
                xmpp.register_plugin('xep_0085') # Chat State Notifications
                xmpp.connect()
                xmpp.process(forever=False)
            if(opcion == "6"):
                contact = input("¿A quien quieres stalkear hoy? ") 
                xmpp = Rosters(args.jid, args.password, posible_status[args.show], args.status, contact)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                xmpp.register_plugin('xep_0096') # Jabber Search
                xmpp.register_plugin('xep_0085') # Chat State Notifications
                xmpp.connect()
                xmpp.process(forever=False)
            if (opcion == "7"):
                recipient = input("¿A quien le quieres escribir hoy? ") 
                xmpp = File(args.jid, args.password, posible_status[args.show], args.status, True, recipient)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                xmpp.register_plugin('xep_0096') # Jabber Search
                xmpp.register_plugin('xep_0085') # Chat State Notifications
                xmpp.connect()
                xmpp.process(forever=False)
            if(opcion == "8"):
                corriendo = False
                print('\n ¡Hasta la proxima! \n')
            if(opcion == "9"):
                xmpp = Eliminar(args.jid, args.password, posible_status[args.show], args.status)
                xmpp.connect()
                xmpp.process(forever=False)
                xmpp = None
                corriendo = False
                print("Tu cuenta ha sido eliminada exitosamente")

            