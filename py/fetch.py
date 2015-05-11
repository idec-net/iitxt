import urllib.request, base64, codecs, os, time
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
        local_msg_list = codecs.open("../base/echo/" + echo, "r", "utf-8").read().split("\n")
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
                codecs.open("../base/msg/" + msgid, "w", "utf-8").write(base64.b64decode(m[1]).decode("utf-8"))
                codecs.open("../base/echo/" + echo, "a", "utf-8").write(msgid + "\n")
                codecs.open("../.newmsg", "a", "utf-8").write(msgid + "\n")

def fetch_mail():
    for echo in ii.echoes:
        remote_msg_list = get_msg_list(echo)
        if len(remote_msg_list) > 1:
            local_msg_list = get_local_msg_list(echo)
            msg_list = [x for x in remote_msg_list if x not in local_msg_list]
            for get_list in ii.separate(msg_list):
                debundle(echo, get_bundle("/".join(get_list)))
        else:
            codecs.open("../base/echo/" + echo, "a", "utf-8").close()

def mail_rebuild():
    for echo in ii.echoes:
        if not os.path.exists("../mail/" + echo):
            os.makedirs("../mail/" + echo)
        msgs = codecs.open("../base/echo/" + echo, "r", "utf-8").read().split("\n")
        f = codecs.open("../mail/" + echo + "/0000.txt", "w", "utf-8")
        for i, m in enumerate(msgs, 1):
            if m:
                n = str(i).zfill(4)
                msg = codecs.open("../base/msg/" + m, "r", "utf-8").read().split("\n")
                buf = m + "\nОт:   " + msg[3] + " [" + msg[4] + "] " + time.strftime("%Y.%m.%d %H:%M", time.gmtime(int(msg[2]))) + " GMT\nКому: " + msg[5] + "\nТема: " + msg[6] + "\n\n" + "\n".join(msg[8:])
                codecs.open("../mail/" + echo +"/" + n + ".txt", "w", "utf-8").write(buf)
                f.write("== " + n + " ==================== " + buf + "\n\n\n")
        f.close()

def mail_add():
    if os.path.exists("../.newmsg"):
        msgs = codecs.open("../.newmsg", "r", "utf-8").read().split("\n")
        for msgn in msgs:
            if msgn:
                msg = codecs.open("../base/msg/%s" % msgn, "r", "utf-8").read().split("\n")
                echo = msg[1]
                if not os.path.exists("../mail/" + echo):
                    os.makedirs("../mail/" + echo)
                f = codecs.open("../mail/" + echo + "/0000.txt", "a", "utf-8")
                n = os.listdir("../mail/%s" % echo)
                n.sort()
                n = str(int(n.pop().replace(".txt", "")) + 1).zfill(4) + ".txt"
                buf = msgn + "\nОт:   " + msg[3] + " [" + msg[4] + "] " + time.strftime("%Y.%m.%d %H:%M", time.gmtime(int(msg[2]))) + " GMT\nКому: " + msg[5] + "\nТема: " + msg[6] + "\n\n" + "\n".join(msg[8:])
                codecs.open("../mail/%s/%s" % (echo, n), "w", "utf-8").write(buf)
                f.write("== " + n + " ==================== " + buf + "\n\n\n")
                f.close()

def newmsg():
    if os.path.exists("../newmsg.txt"):
        os.remove("../newmsg.txt")
    if os.path.exists("../.newmsg"):
        msgs = codecs.open("../.newmsg", "r", "utf-8").read().split("\n")
        f = codecs.open("../newmsg.txt", "w", "utf-8")
        for m in msgs:
            if m:
                msg = codecs.open("../base/msg/" + m, "r", "utf-8").read().split("\n")
                buf = m + "\nОт:   " + msg[3] + " [" + msg[4] + "] " + time.strftime("%Y.%m.%d %H:%M", time.gmtime(int(msg[2]))) + " GMT\nКому: " + msg[5] + "\nТема: " + msg[6] + "\n\n" + "\n".join(msg[8:])
                f.write("== " + msg[1] + " ==================== " + buf + "\n\n\n")
        f.close()
        os.remove("../.newmsg")
        
ii.check_base()
ii.load_config()

print ("Fetching start.")
fetch_mail()

if ii.rebuild == "0":
    print ("Add new messages to mail directory.")
    mail_add()
else:
    print ("Mail directory rebuild.")
    mail_rebuild()

print ("Generate newmsg.txt.")
newmsg()
