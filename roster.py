import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser

class Rosters(slixmpp.ClientXMPP):
    def __init__(self, jid, password, show1, status, user=None, show=True, message=""):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.presences = threading.Event()
        self.contacts = []
        self.user = user
        self.show = show
        self.show1 = show1
        self.stat = status
        self.message = message

    async def start(self, event):
        self.send_presence(self.show1, self.stat)
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
                        print('**** JID >> ' + str(contact[0])  + '\n**** Nombre de usuario >> ' + str(contact[2]) + '\n**** Estado >> ' + str(contact[1]) + '\n**** Disponibilidad >> ' + str(contact[3]) + "\n\n")
            else:
                flag = True
                for contact in my_contacts:
                    if(contact[0] == self.user):
                        print('**** JID >> ' + str(contact[0]) + '\n**** Nombre de usuario >> ' + str(contact[2]) + '\n**** Estado >> ' + str(contact[1]) + '\n**** Disponibilidad >> ' + str(contact[3]) + "\n\n")
                        flag = False
                if flag:
                    print("\nNO se han encontrado resultados para esa busqueda\n")
        else:
            for JID in self.contacts:
                self.presenceRoster(JID[0], self.message)

        self.disconnect()

    def presenceRoster(self, to, body):

        message = self.Message()
        message['to'] = to
        message['type'] = 'chat'
        message['body'] = body

        fragmentStanza = ET.fromstring("<active xmlns='http://jabber.org/protocol/chatstates'/>")
        message.append(fragmentStanza)

        try:
            message.send()
        except IqError as e:
            print("Algo salio mal, intentalo de nuevo", e, "\n")
        except IqTimeout:
            print("ERROR 500: El server no esta respondiendo")


class AddRoster(slixmpp.ClientXMPP):
    def __init__(self, jid, password, show, status, to=None):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.to = to
        self.show = show
        self.stat = status

    async def start(self, event):
        self.send_presence(self.show, self.stat)
        await self.get_roster()
        try:
            if self.to is not None:
                self.send_presence_subscription(pto = self.to) 
        except IqTimeout:
            print("ERROR 500: El server no esta respondiendo") 
        self.disconnect()
        