import urllib.request, base64, os, time
import ii

def get_msg_list(echo):
    msg_list = []
    r = urllib.request.Request(ii.node + "u/e/" + echo)
    with urllib.request.urlopen(r) as f:
        lines = f.read().decode("utf-8").split("\n")
        for line in lines:
            if line != echo:
                msg_list.append(line)
    return msg_list

def get_local_msg_list(echo):
    if not os.path.exists("../base/echo/" + echo):
        return []
    else:
        f = open("../base/echo/" + echo, "r")
        local_msg_list = f.read().split("\n")
        f.close()
        return local_msg_list

def get_bundle(msgids):
    print ("Fetch %su/m/%s\n" % (ii.node, msgids))
    bundle = []
    r = urllib.request.Request(ii.node + "u/m/" + msgids)
    with urllib.request.urlopen(r) as f:
        bundle = f.read().decode("utf-8").split("\n")
    return bundle

def debundle(echo, bundle):
    for msg in bundle:
        if msg:
            m = msg.split(":")
            msgid = m[0]
            if len(msgid) == 20 and m[1]:
                open("../base/msg/" + msgid, "w").write(base64.b64decode(m[1]).decode("utf-8"))
                open("../base/echo/" + echo, "a").write(msgid + "\n")
                open("../.newmsg", "a").write(msgid + "\n")

def fetch_mail():
    for echo in ii.echoes:
        remote_msg_list = get_msg_list(echo)
        local_msg_list = get_local_msg_list(echo)
        msg_list = [x for x in remote_msg_list if x not in local_msg_list]
        for get_list in ii.separate(msg_list):
            debundle(echo, get_bundle("/".join(get_list)))

def mail_rebuild():
    for echo in ii.echoes:
        if not os.path.exists("../mail/" + echo):
            os.makedirs("../mail/" + echo)
        msgs = open("../base/echo/" + echo, "r").read().split("\n")
        f = open("../mail/" + echo + "/0000.txt", "w")
        for i, m in enumerate(msgs, 1):
            if m:
                n = str(i).zfill(4)
                msg = open("../base/msg/" + m, "r").read().split("\n")
                buf = m + "\nОт:   " + msg[3] + " [" + msg[4] + "] " + time.strftime("%Y.%m.%d %H:%M", time.gmtime(int(msg[2]))) + " GMT\nКому: " + msg[5] + "\nТема: " + msg[6] + "\n\n" + "\n".join(msg[8:])
                open("../mail/" + echo +"/" + n + ".txt", "w").write(buf)
                f.write("== " + n + " ==================== " + buf + "\n\n\n")
        f.close()

def newmsg():
    if os.path.exists("../newmsg.txt"):
        os.remove("../newmsg.txt")
    if os.path.exists("../.newmsg"):
        msgs = open("../.newmsg").read().split("\n")
        f = open("../newmsg.txt", "w")
        for m in msgs:
            if m:
                msg = open("../base/msg/" + m, "r").read().split("\n")
                buf = m + "\nОт:   " + msg[3] + " [" + msg[4] + "] " + time.strftime("%Y.%m.%d %H:%M", time.gmtime(int(msg[2]))) + " GMT\nКому: " + msg[5] + "\nТема: " + msg[6] + "\n\n" + "\n".join(msg[8:])
                f.write("== " + msg[1] + " ==================== " + buf + "\n\n\n")
        f.close()
        os.remove("../.newmsg")
        
ii.check_base()
ii.load_config()
print ("Fetching start.")
fetch_mail()
print ("Generate newmsg.txt.")
newmsg()
print ("Mail directory rebuild.")
mail_rebuild()
