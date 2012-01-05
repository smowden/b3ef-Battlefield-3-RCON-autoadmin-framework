name = "Punishment Module"
author = "codesuela"
requiredImports = ["playerlist", "loadlock"]

import base, time


class Bf3Mod(base.Bf3Mod):
    def strike(self, player):
        if self.modLoader.tryGetOtherModInstance("playerlist").playerInGame(player) and not self.modLoader.tryGetOtherModInstance("loadlock").isMapLoading():
            if player in self.playerStrikes:
                self.playerStrikes[player] += 1
            else:
                self.playerStrikes[player] = 1
                self.playerPunished[player] = 0

            self.punishPlayer(player)


    def onLoad(self):
        self.playerStrikes = {}
        self.playerPunished = {}
        self.slayOnSpawn = {}
        self.slayPlayerNow = []

    def playerOnChat(self, name, text):
        #for debug purposes
        if text == "/strikeme" or text == "/sm":
            self.strike(name)
        if text == "/resetstrikes":
            self.playerStrikes = {}
            self.playerPunished = {}


    def onEveryEvent(self):
        for name, strikes in self.playerStrikes.items():
            if name.strip() in self.slayOnSpawn:
                if time.time() > self.slayOnSpawn[name] + 2 and self.slayOnSpawn[name] != 0:
                    self.actionHandler.killPlayer(name)
                    del(self.slayOnSpawn[name])

    def punishPlayer(self, name):
        strikes = self.playerStrikes[name]

        punishKill = int(self.modConfig.get("kill", "strikes"))
        punishKillOnSpawn = int(self.modConfig.get("killOnSpawn", "strikes"))
        punishKick = int(self.modConfig.get("kick", "strikes"))
        punishBan = int(self.modConfig.get("ban", "strikes"))

        punishmentSet = [punishKill, punishKillOnSpawn, punishKick, punishBan]
        punishRange = (min(punishmentSet), max(punishmentSet))

        # its 4AM right now so this might be buggy, todo revisit

        if  ((strikes < punishKillOnSpawn and strikes >= punishKill and self.playerPunished[
                                                                        name] < punishKillOnSpawn) or (
        punishKill == punishRange[1] and strikes >= punishKill) ) and punishKill != 0:
            self.actionHandler.killPlayer(name)
            self.actionHandler.sayAll(self.parseAnnouncement(self.modConfig.get("kill", "announce"), name))
        elif ((strikes < punishKick and strikes >= punishKillOnSpawn and self.playerPunished[name] < punishKick) or (
        punishKillOnSpawn == punishRange[1] and strikes >= punishKillOnSpawn) ) and punishKillOnSpawn != 0:
            self.actionHandler.killPlayer(name)
            self.slayOnSpawn[name] = 0
            self.actionHandler.sayAll(self.parseAnnouncement(self.modConfig.get("killOnSpawn", "announce"), name))
        elif ((strikes < punishBan and strikes >= punishKick and self.playerPunished[name] < punishBan) or (
        punishKick == punishRange[1] and strikes >= punishKick) ) and punishKick != 0:
            self.actionHandler.kickPlayer(name, self.parseAnnouncement(self.modConfig.get("kick", "announce"), name))
            self.actionHandler.sayAll(self.parseAnnouncement(self.modConfig.get("kick", "announce"), name))
        elif ((strikes == punishBan and self.playerPunished[name] == punishBan - 1) and (
        punishBan == playerPunished[1] and strikes >= punishBan) ) and punishBan != 0:
            #todo: for a true permanent ban the id type needs to be guid, so the player name needs to be resolved to guid to ban
            self.actionHandler.banPlayer("name", name, str(self.modConfig.get("ban", "timeout")).split(" ")[0],
                self.parseAnnouncement(self.modConfig.get("ban", "announce"), name))
            self.actionHandler.sayAll(self.parseAnnouncement(self.modConfig.get("ban", "announce"), name))

        self.playerPunished[name] += 1


    def parseAnnouncement(self, announcement, name):
        return str(announcement).replace("##PLAYERNAME##", name)


    def playerOnSpawn(self, name, teamId):
        if name in self.slayOnSpawn:
            self.slayOnSpawn[name] = time.time()
            

        
        
    
        

    