import os

node = ""
auth = ""
echoes = []

def get_echo_list():
    echo = []
    r = urllib.request.Request(node + "list.txt")
    with urllib.request.urlopen(r) as f:
        lines = f.read().decode("utf-8").split("\n")
        for line in lines:
            echo.append(line.split(":")[0])
    return echo

def load_config():
    global node, auth, echoes
    f = open ("../config.cfg", "r")
    lines = f.read().split("\n")
    f.close()
    for line in lines:
        if len(line) > 0 and not line[0] == "#":
            param = line.split(" ")
            if len(param) == 2:
                if param[0] == "node":
                    node = param[1]
                if param[0] == "auth":
                    auth = param[1]
                if param[0] == "echo":
                    echoes.append(param[1])

def check_base():
    if not os.path.exists("../.msg"):
        os.makedirs("../.msg")
    if not os.path.exists("../.echo"):
        os.makedirs("../.echo")
    if not os.path.exists("../.out"):
        os.makedirs("../.out")

def separate(l, step=20):
    for x in range(0, len(l), step):
        yield l[x:x+step]
