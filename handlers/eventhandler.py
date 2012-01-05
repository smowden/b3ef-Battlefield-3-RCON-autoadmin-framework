import logging
from modloader import ModLoader


class EventHandler:
    def __init__(self, actionHandler, battleQuery):
        self.currentPlayers={}
        self.modLoader=ModLoader(actionHandler, battleQuery)

    def handle(self,packet):
        logging.debug(packet[3])

        if len(packet[3])>=2:
            event=packet[3]
            normalizedEvent=str(event[0]).replace(".o","O")
            
        
            logging.debug(normalizedEvent)
            
            if event!="punkBuster.onMessage":
                for m in self.modLoader.getMods():
                    try:
                        call = getattr(m, normalizedEvent)
                    except AttributeError:
                        logging.debug("unknown event")
                    else:
                        eventArgs=event[1:]
                        if "name" in eventArgs: #check for playerstats block and group it
                            nIndex=eventArgs.index("name")
                            playerStats=eventArgs[nIndex-1:]
                            eventArgs=eventArgs[:len(eventArgs)-len(playerStats)]
                            eventArgs.append(playerStats)
                            
                        call(*eventArgs)
                    m.onEveryEvent()