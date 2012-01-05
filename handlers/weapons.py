##todo: make constants all caps, alter the getWeapon function so it capitalizes all input

# Weapongroups are at the bottom
class Weapons:
    ##Enviroment
    DEATH="Death"
    SOLDIER_COLLISION="SoldierCollision"
    ROADKILL="RoadKill"
    DAMAGE_AREA="DamageArea"
    SUICIDE="Suicide"

    ##Carbines
    M4A1="M4A1"
    G36C="Weapons/G36C/G36C"
    AKS74U="AKS-74u"
    A91="Weapons/A91/A91"
    SG553="SG 553 LB"

    ##Assault Rifles
    F2000="F2000"
    M16A4="M16A4"
    AEK="AEK-971"
    AN94="AN-94 Abakan"
    KH2002="Weapons/KH2002/KH2002"
    M416="Weapons/M416/M416"
    AK74="Weapons/AK74M/AK74"
    G3A3="Weapons/G3A3/G3A3"
    M416="Weapons/M416/M416"

    ##Handguns
    M1911="M1911"
    MP412REX="Weapons/MP412Rex/MP412REX"
    M9="M9"
    G18="Glock18"
    MP443="Weapons/MP443/MP443"
    MAGNUM="Taurus .44"
    M93R="M93R"

    ##Sniper Rifles
    SV98="SV98"
    MK11="Mk11"
    SKS="SKS"
    M98B="Model98B"
    SVD="SVD"
    M40A5="M40A5"
    M39="M39"

    #Light Mashine Guns
    RPK74M="RPK-74M"
    M249="M249"
    M240="M240"
    TYPE88="Type88"
    M27IAR="M27IAR"
    PKP="Pecheneg"
    M60="M60"

    ##Shotguns
    M1014="M1014"
    USAS="USAS-12"
    MCS="870MCS"
    SAIGA="Siaga20k"
    DAO="DAO-12"

    ## Personal Defense Weapons and SMGs
    ASVAL="AS Val"
    PDWR="Weapons/MagpulPDR/MagpulPDR"
    P90="Weapons/P90/P90"
    MP7="MP7"
    UMP="Weapons/UMP45/UMP45"
    PP2000="PP-2000"

    ##Rockets
    SMAW="SMAW"
    RPG="RPG-7"

    ##Knife
    MELEE="Melee" #One hit knife w animation
    KNIFE="Weapons/Knife/Knife" #multiple hits

    ##Misc
    M67="M67" #Grenade
    M320="M320"
    AT_MINE="M15 AT Mine"
    C4="Weapons/Gadgets/C4/C4"
    REPAIR_TOOL="Repair Tool"
    CLAYMORE="Weapons/Gadgets/Claymore/Claymore"
    M26_MASS="M26Mass"


    CARBINES=[M4A1, G36C, AKS74U, A91, SG553]

    ASSAULT_RIFLES=[F2000, M16A4, AEK, AN94, KH2002, M416, AK74, G3A3]

    HANDGUNS=[M1911, MP412REX, M9, G18, MP443, MAGNUM, M93R]

    SNIPER_RIFLES=[SV98, MK11, SKS, M98B, SVD, M40A5, M39]

    LMGS=[RPK74M, M249, M240, TYPE88, M27IAR, PKP, M60]

    SHOTGUNS=[M1014, USAS, MCS, SAIGA, DAO]

    PDW=[ASVAL, PDWR, P90, MP7, UMP, PP2000]

    ROCKET_LAUNCHERS=[SMAW, RPG]

    KNIFE=[MELEE, KNIFE]

    EXPLOSIVES=ROCKET_LAUNCHERS.extend([M320])

    EXPLOSIVE_GADGETS=[AT_MINE, C4, CLAYMORE]

