# -*- coding: utf-8 -*-
import json
import ff
import sys
import datetime
import time

import thrift.Thrift as Thrift
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.protocol.TCompactProtocol as TCompactProtocol
import thrift.protocol.TJSONProtocol as TJSONProtocol
import thrift.transport.TTransport as TTransport

g_session_verify_callback  = None
g_session_enter_callback   = None
g_session_offline_callback = None
g_session_logic_callback_dict = {}#cmd -> func callback
g_timer_callback_dict = {}

def session_verify_callback(func_):
    global g_session_verify_callback
    g_session_verify_callback = func_
    return func_
def session_enter_callback(func_):
    global g_session_enter_callback
    g_session_enter_callback = func_
    return func_
def session_offline_callback(func_):
    global g_session_offline_callback
    g_session_offline_callback = func_
    return func_
GID = 0
def once_timer(timeout_, func_):
    global g_timer_callback_dict, GID
    GID += 1
    if GID > 100000000:
        GID = 1
    g_timer_callback_dict[GID] = func_
    ff.ffscene_obj.once_timer(timeout_, GID);


def json_to_value(val_):
    return json.loads(val_)

def protobuf_to_value(msg_type_, val_):
    dest = msg_type_()
    dest.ParseFromString(val_)
    return dest

g_protocol = 1 #1 json

g_ReadTMemoryBuffer   = TTransport.TMemoryBuffer()
g_ReadTBinaryProtocol = TBinaryProtocol.TBinaryProtocol(g_ReadTMemoryBuffer)

def decode_buff(dest, val_):
    global g_ReadTMemoryBuffer, g_ReadTBinaryProtocol
    g_ReadTMemoryBuffer.cstringio_buf.truncate()
    g_ReadTMemoryBuffer.cstringio_buf.seek(0)
    g_ReadTMemoryBuffer.cstringio_buf.write(val_)
    g_ReadTMemoryBuffer.cstringio_buf.seek(0)
    if g_protocol == 1:
        proto = TJSONProtocol.TJSONProtocol(g_ReadTMemoryBuffer)
        proto.readMessageBegin();
        dest.read(proto)
        proto.readMessageEnd();
    else:
        dest.read(g_ReadTBinaryProtocol)
    return dest

def ignore_id(id_):
    return id_
def session_call(cmd_, protocol_type_ = 'json', convert_func_ = ignore_id):
    global g_session_logic_callback_dict
    def session_logic_callback(func_):
        if protocol_type_ == 'json':
            g_session_logic_callback_dict[cmd_] = (json_to_value, func_, convert_func_)
        elif hasattr(protocol_type_, 'thrift_spec'):
            def thrift_to_value(val_):
                dest = protocol_type_()
                global g_ReadTMemoryBuffer, g_ReadTBinaryProtocol
                g_ReadTMemoryBuffer.cstringio_buf.truncate()
                g_ReadTMemoryBuffer.cstringio_buf.seek(0)
                g_ReadTMemoryBuffer.cstringio_buf.write(val_)
                g_ReadTMemoryBuffer.cstringio_buf.seek(0)
                dest.read(g_ReadTBinaryProtocol);
                #mb2 = TTransport.TMemoryBuffer(val_)
                #bp2 = TBinaryProtocol.TBinaryProtocol(mb2)
                #dest.read(bp2);
                return dest
            g_session_logic_callback_dict[cmd_] = (thrift_to_value, func_, convert_func_)
        else: #protobuf
            def protobuf_to_value(val_):
                dest = protocol_type_()
                dest.ParseFromString(val_)
                return dest
            g_session_logic_callback_dict[cmd_] = (protobuf_to_value, func_, convert_func_)
        return func_
    return session_logic_callback

def ff_session_verify(session_key, online_time, ip, gate_name):
    '''
    session_key 为client发过来的验证key，可能包括账号密码
    online_time 为上线时间
    gate_name 为从哪个gate登陆的
    '''
    ret= [session_key]
    if g_session_verify_callback != None:
       ret = g_session_verify_callback(session_key, online_time, ip, gate_name) 
    return ret

def ff_session_enter(session_id, from_scene, extra_data):
    '''
    session_id 为client id
    from_scene 为从哪个scene过来的，若为空，则表示第一次进入
    extra_data 从from_scene附带过来的数据
    '''
    if g_session_enter_callback != None:
       return g_session_enter_callback(session_id, from_scene, extra_data)

def ff_session_offline(session_id, online_time):
    '''
    session_id 为client id
    online_time 为上线时间
    '''
    if g_session_offline_callback != None:
       return g_session_offline_callback(session_id, online_time)

