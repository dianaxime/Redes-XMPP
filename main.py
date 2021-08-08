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
from registro import registro, eliminar

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
    parser.add_argument("-r", "--register", dest="register",
                        help="Is new user")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

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

    if opcion == "1":
        if registro(args.jid, args.password):
            print("¡Excelente! Ya tienes una cuenta en ALUMCHAT v.20.21 \n")
            opcion = input("¿Deseas iniciar sesion? y/n: ")
        else:
            print("Un error inesperado ha ocurrido")

    if opcion == "2" or opcion.lower() == "y":
        corriendo = True
        while corriendo:
            print("""
            *************************************************
                            ALUMCHAT v.20.21                
            *************************************************
            0. Mensajeria privada
            1. Unirme a un grupo
            2. Mensajeria de grupo
            3. Modificar mi estado
            4. Notificaciones
            5. Mis contactos
            6. Añadir contacto
            7. Buscar perfil de un usuario
            8. Buscar todos los usuarios
            9. Envio/recepcion de archivos
            10. Salir
            11. Borrar mi cuenta // CUIDADO //
            *************************************************
            """)
            opcion = input("Ingresa el ## de accion que deseas realizar: ") 
            if(opcion == "0"):
                recipient = input("¿A quien le quieres escribir hoy? ") 
                message = input("Mensaje... ")
                xmpp = Client(args.jid, args.password, recipient, message)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                xmpp.register_plugin('xep_0096') # Jabber Search
                xmpp.connect()
                xmpp.process(forever=False)
            if(opcion == "1"):
                pass
            if(opcion == "2"):
                pass
            if(opcion == "3"):
                pass
            if(opcion == "4"):
                pass
            if(opcion == "5"):
                pass
            if(opcion == "6"):
                pass
            if(opcion == "7"):
                pass
            if (opcion == "8"):
                pass
            if(opcion == "9"):
                pass
            if(opcion == "10"):
                corriendo = False
                print('\n ¡Hasta la proxima! \n')
            if(opcion == "11"):
                if registro(args.jid, args.password):
                    print("Tu cuenta en ALUMCHAT v.20.21 ha sido elimada permanentemente\n")
                    xmpp = None
                    corriendo = False
                else:
                    print("Un error inesperado ha ocurrido")