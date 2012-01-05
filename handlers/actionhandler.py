from misc_rcon_functions import *

class ActionHandler:
    def __init__(self,host, port, password):
        self.serverSocket=connectAndAuthenticate(host, port, password)

    def execCommand(self, command):
        logging.debug("Sending command:"+str(command))
        request = EncodeClientRequest(command)
        self.serverSocket.send(request)

        # Wait for response from server
        packet = self.serverSocket.recv(4096)	

        [isFromServer, isResponse, sequence, words] = DecodePacket(packet)

        # The packet from the server should 
        # For now, we always respond with an "OK"
        if not isResponse:
            logging.warn('Received an unexpected request packet from server, ignored:')
            #logging.warn(packet)

        packet=DecodePacket(packet)
        logging.debug("Printing Packet :")
        logging.debug(packet)
        return packet[3]
    
    def killPlayer(self, name):
        self.execCommand(["admin.killPlayer",name])
    
    def kickPlayer(self, name, reason):
        self.execCommand(["admin.kickPlayer", name, reason])
        
    def banPlayer(self, idType, id, timeout, reason=""):
        self.execCommand(["banList.add", idType, id, timeout, reason])
        
    def sayAll(self, message):
        self.execCommand(["admin.say", message, "all"])
    
    def sayTeam(self, message, team):
        self.execCommand(["admin.say", message, "team", team])
    
    def saySquad(self, message, squad):
        self.execCommand(["admin.say", message, "squad", squad])