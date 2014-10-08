import piglass
import os

WLAN = "wlan0"

ncfile = piglass.readFile("app/wifimanager/networks.conf")
NET = ncfile[0].split("=")[0]
KEY = ncfile[0].split("=")[1]

def run():
    return

def init():
    return

def onSpeechInput(s):
    print s
    if s == "connect":
        wifiUp()
        scan()
        connect()
    if s == "disconnect":
        wifiDown()
    if s == "scan":
        scan()
        connect()
    if s == "restart":
        wifiDown()
        wifiUp()
        scan()
        connect()

def wifiUp():
    os.system("sudo ifconfig "+WLAN+" up")

def wifiDown():
    os.system("sudo ifconfig "+WLAN+" down")

def scan():
    os.system("sudo iwlist "+WLAN+" scan")

def connect():
    os.system("sudo ifconfig "+WLAN+" essid "+NET+" key s:"+KEY)
    os.system("sudo dhclient "+WLAN)

