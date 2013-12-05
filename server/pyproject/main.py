# -*- coding: utf-8 -*-
import os
import time
import ffext
import event_bus

import  msg_def.ttypes  as msg_def
from   player import player_handler

def GetNowTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

print("loading.......")

def init():
    msg = msg_def.chat_req_t()
    msg.content = 'OhNice'
    s = ffext.to_str(msg)
    print(s)
    
    dest = msg_def.chat_req_t()
    ffext.decode_buff(dest, s)
    print(dest.content)
    
    return 0
    
def cleanup():
    return 0