#    def __init__(self):
#        ##Enviroment
#        self.Death="Death" #death by vehicle or mortar
#        self.SoldierCollision="SoldierCollision"
#        self.RoadKill="RoadKill"
#        self.DamageArea="DamageArea"
#        self.Suicide="Suicide"
#
#        ##Carabines
#        self.M4A1="M4A1"
#        self.G36C="Weapons/G36C/G36C"
#        self.AKS74U="AKS-74u"
#        self.A91="Weapons/A91/A91"
#        self.SG553="SG 553 LB"
#
#        ##Assault Rifles
#        self.F2000="F2000"
#        self.M16A4="M16A4"
#        self.AEK="AEK-971"
#        self.AN94="AN-94 Abakan"
#        self.KH2002="Weapons/KH2002/KH2002"
#        self.M416="Weapons/M416/M416"
#        self.AK74="Weapons/AK74M/AK74"
#        self.G3A3="Weapons/G3A3/G3A3"
#        self.M416="Weapons/M416/M416"
#
#        ##Handguns
#        self.M1911="M1911"
#        self.MP412REX="Weapons/MP412Rex/MP412REX"
#        self.M9="M9"
#        self.G18="Glock18"
#        self.MP443="Weapons/MP443/MP443"
#        self.Magnum="Taurus .44"
#        self.M93R="M93R"
#
#        ##Sniper Rifles
#        self.SV98="SV98"
#        self.MK11="Mk11"
#        self.SKS="SKS"
#        self.M98B="Model98B"
#        self.SVD="SVD"
#        self.M40A5="M40A5"
#        self.M39="M39"
#
#        #Light Mashine Guns
#        self.RPK74M="RPK-74M"
#        self.M249="M249"
#        self.M240="M240"
#        self.Type88="Type88"
#        self.M27IAR="M27IAR"
#        self.PKP="Pecheneg"
#        self.M60="M60"
#
#        ##Shotguns
#        self.M1014="M1014"
#        self.USAS="USAS-12"
#        self.MCS="870MCS"
#        self.Saiga="Siaga20k"
#        self.DAO="DAO-12"
#
#        ## Personal Defense Weapons and SMGs
#        self.ASVAL="AS Val"
#        self.PDWR="Weapons/MagpulPDR/MagpulPDR"
#        self.P90="Weapons/P90/P90"
#        self.MP7="MP7"
#        self.UMP="Weapons/UMP45/UMP45"
#        self.PP2000="PP-2000"
#
#        ##Rockets
#        self.SMAW="SMAW"
#        self.RPG="RPG-7"
#
#        ##Knife
#        self.Melee="Melee" #One hit knife w animation
#        self.Knife="Weapons/Knife/Knife" #multiple hits
#
#        ##Misc
#        self.M67="M67" #Grenade
#        self.M320="M320"
#        self.ATMine="M15 AT Mine"
#        self.C4="Weapons/Gadgets/C4/C4"
#        self.RepairTool="Repair Tool"
#        self.Claymore="Weapons/Gadgets/Claymore/Claymore"
#        self.M26Mass="M26Mass"
#
#        ###################
#
#        self.Carabines=[self.M4A1, self.G36C, self.AKS74U, self.A91, self.SG553]
#
#        self.AssaultRifles=[self.F2000, self.M16A4, self.AEK, self.AN94, self.KH2002, self.M416, self.AK74, self.G3A3]
#
#        self.Handguns=[self.M1911, self.MP412REX, self.M9, self.G18, self.MP443, self.Magnum, self.M93R]
#
#        self.SniperRifles=[self.SV98, self.MK11, self.SKS, self.M98B, self.SVD, self.M40A5, self.M39]
#
#        self.LMGs=[self.RPK74M, self.M249, self.M240, self.Type88, self.M27IAR, self.PKP, self.M60]
#
#        self.Shotguns=[self.M1014, self.USAS, self.MCS, self.Saiga, self.DAO]
#
#        self.PDW=[self.ASVAL, self.PDWR, self.P90, self.MP7, self.UMP, self.PP2000]
#
#        self.RocketLaunchers=[self.SMAW, self.RPG]
#
#        self.Knife=[self.Melee, self.Knife]
#
#        self.Explosives=self.RocketLaunchers.extend([self.M320])
#
#        self.ExplosiveGadgets=[self.ATMine, self.C4, self.Claymore]
        
    def getWeapon(self, name):
        try:
            weapon = getattr(self, str(name).upper())
        except AttributeError:
            return False
        else:
            return weapon