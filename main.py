#ticket count var: vars.gameModeCounter 200

import ConfigParser
import logging
import datetime
import argparse

from handlers.eventhandler import EventHandler
from handlers.actionhandler import ActionHandler
from handlers.misc_rcon_functions import *

from battlequery import BattleQuery


def launch(args):
    logging.basicConfig(filename=datetime.date.strftime(datetime.datetime.today(),"logs/%Y%m%d_%H%M%S")+'.log',level=logging.DEBUG)

    formatter = logging.Formatter('%(levelname)s - %(message)s')
    consoleLogger = logging.StreamHandler()
    consoleLogger.setLevel(logging.INFO)
    consoleLogger.setFormatter(formatter)
    logging.getLogger('').addHandler(consoleLogger)

    config=ConfigParser.SafeConfigParser(allow_no_value=True)
    config.read("main.ini")

    serverSocket=connectAndAuthenticate(args.server_ip, args.server_port, args.server_password)
    #serverSocket=False


    if config.getboolean("battlequery", "enable"):
        bQ=BattleQuery()
        bQ.setup()
        if not args.bq_username or not args.bq_password:
            bQ.authenticate(args.bq_username, args.bq_password)
        bQ.start()
    else:
        bQ=False


    aHandler=ActionHandler(args.server_ip, args.server_port, args.server_password)
    eHandler=EventHandler(aHandler, bQ)

    if serverSocket:
        logging.info('Enabling events...')

        enableEventsRequest = EncodeClientRequest( [ "admin.eventsEnabled", "true" ] )
        serverSocket.send(enableEventsRequest)

        enableEventsResponse = serverSocket.recv(4096)
        logging.debug(DecodePacket(enableEventsResponse))

        [isFromServer, isResponse, sequence, words] = DecodePacket(enableEventsResponse)

        # if the server didn't know about the command, abort
        if words[0] != "OK":
            sys.exit(0)

        logging.info('Now waiting for events.')

        while True:
            try:

                packet = serverSocket.recv(4096)
                if packet:
                    [isFromServer, isResponse, sequence, words] = DecodePacket(packet)
                else:
                    logging.info("no packet ")
            except Exception, e: # todo: more specific exception needs to be written down here
                #struct error, unpack requires ...
                logging.debug("exception occured, skipping packet")
                logging.debug(e)


            else:
                # If this was a command from the server, we should respond to it
                # For now, we always respond with an "OK"
                if not isResponse:
                    response = EncodeClientResponse(sequence, ["OK"])
                    serverSocket.send(response)
                else:
                    logging.warn('Received an unexpected response packet from server, ignoring')

                eHandler.handle(DecodePacket(packet))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Battlefield 3 enhancement framework launcher')

    parser.add_argument('-ip', action='store', dest='server_ip',
        help='Server IP address', required=True)

    parser.add_argument('-port', action='store', dest='server_port',
        help='Server Query Port usually something like 4XXX', required=True)

    parser.add_argument('-pw', action='store', dest='server_password',
        help='Server RCON password', required=True)

    parser.add_argument('-bqu', action='store', dest='bq_username', default=False,
        help='Battlelog username, optional but required for some mods that rely on querying Battlelog')

    parser.add_argument('-bqp', action='store', dest='bq_password', default=False,
        help='Battlelog password, optional but required for some mods that rely on querying Battlelog')

    launch(parser.parse_args())



