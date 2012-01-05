name = "Votekickban Module"
author = "codesuela"
requiredImports = ["playerlist"]

import base, time

class Bf3Mod(base.Bf3Mod):
    def onLoad(self):
        self.resetCurVote()
        self.alreadyVotedOn = []
        self.playerList = self.modLoader.tryGetOtherModInstance("playerlist")
        self.voteTime = 80


    def resetCurVote(self):
        self.curVote = {'name': '', 'voters': [], 'guid': '', 'type': '', 'startTime': 0, 'y': 0, 'n': 0}

    def playerOnChat(self, name, text):
        if self.curVote["name"] == "":
            if("/votekick" in text or "/voteban" in text):
                params = str(text).split(" ")
                if(self.playerList.playerInGame(params[1])) and not params[1].lower() in self.alreadyVotedOn:
                    if params[0] == "/votekick":
                        self.actionHandler.sayAll("Starting a VOTEKICK on " + str(params[1]).upper())
                        self.curVote["type"] = "kick"

                    elif params[0] == "/voteban":
                        self.actionHandler.sayAll("Starting a VOTEBAN on " + str(params[1]).upper())
                        self.curVote["type"] = "ban"

                    self.curVote["startTime"] = time.time()
                    self.curVote["name"] = params[1]

                    self.actionHandler.sayAll("Type /y /yes or 1  to kick or ban %s" % str(params[1]).upper() )
                    self.actionHandler.sayAll("Type /n or /no or 0 if you want %s to stay" %  str(params[1]).upper())
                    self.actionHandler.sayAll("Vote is ending in  seconds" % str(self.voteTime))
        else:
            yText=["/y", "/yes", "y", "1"]
            nText=["/n", "/no", "n", "0"]
            if text in (yText + nText) and not name.lower() in self.curVote['voters']:

                self.curVote['voters'].append(name.lower())
                if text in yText:
                    self.curVote['y'] += 1
                elif text in nText:
                    self.curVote['n'] += 1
                self.actionHandler.sayAll("%s %s %s %s YES %s NO" % (self.curVote["type"].upper(), self.curVote["name"], self.curVote["y"], str(self.curVote["n"])))



    def onEveryEvent(self):
        if self.curVote["name"] != "":
            if self.curVote["startTime"] + self.voteTime < time.time():
                self.actionHandler.sayAll("Vote ended, result:")
                if (self.curVote["y"] + self.curVote["n"]) >= (int(self.playerList.getTotalPlayers()) / 2):
                    if self.curVote["y"] > self.curVote["n"]:
                        result = "y"
                    else:
                        result = "n"

                    if self.curVote["type"] == "kick" and result == "y":
                        self.actionHandler.sayAll("Player " + self.curVote["name"].upper() + " was KICKED")
                        self.actionHandler.kickPlayer(self.curVote["name"], "")
                    elif self.curVote["type"] == "ban" and result == "y":
                        self.actionHandler.banPlayer("name", self.curVote["name"], "999999", "you've got votebanned")
                        self.actionHandler.sayAll("Player "+self.curVote["name"].upper()+" was BANNED")
                    else:
                        self.actionHandler.sayAll("Player " + self.curVote["name"].upper() + " STAYS on the server")

                else:
                    self.actionHandler.sayAll("Too few players voted, 50 % required")
                self.resetCurVote()
                    
            
                        