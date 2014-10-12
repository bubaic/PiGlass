import thread
import pygame
import os
import subprocess
import __builtin__
import system.FAKE_GPIO as GPIO

def initialize():
    global screen
    global appScreen
    global sWidth
    global sHeight
    global asWidth
    global asHeight
    global font
    global bigfont
    global inpin
    global appText

    global APPS
    global BGTASKS
    global settings

    global STOP_VF
    global STOP_SF

    global NOTIFICATION

    pygame.init()
    screen = pygame.display.set_mode([320, 240])#Add fullscreen and 0, 0 later
    sWidth = screen.get_width()
    sHeight = screen.get_height()
    asWidth = sWidth
    asHeight = sHeight - 22
    appScreen = pygame.Surface([asWidth, asHeight])
    appText = "PiGlass 1.0"
    font = pygame.font.Font("system/fonts/Roboto-Regular.ttf", 20)
    bigfont = pygame.font.Font("system/fonts/Roboto-Bold.ttf", 30)
    inpin = 17
    GPIO.setmode(pygame)#Set to GPIO.BCM
    GPIO.setup(inpin, GPIO.IN)

    APPS = []
    BGTASKS = []
    NOTIFICATION = None
    settings = SyncedFile('system/mem.sync', {"sWidth":sWidth, "sHeight":sHeight})
    settings.sync()

    STOP_SF = SyncedFile("system/stop", "w", {"stop":False})
    STOP_VF = ValueFile("system/stop")

    __builtin__.APPS = APPS
    __builtin__.BGTASKS = BGTASKS
    __builtin__.font = font
    __builtin__.bigfont = bigfont

def getNotification():
    return NOTIFICATION

def getValidModule(path):
    mp = path.replace("/", ".").rstrip(".py").rstrip(".pyc")
    import imp
    if path.endswith(".py"):
        return imp.load_source(mp.split(".")[len(mp.split("."))-1], path, open(path, 'rU'))
    return imp.load_source(mp.split(".")[len(mp.split("."))-1], path, open(path+"/__init__.py", 'rU'))

def strToBool(s):
    if s == "True":
        return True
    if s == "False":
        return False

def getStopped():
    val = STOP_VF.get("stop", True)
    if val != None:
        return strToBool(val)
    return False

def getAppScreen():
    return appScreen

def getScreen():
    return screen

def getApp(name):
    for a in APPS:
        if a.name == name:
            return a
    return None

def setAppText(text):
    global appText
    appText = text

def setStopped(state):
    STOP_SF.store("stopped", state)
    STOP_SF.sync()

def readFile(path):
    fo = open(path, 'rU')
    tr = []
    for ln in fo.readlines():
        tr.append(ln.rstrip())
    fo.close()
    return tr            

def startApp(path, populate=True):
    global APPS
    avf = ValueFile(path+"pgapp.conf")
    ao = PGApp(avf.get('name'), avf.get('displayName'), avf.get('path'), avf.get('modulePath'), float(avf.get('version')))
    if len(APPS)>0:
        APPS[0].onLoopPaused()
    APPS.insert(0, ao)
    if populate:
        populateAppObject(ao)
    ao.start()
    setAppText(avf.get('displayName'))
    if avf.get("speechlib") != None:
        ao.speechlib = avf.get("speechlib")
    if avf.get("focus") != None:
        ao.focus = strToBool(avf.get("focus"))
    if avf.get("sendStrippedCommands") != None:
        ao.sendStrippedCommands = strToBool(avf.get("sendStrippedCommands"))
    return ao

def fStrip(a, b):
    return b[len(a)+1:]

def activateApp(ao):
    global APPS
    ao.onLoopRestarted()
    p = 0
    for a in APPS:
        if a == ao:
            APPS.insert(0, APPS.pop(p))
        p += 1

def startBGTask(path):
    global BGTASKS
    BGTASKS.append([path, getValidModule(path)])

def getAppByName(name):
    for a in APPS:
        if a.name == name:
            return a

def getAppByDisplayName(dname):
    for a in APPS:
        if a.displayName.lower() == dname.lower():
            return a

