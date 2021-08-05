import sys
import aiodns
import asyncio
import logging
import xmpp
from prueba_status import Presence
import _thread

from slixmpp import ClientXMPP

if sys.platform == 'win32' and sys.version_info >= (3, 8):
     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Done...


class EchoBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        # self.add_event_handler("changed_status", self.wait_for_presences)
        # If you wanted more functionality, here's how to register plugins:
        # self.register_plugin('xep_0030') # Service Discovery
        # self.register_plugin('xep_0199') # XMPP Ping

        # self.register_plugin('xep_0107') # User mood
        # Here's how to access plugins once you've registered them:
        # self['xep_0030'].add_feature('echo_demo')
        self.schedule(name="menu", callback=menu, seconds=10, repeat=True)

    
    async def session_start(self, event):
        self.send_presence('chat', 'hello my friends!')
        await self.get_roster()
        
        #print("---------------")
        #print(event)
        # Most get_*/set_* methods from plugins use Iq stanzas, which
        # are sent asynchronously. You can almost always provide a
        # callback that will be executed when the reply is received.
        # raise KeyboardInterrupt

    async def menu(self):
        opcion = input("""
                        A: Create account
                        B: Log In
                        C: Log Out
                        D: Delete Account
                        E: Show ALL users and info about them
                        F: Add a user to my roster
                        G: Show contacts details
                        H: Send direct message
                        I: Join Chat room
                        J: Create Room
                        k: Send room message
                        L: Send File
                        Q: Quit/Exit
                        Please enter your choice: """)
        print(opcion)

    async def message(self, msg):
        print("........................")
        print(msg["from"])
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()

    async def wait_for_presences(self, pres):
        print("************")
        print(pres)
        self.received.add(pres['from'].bare)
        if len(self.recieved)>=len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

def registerNewUser(user, passw):
    usuario = user
    password = passw
    jid = xmpp.JID(usuario)
    cli = xmpp.Client(jid.getDomain(), debug=[])
    cli.connect()

    if xmpp.features.register(cli, jid.getDomain(), {'username': jid.getNode(), 'password': password}):
        return True
    else:
        return False       


def login():
    logging.basicConfig(level=logging.DEBUG,
                                format='%(levelname)-8s %(message)s')

    userName = input(
                "Type username please:   ")
    passWord = input("Type the password:    ")
    xmpp = EchoBot(userName, passWord)
    xmpp.connect()
    # xmpp.process(forever=True)
    return xmpp

def menu():
    while True:
        opcion = input("""
                        A: Create account
                        B: Log In
                        C: Log Out
                        D: Delete Account
                        E: Show ALL users and info about them
                        F: Add a user to my roster
                        G: Show contacts details
                        H: Send direct message
                        I: Join Chat room
                        J: Create Room
                        k: Send room message
                        L: Send File
                        Q: Quit/Exit
                        Please enter your choice: """)
        print(opcion)

"""async def main(cliente):
    await asyncio.gather(menu(),
    cliente.process())
"""

if __name__ == '__main__':
    # Ideally use optparse or argparse to get JID,
    # password, and log level.

    # registerNewUser("diana@alumchat.xyz", "123")
    cliente = None
    opcion = "Z"
    opcion = input("""
                        A: Create account
                        B: Log In
                        C: Log Out
                        D: Delete Account
                        E: Show ALL users and info about them
                        F: Add a user to my roster
                        G: Show contacts details
                        H: Send direct message
                        I: Join Chat room
                        J: Create Room
                        k: Send room message
                        L: Send File
                        Q: Quit/Exit
                        Please enter your choice: """)
    #while opcion != "Q":
    if (opcion == "A"):
        print("You are going to create account")
        userName = input(
            "Type username please:   ")
        passWord = input("Type the password:    ")
        # print(userName)
        # print(passWord)
        ansRegister = registerNewUser(userName, passWord)
        if (ansRegister):
            print("User succesfully created")
        else:
            print("Fail!!!! Try again")
    elif (opcion == "B"):
        cliente = login()
        cliente.process()
        #cliente.process(timeout=10)
        # asyncio.run(cliente.process())
            #try:
            #if cliente:
            #    cliente.process()
            #except KeyboardInterrupt:
    #_thread.start_new_thread(menu)
    #_thread.start_new_thread(cliente.process()) 
      
            