import logging
import threading
import slixmpp
import base64, time
from slixmpp import stanza
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message, show, status):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.recipient = recipient
        self.msg = message
        self.show = show
        self.stat = status
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("chatstate_active", self.status_active)
        self.add_event_handler("chatstate_inactive", self.status_inactive)
        self.add_event_handler("chatstate_composing", self.status_composing)
        self.add_event_handler("chatstate_paused", self.status_paused)
        self.add_event_handler("chatstate_gone", self.status_gone)

    async def start(self, event):
        self.send_presence(self.show, self.stat)
        await self.get_roster()
        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

    async def message(self, msg):
        if msg['type'] in ('chat'):
            sender = str(msg['from']).split("/")
            recipient = str(msg['to']).split("/")
            body = msg['body']
            print(str(sender[0]) + " >> " + str(recipient[0]) +  " >> " + str(body))
            self.change_status(self.recipient, 'composing')
            message = input("Escribe <<volver>> si deseas regresar al menu \n Mensaje... ")
            self.change_status(self.recipient, 'paused')
            if message == "volver":
                self.change_status(self.recipient, 'gone')
                self.disconnect()
            else:
                self.send_message(mto=self.recipient,
                                mbody=message, mtype='chat')

    def change_status(self, to, status):
        msg = self.make_message(
            mto=to,
            mfrom=self.boundjid.bare,
            mtype='chat'
        )
        msg['chat_state'] = status
        msg.send()

    def status_active(self, chatstate):
        print(str(chatstate['from']).split("/")[0] + " esta activo.")


    def status_inactive(self, chatstate):
        print(str(chatstate['from']).split("/")[0] + " esta inactivo.")


    def status_composing(self, chatstate):
        print(str(chatstate['from']).split("/")[0] + " esta escribiendo...")


    def status_paused(self, chatstate):
        print(str(chatstate['from']).split("/")[0] + " ha dejado de escribir.")


    def status_gone(self, chatstate):
        print(str(chatstate['from']).split("/")[0] + " se ha ido a hacer algo mas.")