def closeApp():
    global APPS
    if len(APPS)>1:
        APPS[0].onLoopPaused()
        APPS.pop(0)
        if len(APPS)>0:
            APPS[0].onLoopRestarted()

def closeBGTask(path):
    global BGTASKS
    p = 0
    for task in BGTASKS:
        if task[0] == path:
            BGTASKS.pop(p)
        p += 1

def getTermData(speech, term, nextTerm=None):
    if nextTerm != None:
        return speech[speech.find(term)+len(term)+1:speech.find(nextTerm)]
    return speech[speech.find(term)+len(term)+1:]

def populateAppObject(ao):
    try:
        ao.run = ao.module.run
    except:
        print "Module "+ao.name+" defines no run() function!"
    try:
        ao.onLoopPaused = ao.module.onLoopPaused
    except:
        print "Module "+ao.name+" defines no onLoopPaused() function!"
    try:
        ao.onLoopRestarted = ao.module.onLoopRestarted
    except:
        print "Module "+ao.name+" defines no onLoopRestarted() function!"
    try:
        ao.run = ao.module.run
    except:
        print "Module "+ao.name+" defines no run() function!"
    try:
        ao.onSpeechInput = ao.module.onSpeechInput
    except:
        print "Module "+ao.name+" defines no onSpeechInput(cmd, speech) function!"


def render_textrect(string, font, rect, text_color=[200, 200, 200], background_color=[50, 50, 50], justification=0):
    final_lines = []
    requested_lines = string.splitlines()
    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            for word in words:
                if font.size(word)[0] >= rect.width:
                    return pygame.Surface(rect.size)
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 
    surface = pygame.Surface(rect.size) 
    surface.fill(background_color) 
    accumulated_height = 0 
    for line in final_lines: 
        if accumulated_height + font.size(line)[1] >= rect.height:
            return pygame.Surface(rect.size)
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                return pygame.Surface(rect.size)
        accumulated_height += font.size(line)[1]
    return surface

def installApp(path):
    import zipfile
    print "Installing application from "+path
    pkg = zipfile.ZipFile(path, 'r')
    pkg.extract("pgapp.conf", "system/")
    vf = ValueFile("system/pgapp.conf")
    name = vf.get("name")
    print "App Name: "+name
    print "Extracting"
    os.mkdir("app/"+name)
    pkg.extractall("app/"+name+"/")
    print "Adding to directory"
    aaf = open("app/apps.conf", 'a')
    print >> aaf, "app/"+name+"/"
    aaf.close()
    print "Added and finalized"
    print "Initializing"
    startApp("app/"+name+"/")
    return

def uninstallApp(name):
    print "Uninstalling "+name
    print "Removing from memory"
    activateApp(getApp(name))
    closeApp()
    pth = "app/"+name+"/"
    print "Removing folder"
    __import__("shutil").rmtree(pth)
    print "Removing from app entries"
    of = readFile("app/apps.conf")
    ff = []
    for ln in of:
        if ln != pth:
            ff.append(ln)
    f = open("app/apps.conf", 'w')
    for l in ff:
        print >> f, l
    f.close()
    print "Uninstalled"
    Notification("App Uninstalled", "The app "+name+" has been uninstalled.").show()

def checkUpdate(name):
    import urllib
    baseURL = 'https://sites.google.com/site/piglassapps/repository/'
    acnf = urllib.urlopen(baseURL+"apps.conf")
    lns = acnf.readlines()
    app = getApp(name)
    p = 0
    for l in lns:
        lns[p] = l.rstrip().split(":")
        p += 1
    for l in lns:
        if l[0] == name:
            if float(l[2]) > app.version:
                return True, baseURL+l[1]
    return False, ""

def updateAll():
    print "Updating all apps."
    names = []
    for a in APPS:
        names.append(a.name)
    for n in names:
        do, pth = checkUpdate(n)
        if do == True:
            installRemote(pth)
        if do == False:
            print n+" is already up to date."

