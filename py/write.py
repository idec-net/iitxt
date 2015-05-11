#!/usr/bin/env python3

import ii, os, sys, time, subprocess, codecs

ii.check_base()
ii.load_config()

args = sys.argv[1:]
argc = len(args)

if argc==0:
    print("Usage: write.py echoarea <msg number>")
    sys.exit(1)

def parseTags(str):
    arr = str.split("/")
    tags = {}
    for i in range(0,len(arr),2):
        if arr[i + 1]:
            tags[arr[i]] = arr[i + 1]
    return tags

def getMsg(msgid):
    try:
        msg = codecs.open("../base/msg/" + msgid, "r", "utf-8").read().splitlines()
        tags = parseTags(msg[0])
        if 'repto' in tags:
            rpt = tags['repto']
        else:
            rpt = False
        message = "\n".join(msg[8:])
        meta = dict(repto=rpt, echo=msg[1], time=msg[2], sender=msg[3], addr=msg[4], to=msg[5], subj=msg[6], msg=message, id=msgid)
    except:
        meta = dict(repto=False, echo="", time=0, sender="", addr="", to="", subj="", msg="no message", id=msgid)
    return meta

def openEditor(file):
    p = subprocess.Popen(ii.editor + " " + file, shell=True)
    p.wait()

def edit(echo, msgfile, text):
    if not os.path.exists("../mail/" + echo):
        os.makedirs("../mail/" + echo)
    
    fname = "../mail/" + echo + "/" + msgfile + ".new"
    if not os.path.exists(fname):
        codecs.open(fname, "w", "utf-8").write(text)
    openEditor(fname)

def writeNew(echo):
    filename = str(time.time())
    template = "All\n...\n\n"
    edit(echo, filename, template)

def frmSubj(str):
    if str.startswith("Re: "):
        return str
    else:
        return "Re: " + str

def answer(echo, msgfile):
    msgid = codecs.open("../mail/" + echo + "/" + msgfile, "r", "utf-8").read().splitlines()[0]
    msg = getMsg(msgid)
    subj = msg.get("subj")
    to = msg.get("sender")
    template = msgid + "\n" + to + "\n" + frmSubj(subj) + "\n\n"
    edit(echo, msgfile, template)

if argc==1:
    writeNew(args[0])
elif argc==2:
    msglist = ii.get_local_mail_list(args[0])
    answer(args[0], msglist[int(args[1])])
