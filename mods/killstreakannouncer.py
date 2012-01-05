name = "Killstreak Announcer"
author = "codesuela"

import base

class Bf3Mod(base.Bf3Mod):
    def onLoad(self):
        self.playerStreaks = {}

    def playerOnKill(self, killer, killed, weapon, headshot):
        killer = str(killer).strip()
        killed = str(killed).strip()

        if killer and killed: # disregard environmental and admin induced deaths
            if killer in self.playerStreaks:
                self.playerStreaks[killer] += 1
            else:
                self.playerStreaks[killer] = 1

            self.playerStreaks[killed] = 0

            if(self.playerStreaks[killer] == 4):
                self.actionHandler.sayAll("%s Mega Kill" % killer)
            elif(self.playerStreaks[killer] == 5):
                self.actionHandler.sayAll("%s Ultra Kill" % killer)
            elif(self.playerStreaks[killer] == 6):
                self.actionHandler.sayAll("%s Monster Kill" % killer)
            elif(self.playerStreaks[killer] == 7):
                for _ in range(2):
                    self.actionHandler.sayAll("%s Ludicrous Kill" % killer)

            elif(self.playerStreaks[killer] == 8):
                for _ in range(3):
                    self.actionHandler.sayAll(killer + " HOLY SHIT")

            elif(self.playerStreaks[killer] > 8):
                self.actionHandler.sayAll(killer + " IS LEGENDARY")


    def playerOnLeave(self, name, pInfo):
        try:
            del(self.playerStreaks[name])
        except KeyError:
            pass

    def serverOnRoundOver(self, winningTeam):
        del(self.playerStreaks)
        self.playerStreaks = {}