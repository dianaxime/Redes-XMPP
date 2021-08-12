# CC-3067 Redes
# Proyecto de Cliente XMPP
# Diana Ximena de Leon Figueroa
# Carne 18607

import xmpp
import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser

# funcion para registrar usuarios

def registro(usuario, password):
    jid = xmpp.JID(usuario)
    cli = xmpp.Client(jid.getDomain(), debug=[])
    cli.connect()
    if xmpp.features.register(cli, jid.getDomain(), {'username': jid.getNode(), 'password': password}):
        return True
    else:
        return False


# Clase para eliminacion de un usuario

class Eliminar(slixmpp.ClientXMPP):
    def __init__(self, jid, password, show, status):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.user = jid
        self.show = show
        self.stat = status
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.send_presence(self.show, self.stat)
        self.get_roster()
        self.delete_account()
        

    def delete_account(self):
        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = self.user
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        delete.append(fragment)

        try:
            delete.send()
            print("Tu cuenta en ALUMCHAT v.20.21 ha sido elimada permanentemente\n")
            self.disconnect()
        except IqError as e:
            print("Un error inesperado ha ocurrido", e)
        except IqTimeout:
            print("ERROR 500: El server no esta respondiendo")
        except Exception as e:
            print(e)  