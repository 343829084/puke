# -*- coding: utf-8 -*-
import ffext
import msg_def.ttypes as msg_def
  
import time


class player_mgr_t:
    def __init__(self):
        self.all_players = {}
    def get(self, session_id_):
        return self.all_players.get(session_id_)
    def get_by_name(self, name_):
        for id, player in self.all_players.iteritems():
            if player.nick_name == name_:
                return player
        return None
    def foreach(self, func_):
        for id, player in self.all_players.iteritems():
            func_(player)
    def foreach_except(self, func_, except_id_ = None):
        for id, player in self.all_players.iteritems():
            if id != except_id_:
                func_(player)
    def remove(self, session_id_):
        if None != self.all_players.get(session_id_):
            del  self.all_players[session_id_]
    def add(self, session_id_, player):
        self.all_players[session_id_] = player
    def size(self):
        return len(self.all_players)
    def idlist(self):
        return self.all_players.keys()
    def get_status_by_id(self, id_):
        player = self.get(id_)
        if player == None:
            return 4 #不在线
        return player.get_status()

def is_tody(tm_):
    now = datetime.datetime.now()
    return now.year == tm_.year and now.month == tm_.month and now.hour == tm_.hour

def is_this_week(tm_):
    now = datetime.datetime.now()
    return now.year == tm_.year and now.month == tm_.month and now.hour == tm_.hour

def is_this_month(tm_):
    now = datetime.datetime.now()
    return now.year == tm_.year and now.month == tm_.month and now.hour == tm_.hour


class player_t:
    def __init__(self, session_id_ = 0):
        self.tmp_socket_id = 0#临时socket
        self.register_flag = 0
        self.session_id = session_id_;
        self.real_name  = ''
        self.nick_name  = ''
        self.level      = 1
        self.exp        = 0
        
        self.room = None
        
    def name(self):
        return self.nick_name
    def trace(self, content_):
        ffext.TRACE('%s %s'%(self.nick_name, content_))
   
    def set_socket_id(self, id_):
        self.tmp_socket_id = id_
    def get_socket_id(self):
        if self.tmp_socket_id != 0:
            return self.tmp_socket_id
        return self.id()
    def id(self):
        return self.session_id
    def get_status(self):
        return 1 #1表示在线
    def set_id(self, id_):
        self.session_id = id_
    def get_extra_data(self):
        return ''
    def send(self, cmd_, msg_):
        return ffext.send_msg_session(self.get_socket_id(),cmd_, msg_)
    def send_error(self, error_code_, error_msg_ = ''):
        msg = msg_def.error_code_ret_t()
        msg.error_code = error_code_
        msg.error_msg = error_msg_
        return ffext.send_msg_session(self.get_socket_id(), msg_def.server_cmd_e.ERROR_CODE_RET, msg)
    def sys_msg(self, msg_):
        ret_msg = msg_def.chat_msg_ret_t()
        ret_msg.channel = 2
        ret_msg.from_player_uid = self.id()
        ret_msg.from_player_name = ''#self.nick_name    
        ret_msg.msg = msg_
        self.send(msg_def.server_cmd_e.CHAT_RET, ret_msg)

def session_id_to_player(session_id):
    return ffext.singleton(player_mgr_t).get(session_id)
#方便注册用
def reg(cmd_, protocol_type_):
    return ffext.session_call(cmd_, protocol_type_, session_id_to_player)


#gm注册
class gm_reg_t:
    def __init__(self):
        self.gm_reg = {}


GID = 0

def gen_id():
    GID += 1
    return GID