def installRemote(pth):
    import urllib
    rf = urllib.urlretrieve(pth, "system/tmp_pkg.zip")
    installApp('system/tmp_pkg.zip')

def getPackageFromRemoteDisplayName(dname):
    import urllib
    baseURL = 'https://sites.google.com/site/piglassapps/repository/'
    acnf = urllib.urlopen(baseURL+"apps.conf")
    lns = acnf.readlines()
    p = 0
    for l in lns:
        lns[p] = l.rstrip().split(":")
        p += 1
    for l in lns:
        if l[3].lower() == dname.lower():
            return l[1]
    return None

class EventManager(object):
    """
    An EventManager is the controller governing inputs to PiGlass.
    """
    def __init__(self):
        self.sfo = ValueFile("system/button")
        
    def check(self):
        return GPIO.input(inpin)
            
class ThreadManager(object):
    """
    A ThreadManager controls level-0 and level-1 subthreads.
    PiGlass Apps are level-1 threads controlling PGApp Objects.
    Background Monitors are level-0 threads started by ThreadManager.
    """
    def __init__(self):
        print "New ThreadManager started"

    def startSub(self, level, path):
        if level == 0:
            self.__levelZero(path)
        if level == 1:
            self.__levelOne(path)

    def __levelZero(self, path):
        print "Starting new thread at level 0; path="+path
        try:
            thread.start_new(startBGTask, (path,))
        except:
            print "Error at execution!"

    def __levelOne(self, path):
        print "Starting new thread at level 1; path="+path
        try:
            thread.start_new(startApp, (path,))
        except:
            print "Error at execution!"

    def refreshScreen(self):
        screen.blit(appScreen, [0, 0])

    def refreshAppBar(self):
        pygame.draw.rect(screen, [100, 100, 100], [0, 200, 320, 240])
        screen.blit(font.render(appText, 1, [200, 200, 200]), [50, sHeight-23])
            

class PGApp(object):
    """
    A PGApp is the main part of constructing a PiGlass app. 
    It has three states: running, paused, and not running. Each of these has its own trigger.
    A PGApp is initialized by the system by parameters from the apps manifest.
    The system then calls the defined init funtion.
    """

    def __init__(self, name="PGApp", displayName="PGApp", path="system/jail.pgapp", modulePath="system/jail.pgapp/module.py", version=1.0, speechlib="system/conf/blank.conf"):
        self.name = name
        self.displayName = displayName
        self.path = path
        self.module = getValidModule(modulePath)
        self.version = version
        self.running = False
        self.paused = False
        self.speechlib = speechlib
        self.focus = False
        self.sendStrippedCommands = False

    def start(self):
        self.module.init()

    def run(self):
        self.running = True
        #empty by default

    def onLoopPaused(self):
        self.paused = True
        #Empty by default

    def onLoopRestarted(self):
        self.paused = False
        #Empty on default

    def onSpeechInput(self, speech):
        self.speech = speech
        #Empty by default

class ResourcePack(object):
    """
    A ResourePack is a preloaded object with all the resources for an app.
    It loads images as pygame.image objects and text files as lists of strings.
    """

    def __init__(self, toload):
        self.dict = {}
        self.IMG_EXT = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]
        for item in toload:
            add(item)
                    
    def get(self, item):
        return self.dict[item]
    
    def add(self, item):
        for ext in IMG_EXT:
            if item[1].endswith(ext):
                self.dict[item[0]] = pygame.image.load(item[1])
            else:
                self.dict[item[0]] = readFile(item[1])

class ValueFile(object):
    """
    A ValueFile is a file of x=y attributes with #comments.
    """

    def __init__(self, path):
        self.dict = {}
        self.path = path
        self.scan()

    def scan(self):
        contents = readFile(self.path)
        for ln in contents:
            if not ln.startswith("#"):
                try:
                    ls = ln.split("=")
                    self.dict[ls[0]] = ls[1]
                except:
                    self.dict[ls[0]] = None

    def get(self, value, rescan=False):
        if rescan:
            self.scan()
        try:
            return self.dict[value]
        except:
            return None

