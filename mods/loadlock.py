name = "Map Loading Module"
author = "codesuela"

import base


class Bf3Mod(base.Bf3Mod):
    def serverOnRoundOver(self, winningTeam):
        self.mapLoading = True

    def isMapLoading(self):
        return self.mapLoading

    def serverOnLevelLoaded(self, levelName, gamemode, roundsPlayed, roundsTotal):
        self.mapLoading = False


    def onLoad(self):
        self.mapLoading = False