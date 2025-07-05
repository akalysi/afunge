import os, json
from rich import print

settings = None

runfile = mapfile = None
mapcont = runcont = None

debug_tolerance = False
tolerance = False
x = y = 0

def right():
    global x
    x += 1
def left():
    global x
    x -= 1
def up():
    global y
    y += 1
def down():
    global y
    y -= 1
nothing = lambda: 0

def test():
    print("test")

functions = {
    ">": right,
    "<": left,
    "^": up,
    "v": down,
    "x": exit,
    "o": nothing
}

mapfunc = {
    "t": test
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
    global runfile, mapfile, mapcont, runcont, settings, tolerance, debug_tolerance

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
    if "debug" in settings:
        debug_tolerance = settings["debug"]

    with open(mapfile) as file:
        mapcont = file.read()
    with open(runfile) as file:
        runcont = file.read()

def pos(x=x, y=y):
    global mapcont
    row = mapcont.split("\n")[abs(y)]
    col = row[abs(x)]
    print(f"calling from pos. returning {col}. following is the row.\n{row}")
    return col

def check():
    print(f"hey boss, pos is {pos()}, our coords are {x}, {y}. checking {abs(x)}, {abs(y)}")
    if pos() in mapfunc:
        print(f"hey boss, we got a map function, it's {pos()}")
        mapfunc[pos()]()

def main():
    for ln in runcont.split("\n"):
        ln = ln.split("=")[0]
        for char in ln:
            if char in functions:
                print(f"hey boss, we got a main function, it's {char}")
                functions[char]()
            check()
    input("Press enter to continue... > ")

init()
main()