class LinuxScript(object):
    """
    A LinuxScript is a representation of a shell script.
    """

    def __init__(self, path, su=False, cdTo=None, async=False):
        self.path = path
        self.su = su
        self.cd = cdTo
        self.async = async

    def run(self):
        if self.cd != None:
            cmd = 'cd "'+self.cd+'" && sh "'+self.path+'"'
        if self.cd == None:
            cmd = 'sh "'+self.path+'"'
        if self.su:
            cmd = "sudo "+cmd
        if self.async:
            thread.start_new(os.system, (cmd,))
            return
        os.system(cmd)

class SyncedFile(object):
    """
    A SyncedFile is a dict synchronized with a file.
    The produced file is a valid ValueFile object.
    """

    def __init__(self, path, mode="w", initial={}):
        self.dict = initial
        self.path = path
        self.mode = mode

    def store(self, name, value):
        self.dict[name] = value

    def sync(self):
        if self.mode == "w":
            fo = open(self.path, 'w')
            for value in self.dict:
                print >> fo, value+"="+str(self.dict[value])
            fo.close()
        if self.mode == "r":
            fo = ValueFile(self.path)
            self.dict = fo.dict

class SpeechRecognizer(object):
    """
    A SpeechRecognizer provides the interfaces for parsing speech
    """
    def __init__(self):
        self.rm = getValidModule("system/fakespeech.py")
        self.recognizer = self.rm.Recognizer()
        self.recognizer.pause_threshold = 1.5
        self.reclist = []
        
    def recognize(self):
        #with self.rm.Microphone() as source:
        #   audio = self.recognizer.listen(source, 3)
        self.reclist = []
        source = self.rm.Microphone()
        audio = self.recognizer.record(source)
        #try:
        recd = self.recognizer.recognize(audio, True)
        for it in recd:
            self.reclist.append([it["text"], it["confidence"]*100])
        #except:
        #    self.reclist = [["no speech heard", 100]]
        return self.reclist

    def parse(self, libPath):
        lib = readFile(libPath)
        bestrec = self.reclist[0]
        for entry in lib:
            if bestrec[0].startswith(entry):
                return True, entry
        return False, ""

    def parseBasicActions(self, speech):
        if speech.startswith("notify"):
            tit = getTermData(speech, "title", "text")
            txt = getTermData(speech, "text")
            n = Notification(tit, txt)
            n.show()
            return True
        if speech.startswith("quit"):
            closeApp()
            return True
        if speech.startswith("close"):
            activateApp(getAppByName("home"))
            return True
        if speech.startswith("update"):
            updateAll()
            return True
        if speech.startswith("install"):
            installRemote('https://sites.google.com/site/piglassapps/repository/'+getPackageFromRemoteDisplayName(getTermData(speech, "install")))
        if speech.startswith("uninstall"):
            uninstallApp(getAppByDisplayName(getTermData(speech, 'uninstall')).name)
        return False

class Notification(object):
    def __init__(self, title, text, icon=None):
        print title
        print text
        self.title = bigfont.render(title, 1, (200, 200, 200))
        self.text = render_textrect(text, font, pygame.Rect(0, 0, asWidth, asHeight-43))
        self.icon = icon
    def show(self):
        global NOTIFICATION
        NOTIFICATION = self
        self.old = appText
        setAppText("Tap to dismiss")
        print "set notification"
    def remove(self):
        global NOTIFICATION
        NOTIFICATION = None
        setAppText(self.old)
        return
    def render(self):
        appScreen.fill([50, 50, 50])
        if self.icon != None:
            appScreen.blit(self.icon, [0, 0])
        if self.icon == None:
            pygame.draw.rect(appScreen, [200, 200, 200], [0, 0, 40, 40])            
        appScreen.blit(self.title, [40, 2])
        appScreen.blit(self.text, [0, 43])

def onSpeechInput(speech):
    if speech == "hi":
        Notification("Hi!", "Hello there!").show()
    if speech == "shutdown" or speech == "shut down":
        print "shutdown"
        setStopped(True)
        pygame.quit()
        #LinuxScript("system/scripts/shutdown.sh", True).run()
