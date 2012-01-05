name = "Map Settings"
author = "codesuela"
requiredImports = ["punisher"]

import base, ConfigParser, logging


class Bf3Mod(base.Bf3Mod):
    def playerOnKill(self, killer, killed, weapon, headshot):
        if self.restrictedWeapons:
            if (weapon in self.restrictedWeapons["weapons"] and self.restrictedWeapons["mode"] == "bl") or (
            weapon not in self.restrictedWeapons["weapons"] and self.restrictedWeapons["mode"] == "wl"):
                self.punisher.strike(killer)


    def serverOnLevelLoaded(self, levelName, gamemode, roundsPlayed, roundsTotal):
        ## initialize new weapon restrictions
        if (int(roundsPlayed) + 1) == int(roundsTotal):
            self.restrictedWeapons = self.getRestrictedWeapons()
            self.setAnnouncements()

    def serverOnRoundOver(self, winningTeam):

        # todo this does not work reliably (the server doesn't send this event if the round does not end gracefully ie an admin changes the map mid game)
        # need to move everything to serverOnLevelLoaded

        if self.isLastRound():
            self.mapList = self.getMapList()
            nextMap = self.getNextMap()

            self.clearAnnouncements()

            ##reset altered settings
            self.restoreAlteredSettings()

            ##apply new settings
            self.prepareSettingsFor(nextMap["map"], nextMap["mode"])

    def onLoad(self):
        self.mapList = self.getMapList()

        self.alteredSettings = []
        self.defaultSettings = self.getDefaultSettings()
        self.punisher = self.modLoader.tryGetOtherModInstance("punisher")
        self.currentAnnouncements = []
        self.restrictedWeapons = []
        self.lastMap = self.getCurrentMap()["map"]

        #self.restrictedWeapons=self.getRestrictedWeapons()
        #self.setAnnouncements()


    def getRestrictedWeapons(self):
        curMap = self.getCurrentMap()
        whiteList = self.getCurrentMapConfig("weaponsWhitelist")
        blackList = self.getCurrentMapConfig("weaponsBlacklist")
        mode = "" #wl for whitelist, bl for blacklist

        if whiteList:
            weaponListStr = whiteList
            mode = "wl"
        elif blackList:
            weaponListStr = blackList
            mode = "bl"
        else:
            return False

        weaponList = []
        for w in weaponListStr.split(","):
            weapon = self.modLoader.weapons.getWeapon(w.strip())
            if weapon:
                if isinstance(weapon, basestring): # how to avoid isinstance here?
                    weaponList.append(weapon)
                else:
                    weaponList.extend(weapon)

        return {"mode": mode, "weapons": weaponList}

    def onEveryEvent(self):
        pass

    def getCurrentMapConfig(self, option):
        curMap = self.getCurrentMap()
        return self.getMapConfig(curMap["map"], curMap["mode"], option)

    def setAnnouncements(self):
        announce = self.getCurrentMapConfig("announce")
        if announce:
            self.currentAnnouncements = self.modLoader.announcer.addMessages(announce)

    def clearAnnouncements(self):
        if len(self.currentAnnouncements) > 0:
            self.modLoader.announcer.removeMessages(self.currentAnnouncements)

    def getMapList(self):
        mapList = self.actionHandler.execCommand(['mapList.list'])[3:]
        maps = [] # [int index : {"map": str MAPNAME, "mode", str MODE, rounds: int rounds}]
        for i in range(0, len(mapList), 3):
            mDict = {"map": mapList[i], "mode": mapList[i + 1], "rounds": mapList[i + 2]}
            maps.append(mDict)

        return maps

    def getMap(self, i): #i=1 current, i=2 next
        mapIndices = self.actionHandler.execCommand(["mapList.getMapIndices"])
        print mapIndices
        return self.mapList[int(mapIndices[int(i)])]

    def getNextMap(self):
        return self.getMap(2)

    def getCurrentMap(self):
        return self.getMap(1)

    def getDefaultSettings(self):
        defaultSettings = {}
        for setting in self.modConfig.get("defaultStartup", "startup").split("\n"):
            var = setting.split(" ", 1)
            try:
                defaultSettings[var[0].lower()] = var[1]
            except IndexError:
                logging.warn("invalid startup setting:")
                logging.warn(var)

        return defaultSettings

    def alterSetting(self, settings):
        self.alteredSettings.append(settings[0].lower())
        self.actionHandler.execCommand(settings)

    def getMapConfig(self, mapName, mode, option):
        mapStr = "%s @ %s" % (mapName, mode)

        if self.modConfig.has_section(mapStr):
            try:
                coms = self.modConfig.get(mapStr, option)
            except ConfigParser.NoOptionError:
                pass
            else:
                return coms
        return False

    def isLastRound(self):
        currentMap = self.getCurrentMap()
        if currentMap["rounds"] == 1:
            return True
        else:
            r = self.actionHandler.execCommand(["mapList.getRounds"])
            if int(r[2]) == (int(r[1]) + 1):
                return True
            else:
                return False

    def prepareSettingsFor(self, map, mode):
        coms = self.getMapConfig(map, mode, "sendCommands")
        if coms:
            for com in coms.split("|"):
                self.alterSetting(com.split(" ", 1))

    def restoreAlteredSettings(self):
        for setting in self.alteredSettings:
            self.actionHandler.execCommand([setting, self.defaultSettings[setting]])

        self.alteredSettings = []