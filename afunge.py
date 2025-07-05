import os, json, random
from rich import print

intmem = []
strmem = []
memcur = 0

settings = None

runfile = mapfile = None
mapcont = runcont = None

time = 0

debug_tolerance = False
tolerance = False
inclusive_time = False

ignoreCheck = False

x = y = 0

def right():
    global x
    x += 1
def left():
    global x
    x -= 1
    if x > 0: x = 0
def up():
    global y
    y -= 1
    if y > 0: y = 0
def down():
    global y
    y += 1
nothing = lambda: 0

def allocateINT():
    global intmem
    intmem.append(0)
def allocateSTR():
    global strmem
    strmem.append("")
def inccur():
    global memcur
    memcur += 1
def deccur():
    global memcur
    memcur -= 1
def incint():
    global intmem, memcur
    intmem[memcur] += 1
def incinten():
    global intmem, memcur
    intmem[memcur] += 10
def decint():
    global intmem, memcur
    intmem[memcur] -= 1
def zerint():
    global intmem, memcur
    intmem[memcur] = 0
def clearint():
    global intmem
    intmem = []
def stradd():
    global strmem, intmem, memcur
    strmem[memcur] += chr(intmem[memcur])
def strclr():
    global strmem, memcur
    strmem[memcur] = ""
def strmemclr():
    global strmem
    strmem = []
def intout():
    global intmem, memcur
    print(intmem[memcur])
def strout():
    global strmem, memcur
    print(strmem[memcur])

functions = {
    ">": right,
    "<": left,
    "^": up,
    "v": down,
    "x": exit,
    "o": nothing,
    "0": nothing # ignore check, pass time
}

mapfunc = {
    "`": allocateINT,
    "~": allocateSTR,
    "+": inccur,
    "-": deccur,
    "=": incint,
    "9": incinten,
    "_": decint,
    "0": zerint,
    ")": clearint,
    "(": strmemclr,
    "*": stradd,
    "8": strclr,
    "1": intout,
    "!": strout
}

def AfungeException(e, ln, fn, lnfn):
    if tolerance:
        return "Error tolerated."
    if lnfn:
        print(f"[red]File {fn}, line {ln}\nAfunge Error: {e}[/red]")
    else:
        print(f"Afunge Error: {e}[/red]")
    if debug_tolerance:
        return "Exit tolerated."
    exit()

def init():
    global runfile, mapfile, mapcont, runcont, settings, tolerance, debug_tolerance, inclusive_time

    if not os.path.exists("afunge.json"):
        AfungeException("Afunge settings file was not found.")
    with open("afunge.json") as file:
        settings = json.load(file)
    
    if "main" not in settings:
        AfungeException("Main afunge file was not found in the afunge settings.")
    runfile = settings["main"]
    
    if "map" not in settings:
        mapfile = "hidden/defaultmap.afunge"
    else:
        mapfile = settings["map"]

    if "tolerant" in settings:
        tolerance = settings["tolerant"]
    if "debugTolerant" in settings:
        debug_tolerance = settings["debugTolerant"]
    if "inclusiveTime" in settings:
        inclusive_time = settings["inclusiveTime"]

    with open(mapfile) as file:
        mapcont = file.read()
    with open(runfile) as file:
        runcont = file.read()

def pos():
    global mapcont, x, y
    if len(mapcont.split("\n")) < y: y = len(mapcont.split)
    row = mapcont.split("\n")[y]
    if len(row) < x: x = len(row)
    col = row[x]
    # print(f"calling from pos. returning {col}. following is the row.\n{row}")
    return col

def check():
    # print(f"hey boss, pos is {pos()}, our coords are {x}, {y}")
    if pos() in mapfunc:
        # print(f"hey boss, we got a map function, it's {pos()}")
        mapfunc[pos()]()

def main():
    global time
    for ln in runcont.split("\n"):
        ln = ln.split("=")[0]
        for char in ln:
            if inclusive_time:
                time += 1
            if char in functions:
                if not inclusive_time:
                    time += 1
                # print(f"hey boss, we got a main function, it's {char}")
                functions[char]()
            if char != "0":
                check()
    input("Press enter to continue... > ")

init()
main()