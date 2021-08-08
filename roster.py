import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser

class Rosters(slixmpp.ClientXMPP):
    def __init__(self, jid, password, user=None, show=True, message=""):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.presences = threading.Event()
        self.contacts = []
        self.user = user
        self.show = show
        self.message = message

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        my_contacts = []
        try:
            self.get_roster()
        except IqError as e:
            print("Algo salio mal, intentalo de nuevo", e, "\n")
        except IqTimeout:
            print("ERROR 500: El server no esta respondiendo")
        
        self.presences.wait(3)

        my_roster = self.client_roster.groups()
        for group in my_roster:
            for user in my_roster[group]:
                show = 'Conectado'
                status = answer = ''
                conexions = self.client_roster.presence(user)
                username = str(user).split("@")[0]
                if conexions.items():
                    for answer, pres in conexions.items():
                        if pres['show']:
                            show = pres['show']
                        if pres['status']:
                            status = pres['status']
                else:
                    show = 'Desconectado'
                    
                my_contacts.append([
                    user,
                    status,
                    username,
                    show
                ])
                self.contacts = my_contacts

        if(self.show):
            if(not self.user):
                if len(my_contacts) == 0:
                    print('NO tienes contactos. FOREVER ALONE')
                else:
                    print('\nContactos:\n')
                    for contact in my_contacts:
                        print('\tJID:' + str(contact[0])  + '\tNombre de usuario:' + str(contact[2]) + '\tEstado:' + str(contact[1]) + '\tDisponibilidad:' + str(contact[3]))
            else:
                flag = True
                for contact in my_contacts:
                    if(contact[0] == self.user):
                        print('\tJID:' + str(contact[0]) + '\n\tNombre de usuario:' + str(contact[2]) + '\n\tEstado:' + str(contact[1]) + '\n\tDisponibilidad:' + str(contact[3]))
                        flag = False
                if flag:
                    print("\nNO se han encontrado resultados para esa busqueda\n")
        else:
            for JID in self.contacts:
                self.notification_(JID, self.message, 'active')

        self.disconnect()

    def notification_(self, to, body, my_type):

        message = self.Message()
        message['to'] = to
        message['type'] = 'chat'
        message['body'] = body

        if (my_type == 'active'):
            fragmentStanza = ET.fromstring("<active xmlns='http://jabber.org/protocol/chatstates'/>")
        elif (my_type == 'composing'):
            fragmentStanza = ET.fromstring("<composing xmlns='http://jabber.org/protocol/chatstates'/>")
        elif (my_type == 'inactive'):
            fragmentStanza = ET.fromstring("<inactive xmlns='http://jabber.org/protocol/chatstates'/>")
        message.append(fragmentStanza)

        try:
            message.send()
        except IqError as e:
            print("Algo salio mal, intentalo de nuevo", e, "\n")
        except IqTimeout:
            print("ERROR 500: El server no esta respondiendo")


class AddRoster(slixmpp.ClientXMPP):
    def __init__(self, jid, password, to):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.to = to

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        try:
            self.send_presence_subscription(pto = self.to) 
        except IqTimeout:
            print("ERROR 500: El server no esta respondiendo") 
        self.disconnect()
        