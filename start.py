from piglass import *

print "Starting GUI"
initialize()

tm = ThreadManager()
em = EventManager()
si = SpeechRecognizer()

clock = pygame.time.Clock()

print "Initializing apps"
for a in readFile("app/apps.conf"):
    startApp(a)
activateApp(getAppByName("home"))
setStopped(False)
stopNow = getStopped()
sendtowolfram = ["what", "how", "where", "when", "why"]
haswaited = 0
screen = getScreen()
while stopNow != True:
    clock.tick(30)
    haswaited += 1
    if haswaited >= 30:
        stopNow = getStopped()
        haswaited = 0
    tm.refreshAppBar()
    tm.refreshScreen()
    pygame.display.flip()
    if getNotification() == None:
        try:
            APPS[0].run()
        except:
            n = Notification("App Crashed", "The app "+APPS[0].displayName+" has crashed.")
            n.show()
            closeApp()
            raise
    if getNotification() != None:
        getNotification().render()
    for task in BGTASKS:
        task[1].run()
    if em.check() == True:
        if getNotification() != None:
            getNotification().remove()
            continue
        pygame.draw.rect(screen, [180, 200, 180], [0, 100, 320, 118])
        screen.blit(bigfont.render("Listening", 1, (50, 50, 50)), [20, 130])
        pygame.display.flip()
        rs = si.recognize()
        print rs
        act = si.parseBasicActions(rs[0][0])
        if act == False:
            act, cmd = si.parse("system/conf/speechlib.conf")
            if act == True:
                onSpeechInput(rs[0][0])
            if act == False:
                if len(APPS) > 0:
                    if APPS[0].focus == False:
                        for a in APPS:
                            act, cmd = si.parse(a.speechlib)
                            if act == True and cmd != "":
                                if a.sendStrippedCommands == True:
                                    a.onSpeechInput(fStrip(cmd, rs[0][0]))
                                    break
                                a.onSpeechInput(rs[0][0])
                                break
                    if APPS[0].focus == True:
                        a = APPS[0]
                        act, cmd = si.parse(a.speechlib)
                        if act == True and cmd != "":
                            if a.sendStrippedCommands == True:
                                a.onSpeechInput(fStrip(cmd, rs[0][0]))
                            if a.sendStrippedCommands == False:
                                a.onSpeechInput(rs[0][0])
                    if act == False:
                        for w in sendtowolfram:
                            if rs[0][0].startswith(w):
                                getApp("wolfram").onSpeechInput(rs[0][0])
print "Shut down all threads and exit successful"
