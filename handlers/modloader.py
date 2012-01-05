import logging
import ConfigParser
import announcer
import imp
import os
from weapons import Weapons

class ModLoader:
    """
    this class loads and instantiates all the mods and takes care of dependencies
    """


    def __init__(self, actionHandler, battleQuery):
        self.actionHandler=actionHandler
        self.battleQuery=battleQuery
        self.mods={}
        
        self.loadConfig()

    def loadConfig(self):
        config=ConfigParser.SafeConfigParser(allow_no_value=True)
        config.read('main.ini')
        
        self.mods["base"]=self.loadMod("base")
        
        self.Weapons=Weapons()

        self.announcer=announcer.Announcer(self.actionHandler)
        self.announcer.start()
        
        requiredImports=[]
        moduleImports={} 
        
        for mod in config.options("mods"):
            mod=str(mod).strip()
            if not mod in self.mods and mod!="base" and mod[0]!="#":
                logging.debug("Attempting to load module %s" % mod)
                curmod=self.loadMod(mod)
                if curmod:
                    self.mods[mod]=curmod
                    if hasattr(curmod, "requiredImports"):
                        requiredImports.extend(curmod.requiredImports)
                        moduleImports[mod]=curmod.requiredImports #this is used to check whether all dependencies are met before initializing the module
                    else:
                        moduleImports[mod]=[]
        
        failedImports=[]
        while len(requiredImports) > 0:
            impModule=requiredImports.pop()
            if not impModule in dir() or not impModule in self.mods:
                    logging.info("Trying to import additional required module %s :" % impModule)
                    
                    try:
                        file, pathname, descr=imp.find_module(impModule)
                    except ImportError:
                        iM=self.loadMod(impModule)
                        if iM:
                            if hasattr(iM, "requiredImports"):
                                requiredImports.extend(iM.requiredImports)
                            self.mods[impModule]=iM
                            logging.info("Successfully imported module %s!" % impModule)
                        else:
                            logging.info("Could not import %s! (does the module exist?)" % impModule)
                            failedImports.append(str(os.path.basename(impModule)))
                    else:
                        imp.load_module(impModule, file, pathname, descr)
                        logging.info("Successfully imported module %s !" % impModule)

        for n,m in self.mods.items(): #name, module instance
            logging.info("Trying to initalize mod %s" % n)
            unmet=set(moduleImports.setdefault(n,[])) & set(failedImports)
            if len(unmet) > 0:
                logging.info("Unmet dependencies for module %s :" % n)
                logging.info(unmet)
                logging.info("Unloading module!")
                del(self.mods[n])
            else:
                logging.info("Loaded %s ( %s ) by %s" % (m.name, n, m.author))
                modConfig = ConfigParser.SafeConfigParser(allow_no_value=True)
                modConfig.read('configs/%s.cfg' % os.path.basename(n))
                self.mods[n]=m.Bf3Mod(self, self.actionHandler, modConfig)
        
        for n,m in self.mods.items():
            self.mods[n].modInit()

    def loadMod(self, name):
        try:
            Bf3Mod=imp.load_source(name,'mods/%s.py' % os.path.basename(name))
        except Exception, e:
            logging.critical("Exception while importing module %s :" % name)
            logging.critical(e)
            return False
        else:
            return Bf3Mod

    

    def getMods(self):
        return self.mods.values()
    
    def tryGetOtherModInstance(self, modName):
        if modName in self.mods:
            return self.mods[modName]
        else:
            return False
