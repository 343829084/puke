# -*- coding: utf-8 -*-
from player_model import *
import ffext
import msg_def.ttypes as msg_def

import time
import sys

import thrift.Thrift as Thrift
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.protocol.TCompactProtocol as TCompactProtocol
import thrift.transport.TTransport as TTransport

@ffext.session_verify_callback
def real_session_verify(session_key, online_time, ip, gate_name):
    '''
    '''
    print(session_key)#name
    nick_name = session_key
    if 'test' == session_key:
        return ['123']
    account = msg_def.account_req_t()
    ffext.decode_buff(account, session_key)

    player = player_t()
    player.online_time = online_time
    player.ip          = ip
    player.gate_name   = gate_name
    player.nick_name = nick_name
    player.register_flag = 0#注册成功
    id = gen_id()
    player.set_socket_id(id)
    player.set_id(id)
    ffext.singleton(player_mgr_t).add(player.get_socket_id(), player)

    return [str(player.id())]

@ffext.session_enter_callback
def real_session_enter(session_id, from_scene, extra_data):
    ffext.TRACE('real_session_enter begin session_id=%d'%(session_id))

    player = ffext.singleton(player_mgr_t).get(session_id)
    #广播所有人，上线了
    def broadcast_msg(player_other):
        pass
    ffext.singleton(player_mgr_t).foreach_except(broadcast_msg, session_id)
    #发送当前房间的所有数据
    return 0

@ffext.session_offline_callback
def real_session_offline(session_id, online_time):
    print('real_session_offline~~~~', session_id)
    player = ffext.singleton(player_mgr_t).get(session_id)
    if player == None:
        return
    
    player = ffext.singleton(player_mgr_t).get(session_id)
    #广播所有人，上线了
    def broadcast_msg(player_other):
        pass
    ffext.singleton(player_mgr_t).foreach_except(broadcast_msg, session_id)

    player.trace('real_session_offline')
    ffext.singleton(player_mgr_t).remove(session_id)#有可能 session_id
    player = None
    print('current online user num=%d'%(ffext.singleton(player_mgr_t).size()))

#聊天接口
#这个修饰器的意思是注册process_chat函数接收cmd=1的消息
@reg(msg_def.client_cmd_e.CHAT_REQ, msg_def.chat_req_t)
def process_chat(player, msg):
    print('process_chat~~~~', msg)
   
    ret_msg = msg_def.chat_msg_ret_t()
    ret_msg.channel = msg.channel
    ret_msg.from_player_uid = player.id()
    ret_msg.from_player_name = player.nick_name    
    ret_msg.msg = wrods_filter.filter(msg.msg)

    #发送给自己
    player.send(msg_def.server_cmd_e.CHAT_RET, ret_msg)

def reg_gm(cmd_):
    def wrapper(func_):
        ffext.singleton(gm_reg_t).gm_reg[cmd_] = func_
        return func_
    return wrapper
@reg_gm('@reload')
def reload_script(player, param):
    player.sys_msg('reload_script .')
    if len(param) < 2:
        player.sys_msg('参数')
        return
    ret = ffext.reload(param[1])
    if ret == '':
        player.sys_msg('%s重载ok'%(param[1]))
    else:
        player.sys_msg(ret)
    return
@reg_gm('@reloadall')
def reload_all(player, param):
    dest = [
        ['player.player_handler', 'player.player_model'],
        ['game.room_handler', 'game.room_model'],
    ]
    ret_str = ''
    for tmp_list in dest:
        for k in tmp_list:
            print(k)
            ret = ffext.reload(k)
            if ret == '':
                ret_str += k + '\n'
            else:
                player.sys_msg(ret)
                return
    player.sys_msg(ret_str+'重载ok')

