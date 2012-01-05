name = "Min or max rank enforcer"
author = "codesuela"

import base, logging, ConfigParser

class Bf3Mod(base.Bf3Mod):
    def playerOnAuthenticated(self, name):
        if self.modLoader.battleQuery:
            self.modLoader.battleQuery.resolveQueryAndCallback(name, self, "bqCallback")
        else:
            logging.warn("Battlequery not enabled, could not get player stats")

    def bqCallback(self, playerName, jsonData):
        playerRank = int(jsonData["rank"])

        if playerRank < self.minRank:
            self.actionHandler.kickPlayer(playerName, "Minimum rank is %s" % str(self.minRank))
        elif playerRank > self.maxRank and self.maxRank != 0:
            self.actionHandler.kickPlayer(playerName, "Max rank is %s" % str(self.maxRank))

        return None


    def onLoad(self):
        self.minRank = 0
        self.maxRank = 0

        try:
            self.minRank = int(self.modConfig.get("settings", "minRank"))
        except ConfigParser.NoOptionError:
            pass

        try:
            self.maxRank = int(self.modConfig.get("settings", "maxRank"))
        except ConfigParser.NoOptionError:
            pass
         
                
        