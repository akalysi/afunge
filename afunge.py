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

cur_ln = -1
cur_char = -1

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
    if len(intmem) > memcur:
        intmem[memcur] += 1
    else:
        AfungeException(f"No integer allocated to be at index {memcur}.", cur_ln, cur_char, True)
def decint():
    global intmem, memcur
    if len(intmem) > memcur:
        intmem[memcur] -= 1
    else:
        AfungeException(f"No integer allocated to be at index {memcur}.", cur_ln, cur_char, True)
def zerint():
    global intmem, memcur
    if len(intmem) > memcur:
        intmem[memcur] = 0
    else:
        AfungeException(f"No integer allocated to be at index {memcur}.", cur_ln, cur_char, True)
def clearint():
    global intmem
    intmem = []
def dubint():
    global intmem, memcur
    if len(intmem) > memcur:
        intmem[memcur] *= 2
    else:
        AfungeException(f"No integer allocated to be at index {memcur}.", cur_ln, cur_char, True)
def stradd():
    global strmem, intmem, memcur
    if len(intmem) > memcur and len(strmem) > memcur:
        strmem[memcur] += chr(intmem[memcur])
    if len(intmem) < memcur:
        AfungeException(f"No integer allocated to be at index {memcur}.", cur_ln, cur_char, True)
    if len(strmem) < memcur:
        AfungeException(f"No string allocated to be at index {memcur}.", cur_ln, cur_char, True)
def strclr():
    global strmem, memcur
    if len(strmem) > memcur:
        strmem[memcur] = ""
    else:
        AfungeException(f"No string allocated to be at index {memcur}.", cur_ln, cur_char, True)
def strmemclr():
    global strmem
    strmem = []
def intout():
    global intmem, memcur
    if len(intmem) > memcur:
        print(intmem[memcur])
    else:
        AfungeException(f"No integer allocated to be at index {memcur}.", cur_ln, cur_char, True)
def strout():
    global strmem, memcur
    if len(strmem) > memcur:
        print(strmem[memcur])
    else:
        AfungeException(f"No string allocated to be at index {memcur}.", cur_ln, cur_char, True)
def ifright():
    global x, intmem, memcur
    if len(intmem) > memcur:
        if time > intmem[memcur]:
            x += 1
    else:
        AfungeException(f"No integer allocated to be at index {memcur}.", cur_ln, cur_char, True)
def ifleft():
    global x, intmem, memcur
    if len(intmem) > memcur:
        if time > intmem[memcur]:
            x -= 1
    else:
        AfungeException(f"No integer allocated to be at index {memcur}.", cur_ln, cur_char, True)
def ifup():
    global y, intmem, memcur
    if len(intmem) > memcur:
        if time > intmem[memcur]:
            x -= 1
    else:
        AfungeException(f"No integer allocated to be at index {memcur}.", cur_ln, cur_char, True)
def ifdown():
    global y, intmem, memcur
    if len(intmem) > memcur: 
        if time > intmem[memcur]:
            y += 1
    else:
        AfungeException(f"No integer allocated to be at index {memcur}.", cur_ln, cur_char, True)
def test():
    print("test")

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
    "_": decint,
    "0": zerint,
    ")": clearint,
    "d": dubint,
    "(": strmemclr,
    "*": stradd,
    "8": strclr,
    "1": intout,
    "!": strout,
    "^": ifup,
    "<": ifleft,
    "v": ifdown,
    ">": ifright,
    "t": test
}

def AfungeException(e, ln, fn, lnfn):
    if tolerance:
        return "Error tolerated."
    if lnfn:
        print(f"[red]Line {ln}, char {fn}\nAfunge Error: {e}[/red]")
    else:
        print(f"Afunge Error: {e}[/red]")
    if debug_tolerance:
        return "Exit tolerated."
    exit()

def init():
    global runfile, mapfile, mapcont, runcont, settings, tolerance, debug_tolerance, inclusive_time, x, y

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
    if "spawnPosition" in settings:
        x = settings["spawnPosition"][0]
        y = settings["spawnPosition"][1]

    with open(mapfile) as file:
        mapcont = file.read()
    with open(runfile) as file:
        runcont = file.read()

def pos():
    global mapcont, x, y
    try:
        row = mapcont.split("\n")[y]
    except IndexError:
        AfungeException(f"Less than y value {y} lines in map file.", cur_ln, cur_char, True)
    try:
        col = row[x]
    except IndexError:
        AfungeException(f"Less than x value {x} chars in current {y} line.", cur_ln, cur_char, True)
    return col

def check():
    if pos() in mapfunc:
        print(f"hey boss we got a map {pos()}")
        mapfunc[pos()]()

def main():
    global time, cur_ln, cur_char
    for ln in runcont.split("\n"):
        cur_ln = runcont.split("\n").index(ln)
        ln = ln.split("=")[0]
        for char in ln:
            cur_char = list(ln).index(char)
            if inclusive_time:
                time += 1
            if char in functions:
                if not inclusive_time:
                    time += 1
                functions[char]()
            if char != "0":
                check()
    input("Press enter to continue... > ")

init()
main()