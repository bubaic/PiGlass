import piglass
import app.wolfram.wolframalpha as wolframalpha
screen = piglass.getAppScreen()
appid = '77QKHJ-PKA78UPLJG'
client = wolframalpha.Client(appid)

def init():
    global icon
    global bigicon
    icon = piglass.pygame.image.load("app/wolfram/wolfram.png")
    bigicon = piglass.pygame.image.load("app/wolfram/wolframBig.jpg")
def run():
    screen.fill([200, 180, 180])
    screen.blit(piglass.bigfont.render("Wolfram|Alpha", 1, [50, 50, 50]), [2, 2])
    screen.blit(bigicon, [80, 35])
    
def onSpeechInput(speech):
    print "Wolfram got:"+speech
    try:
        res = client.query(speech)
        title = "Results"
        text = "From Wolfram|Alpha\n"
        for p in res.results:
            if p.text != None:
                text += p.text
                text += "\n"
        n = piglass.Notification(title, text, icon)
        n.show()
    except:
        n = piglass.Notification("Wolfram failed.", "PiGlass could not get a response.", icon)
        n.show()

def onLoopRestarted():
    piglass.setAppText("Wolfram Alpha")
