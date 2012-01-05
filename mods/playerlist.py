name = "Playerlist Module"
author = "codesuela"

import base, time

class Bf3Mod(base.Bf3Mod):
    def onLoad(self):
        self.updateTimeout = 3
        self.lastUpdate = 0
        self.initPlayerlist()


    def initPlayerlist(self):
        self.playerList = []
        self.playerListOK = self.updatePlayerlist()
        self.playerListOutdated = False
        self.haltUpdateList = False

    def updatePlayerlist(self):
        pList = self.actionHandler.execCommand(["admin.listPlayers", "all"])
        if pList.pop(0) == "OK":
            self.playerList = pList
            return True
        else:
            return False

    def getVal(self, playerName, valName):
        playerIndex = False
        if self.playerListOK:
            try:
                valIndex = self.playerList.index(valName)
            except ValueError:
                # "unknown player or value name"
                return False
            else:
                for i in range(0, len(self.playerList)):
                    if(self.playerList[i].lower() == playerName.lower()): playerIndex = i
                if(playerIndex):
                    #offset=self.playerList[0]
                    i = valIndex + playerIndex - 1
                    return self.playerList[i]
                else:
                    return False

    def getTotalPlayers(self):
        if self.playerListOK:
            offset = self.playerList[0]
            return self.playerList[int(offset) + 1]
        else:
            return 0

    def playerOnJoin(self, name, guid):
        self.playerListOutdated = True

    def playerOnLeave(self, name, pInfo):
        self.playerListOutdated = True

    def playerOnSquadChange(self, name, teamId, squadId):
        self.playerListOutdated = True

    def playerOnTeamChange(self, name, teamId, squadId):
        self.playerListOutdated = True

    def onEveryEvent(self):
        if self.lastUpdate + self.updateTimeout < time.time():
            if (not self.playerListOK or self.playerListOutdated) and not self.haltUpdateList:
                self.playerListOK = self.updatePlayerlist()
                if self.playerListOK:
                    self.playerListOutdated = False



    def serverOnRoundOver(self, winningTeam):
        self.playerListOK = False
        self.haltUpdateList = True
        self.playerListOutdated = True
        self.playerList = []

    def serverOnLevelLoaded(self, levelName, gamemode, roundsPlayed, roundsTotal):
        self.initPlayerlist()

    def playerInGame(self, playerName):
        if self.playerListOK:
            if self.getVal(playerName, 'guid'): return True
            else: return False
        else:
            return False

#this how a playerlist looks like (with indices):
#0    1       2     3        4          5       6         7
#"7" "name" "guid" "teamId" "squadId" "kills" "deaths" "score"
#8   
#"1"
# 9                     10                              11   12   13  14 15
#"abc" "EA_9CED4B3FF36BD61D0CBE12345DFC3A52" "2" "1" "0" "0" "0"
# 16                     17                              18   19   20  21 22
#"flippo"         "EA_9CED4B3FF36BD61D0CBE12345DFC3A52" "2" "1" "0" "0" "0"
#23                     24                              25   26   27  28 29
#"pokkoi"         "EA_9CED4B3FF36BD61D0CBE12345DFC3A52" "2" "1" "0" "0" "0"