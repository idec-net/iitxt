#!/usr/bin/env python3

import ii, os, sys, codecs

ii.check_base()
args = sys.argv[1:]
argc = len(args)

if argc==0:
    print("Usage: echocat.py echoarea <start:end>\nor echocat.py echoarea len")
    sys.exit(1)

echoarea = args[0]
messages = ii.get_local_mail_list(echoarea)

if argc==2:
    position = args[1]
    if ":" in position:
        pos = position.split(":")
        start = pos[0]
        end = pos[1]
        if not start:
            start = 0
        if not end:
            end = len(messages)
        filtered = messages[slice(int(start), int(end))]

    elif position == "len":
        print(len(messages))
        sys.exit(0)
    else:
        filtered = [messages[int(position)]]
else:
    filtered = messages

for filename in filtered:
    msg = codecs.open("../mail/" + echoarea + "/" + filename, "r", "utf-8").read()
    print(msg + "\n")