def ff_session_logic(session_id, cmd, body):
    '''
    session_id 为client id
    body 为请求的消息
    '''
    #print('ff_session_logic', session_id, cmd, body)
    info = g_session_logic_callback_dict[cmd]
    arg  = info[0](body)
    convert_func = info[2]
    return info[1](convert_func(session_id), arg)

def ff_timer_callback(id):
    try:
        cb = g_timer_callback_dict[id]
        del g_timer_callback_dict[id]
        cb()
    except:
        return False

g_WriteTMemoryBuffer   = TTransport.TMemoryBuffer()
g_WriteTBinaryProtocol = TBinaryProtocol.TBinaryProtocol(g_WriteTMemoryBuffer)

def to_str(msg):
    if hasattr(msg, 'thrift_spec'):
        global g_WriteTMemoryBuffer, g_WriteTBinaryProtocol
        g_WriteTMemoryBuffer.cstringio_buf.truncate()
        g_WriteTMemoryBuffer.cstringio_buf.seek(0)
        if g_protocol == 1:
            proto = TJSONProtocol.TJSONProtocol(g_WriteTMemoryBuffer)
            proto.writeMessageBegin('ff', 0, 0);
            msg.write(proto)
            proto.writeMessageEnd();
        else:
            msg.write(g_WriteTBinaryProtocol)
        return g_WriteTMemoryBuffer.getvalue()
        #mb = TTransport.TMemoryBuffer()
        #bp = TBinaryProtocol.TBinaryProtocol(mb)
        #bp = TCompactProtocol.TCompactProtocol(mb)
        #msg.write(bp)
        #return mb.getvalue()
    elif hasattr(msg, 'SerializeToString'):
        return msg.SerializeToString()
    elif isinstance(msg, unicode):
        return msg.encode('utf-8')
    elif isinstance(msg, str):
        return msg
    elif msg.__class__ == int or msg.__class__ == long or msg.__class__ == float:
        return str(msg)
    else:
        return json.dumps(msg, ensure_ascii=False)

def send_msg_session(session_id, cmd_, body):
    return ff.py_send_msg_session(session_id, cmd_, to_str(body))
    ff.ffscene_obj.send_msg_session(session_id, cmd_, to_str(body))
def multi_send_msg_session(session_id_list, cmd_, body):
    return ff.ffscene_obj.multicast_msg_session(session_id_list, cmd_, to_str(body))
def broadcast_msg_session(cmd_, body):
    return ff.py_broadcast_msg_session(cmd_, to_str(body))
    return ff.ffscene_obj.broadcast_msg_session(cmd_, to_str(body))
def broadcast_msg_gate(gate_name_, cmd_, body):
    return ff.ffscene_obj.broadcast_msg_gate(gate_name_, cmd_, body)
def close_session(session_id):
    return ff.ffscene_obj.close_session(session_id)

def reload(name_):
    if name_ != 'ff':
        return ff.ffscene_obj.reload(name_)

singleton_register_dict = {}
def singleton(type_):
    try:
	    return type_._singleton
    except:
        global singleton_register_dict
        name = type_.__name__
        obj  = singleton_register_dict.get(name)
        if obj == None:
            obj  = type_()
            singleton_register_dict[name] = obj
        type_._singleton = obj
        return obj


#数据库连接相关接口
DB_CALLBACK_ID = 0
DB_CALLBACK_DICT = {}
class ffdb_t(object):
    def __init__(self, host, id):
        self.host   = host
        self.db_id  = id
    def host(self):
        return self.host
    def query(self, sql_, callback_ = None):
        global DB_CALLBACK_DICT, DB_CALLBACK_ID
        DB_CALLBACK_ID += 1
        DB_CALLBACK_DICT[DB_CALLBACK_ID] = callback_
        ff.ffscene_obj.db_query(self.db_id, sql_, DB_CALLBACK_ID)
    def sync_query(self, sql_):
        ret = ff.ffscene_obj.sync_db_query(self.db_id, sql_)
        if len(ret) == 0:
            return query_result_t(False, [], [])
        col = ret[len(ret) - 1]
        data = []
        for k in range(0, len(ret)-1):
            data.append(ret[k])
        return query_result_t(True, data, col)
#封装query返回的结果
class query_result_t(object):
    def __init__(self, flag_, result_, col_):
        self.flag    = flag_
        self.result  = result_
        self.column  = col_
    def dump(self):
        print(self.flag, self.result, self.column)

#C++ 异步执行完毕db操作回调
def ff_db_query_callback(callback_id_, flag_, result_, col_):
    global DB_CALLBACK_DICT
    cb = DB_CALLBACK_DICT.get(callback_id_)
    del DB_CALLBACK_DICT[callback_id_]
    #print('db_query_callback', callback_id_, flag_, result_, col_)
    if cb != None:
        ret = query_result_t(flag_, result_, col_)
        cb(ret)

