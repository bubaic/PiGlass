import datetime
import piglass

screen = piglass.getAppScreen()

def onLoopRestarted():
    piglass.setAppText("Clock")

def run():
    screen.fill([20, 20, 20])
    now = datetime.datetime.now().timetuple()
    date = str(now[1])+"/"+str(now[2])+"/"+str(now[0])
    time = str(now[3])+":"+str(now[4])
    screen.blit(exbfont.render(time, 1, (200, 200, 200)), [40, 30])
    screen.blit(piglass.bigfont.render(date, 1, (200, 200, 200)), [40, 140])

def onSpeechInput(s):
    if piglass.APPS[0].name != "clock":
        piglass.activateApp(piglass.getApp("clock"))

def init():
    global exbfont
    exbfont = piglass.pygame.font.Font("system/fonts/Roboto-Bold.ttf", 65)
