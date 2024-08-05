import time
import zmq
import random
import json

fonts = {}

configfile = open("config.json", mode="r")
configjson = json.load(configfile)
configfile.close()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:" + str(configjson["port"]))

def loadfonts():
    f = open("fonts.json", mode="r", encoding="utf-8")
    jd = json.load(f)
    f.close()
    
    for font in jd["fonts"]:
        fdict = {}
        for k, v in zip(font["keys"], font["vals"]):
            fdict[k] = v
        fonts[font["name"].strip()] = fdict


def convert(param):
    paramlist = param.split(" ", 1)

    if len(paramlist) == 0:
        raise Exception("No font supplied")

    fontname = paramlist[0].strip()
    text = ""
    if len(paramlist) > 1:
        text = paramlist[1].strip()

    font = None
    if fontname in fonts:
        font = fonts[fontname]
    else:
        raise Exception("Invalid font provided")

    result = ""

    for c in text:
        if c in font:
            result += font[c]
        else:
            result += c

    return result

def fontlist():
    fl = sorted(list(fonts.keys()))
    return ", ".join(fl)

def sample(param):
    samplist = [
        "cursive",
        "gothic",
        "double",
        "fullwidth",
        "circle"
    ]
    result = ""
    for name in samplist:
        if name in fonts:
            result += name + ": " + convert(name + " " + param) + "\n"
    return result

def runcommand(command, param):
    if command == "convert":
        result = convert(param)
    elif command == "list":
        result = fontlist()
    elif command == "sample":
        result = sample(param)
    else:
        raise Exception("Invalid command")
    return result

    
loadfonts()
print("Starting font server...")
while True:
    message = socket.recv_string()
    print(f"Received request from the client: {message}")
    
    if len(message) > 0:
        msglist = message.split(" ", 1)
        command = msglist[0].strip()
        param = ""
        if len(msglist) > 1:
            param = msglist[1].strip()
        try:
            result = runcommand(command, param)
        except Exception as e:
            errmsg = "ERR " + str(e)
            socket.send_string(errmsg)
        else:
            result = "RES " + result
            socket.send_string(result)

context.destroy()