# 封装异步操作数据库类
def ffdb_create(host_):
    db_id = ff.ffscene_obj.connect_db(host_)
    if db_id == 0:
        return None
    return ffdb_t(host_, db_id)


#封装escape操作
def escape(s_):
    return ff.escape(s_)

g_call_service_wait_return_dict = {}
g_call_service_id   = 1
#各个scene之间的互相调用
def call_service(name_, cmd_, msg_, callback_ = None):
    id = 0
    if callback_ != None:
        global g_call_service_id, g_call_service_wait_return_dict
        id = g_call_service_id
        g_call_service_id += 1
        g_call_service_wait_return_dict[id] = callback_
    ff.ffscene_obj.call_service(name_, cmd_, to_str(msg_), id)
def bridge_call_service(group_name_, name_, cmd_, msg_, callback_ = None):
    id = 0
    if callback_ != None:
        global g_call_service_id, g_call_service_wait_return_dict
        id = g_call_service_id
        g_call_service_id += 1
        g_call_service_wait_return_dict[id] = callback_
    ff.ffscene_obj.bridge_call_service(group_name_, name_, cmd_, to_str(msg_), id)


g_py_service_func_dict = {}
# c++ 调用的
def ff_scene_call(cmd_, msg_):
    func = g_py_service_func_dict.get(cmd_)
    ret = func(msg_)
    if ret != None:
        if hasattr(ret, 'SerializeToString2'):
            return [ret.__name__, ret.SerializeToString()]
        elif isinstance(ret, unicode):
            return ['json', ret.encode('utf-8')]
        elif isinstance(ret, str):
            return ['json', ret]
        else:
            return ['json', json.dumps(ret, ensure_ascii=False)]
    return ['', '']

# c++ 调用的
def ff_scene_call_return_msg(id_, err_, msg_type_, msg_):
    func = g_call_service_wait_return_dict.get(id_)
    if func != None:
        del g_call_service_wait_return_dict[id_]
        if err_ == '':
            err_ = None
        else:
            func(err_, None)
            return
        if msg_type_ == 'json':
            func(err_, json_to_value(msg_))
        else:# protobuff
            dest_type = eval(msg_type_)
            func(err_, protobuf_to_value(dest_type, msg_))



# 注册接口
def reg_service(cmd_, msg_type_ = None):
    def bind_func(func_):
        def impl_func(msg_):
            if None == msg_type_:
                return func_(json_to_value(msg_))
            else: #protobuf
                return func_(protobuf_to_value(msg_type_, msg_))

        global g_py_service_func_dict
        g_py_service_func_dict[cmd_] = impl_func
        return func_
    return bind_func

#将python的标准输出导出到日志
save_stdout = None
class mystdout_t(object):
    def write(self, x):
        if x == '\n':
            return 1
        ff.ffscene_obj.pylog(6, 'FFSCENE_PYTHON', x)
        return len(x)
def dump_stdout_to_log():
    save_stdout = sys.stdout
    sys.stdout = mystdout_t()

#分配id
G_ALLOC_ID = 0
def alloc_id():
    global G_ALLOC_ID
    G_ALLOC_ID += 1
    return G_ALLOC_ID


#日志相关的接口
def LOGTRACE(mod_, content_):
    return ff.ffscene_obj.pylog(6, mod_, content_)
def LOGDEBUG(mod_, content_):
    return ff.ffscene_obj.pylog(5, mod_, content_)
def LOGINFO(mod_, content_):
    return ff.ffscene_obj.pylog(4, mod_, content_)
def LOGWARN(mod_, content_):
    return ff.ffscene_obj.pylog(3, mod_, content_)
def LOGERROR(mod_, content_):
    return ff.ffscene_obj.pylog(2, mod_, content_)
def LOGFATAL(mod_, content_):
    return ff.ffscene_obj.pylog(1, mod_, content_)

def ERROR(content_):
    return LOGERROR('PY', content_)

def TRACE(content_):
    return LOGTRACE('PY', content_)
def INFO(content_):
    return LOGINFO('PY', content_)
def WARN(content_):
    return LOGWARN('PY', content_)

#时间相关的操作
def get_time():
    return time.time()

def datetime_now():
    return datetime.datetime.now()#fromtimestamp(time.time())

def datetime_from_time(tm_):
    datetime.datetime.fromtimestamp(tm_)

def datetime_from_str(s_):
    return datetime.datetime.strptime(s_, '%Y-%m-%d %H:%M:%S')

def datetime_to_str(dt_):
    return dt_.strftime('%Y-%m-%d %H:%M:%S')

def get_config(key_):
    return ff.py_get_config(key_)
