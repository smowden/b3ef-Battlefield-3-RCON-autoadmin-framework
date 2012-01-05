#vars.vehicleSpawnAllowed false
name = "Log weapons"
author = "codesuela"

import base, os

class Bf3Mod(base.Bf3Mod):
    def playerOnKill(self, killer, killed, weapon, headshot):

        if os.path.exists("weapon.log"):
            weaps = open("weapon.log", "a+")
            allweaps = weaps.read()
            weaps.seek(weaps.tell()) #reset 

            try:
                allweaps.index(weapon)
            except ValueError:
                pass
            else:
                return
        else:
            weaps = open("weapon.log", "w")

        weaps.writelines("%s \n" % weapon)
        weaps.close()
                