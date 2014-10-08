import app.weather.pywapi as pywapi
import piglass

def init():
    global screen
    global currentCity
    global wfr
    global cid
    screen = piglass.getAppScreen()
    currentCity = ""
    cid = ""
    wfr = piglass.pygame.Surface([piglass.asWidth, piglass.asHeight-65])
    wfr.fill([180, 180, 200])

def onLoopRestarted():
    piglass.setAppText("Weather")

def run():
    screen.fill([180, 180, 200])
    screen.blit(piglass.bigfont.render(currentCity, 1, [50, 50, 50]), [2, 2])
    screen.blit(wfr, [0, 41])
    screen.blit(piglass.font.render("Results from Yahoo Weather", 1, [100, 100, 100]), [10, piglass.asHeight-23])

def getForecast(cc):
    global wfr
    global cid
    global currentCity
    currentCity = cc
    cid = pywapi.get_location_ids(currentCity).keys()[0]
    result = pywapi.get_weather_from_yahoo(cid, 'metric')
    wfr = piglass.render_textrect("Now: "+result["condition"]["temp"]+" degrees Celsius, "+result["condition"]["text"]+"\n"+
                                  "TMR: H "+result["forecasts"][1]["high"]+" L "+result["forecasts"][1]["low"]+", "+result["forecasts"][1]["text"]+"\n"+
                                  "NXT: H "+result["forecasts"][2]["high"]+" L "+result["forecasts"][2]["low"]+", "+result["forecasts"][2]["text"], piglass.font, piglass.pygame.Rect([0, 0, piglass.asWidth, piglass.asHeight-65]), [50, 50, 50], [180, 180, 200])

def onSpeechInput(speech):
    getForecast(speech)
    if piglass.APPS[0].name != "weather":
        piglass.activateApp(piglass.getApp("weather"))
