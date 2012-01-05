#from insttest import *
name = "base"
author = "codesuela"

class Bf3Mod:
    def __init__(self, modLoaderInstance, actionHandler, modConfig=False):
        self.modLoader = modLoaderInstance
        self.actionHandler = actionHandler
        self.modConfig = modConfig


    def modInit(self):
        #basic init function, you should not replace this function with you own, for other initialization code use the onLoad method
        self.onLoad()

    # override these functions, for documentation see the official rcon protocol documentation in the /docs dir
    def playerOnAuthenticated(self, name):
        pass

    def playerOnJoin(self, name, guid):
        pass

    def playerOnLeave(self, name, pInfo):
        pass

    def playerOnSpawn(self, name, teamId):
        pass

    def playerOnKill(self, killer, killed, weapon, headshot):
        pass

    def playerOnChat(self, name, text):
        pass

    def playerOnSquadChange(self, name, teamId, squadId):
        pass

    def playerOnTeamChange(self, name, teamId, squadId):
        pass

    def punkBusterOnMessage(self, message):
        pass

    def serverOnLevelLoaded(self, levelName, gamemode, roundsPlayed, roundsTotal):
        pass

    def serverOnRoundOver(self, winningTeam):
        pass

    def serverOnRoundOverPlayers(self, playerInfos):
        pass

    def serverOnRoundOverTeamScores(self, teamScores):
        pass

    def onLoad(self):
        pass

    def onEveryEvent(self):
        pass

