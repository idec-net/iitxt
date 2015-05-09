import os

node = ""
auth = ""
editor = "nano"
echoes = []
rebuild = "1"

def get_echo_list():
    echo = []
    r = urllib.request.Request(node + "list.txt")
    with urllib.request.urlopen(r) as f:
        lines = f.read().decode("utf-8").split("\n")
        for line in lines:
            echo.append(line.split(":")[0])
    return echo

def get_local_mail_list(echo):
	if not os.path.exists("../mail/" + echo):
		return []
	else:
		msglist = [msg for msg in os.listdir("../mail/" + echo) if (msg.endswith(".txt") and msg!="0000.txt")]
		return sorted(msglist)

def load_config():
    global node, auth, echoes, rebuild, editor
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
                if param[0] == "rebuild":
                    rebuild = param[1]
                if param[0] == "editor":
                    editor = param[1]

def check_base():
    if not os.path.exists("../base"):
        os.makedirs("../base")
    if not os.path.exists("../mail"):
        os.makedirs("../mail")
    if not os.path.exists("../base/msg"):
        os.makedirs("../base/msg")
    if not os.path.exists("../base/echo"):
        os.makedirs("../base/echo")
    if not os.path.exists("../base/out"):
        os.makedirs("../base/out")

def separate(l, step=20):
    for x in range(0, len(l), step):
        yield l[x:x+step]
