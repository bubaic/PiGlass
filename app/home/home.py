import piglass

evmon = piglass.EventManager()
screen = piglass.getAppScreen()

def init():
    print "Home initialized"

def run():
    screen.fill([200, 200, 200])
    
def onSpeechInput(speech):
    print "Home got:"+speech
    if speech != "no speech heard":
        speech = speech.lower()
        for a in piglass.APPS:
            if a.displayName.lower() == speech:
                piglass.activateApp(a)
def onLoopRestarted():
    piglass.setAppText("Home")
