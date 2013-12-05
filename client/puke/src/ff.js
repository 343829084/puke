
var g_sys_msg = function (head, msg){
}
var g_client_cmd = {}
var g_debug_mode = true;
//注册回调函数
var g_register_callback = {}

var g_debugMode = false;
function EnableDebug(){
    g_debugMode = true;
}
function isDebug(){
    return g_debugMode;
}
function getTypeName(cmd, msg){
    for (var k in g_client_cmd){
        if (g_client_cmd[k] == cmd)
            return k
    }
    return "";
}

function encodeMsg(msg){
    var transport = new Thrift.Transport("/thrift/ff");
    var protocol  = new Thrift.Protocol(transport);
    protocol.writeMessageBegin('ff', 0, 0);
    msg.write(protocol);
    protocol.writeMessageEnd();
    return transport.getSendBuffer();
}

function decdoeMsg(msgType, data){
    var msg = new msgType();
    var transport = new Thrift.Transport("/thrift/ff");
    transport.setRecvBuffer(data);
    var protocol  = new Thrift.Protocol(transport);
    protocol.readMessageBegin('ff', 0, 0);
    msg.read(protocol);
    protocol.readMessageEnd();
    return msg;
}

function Connect(host){
    return 1;
}

function SendMsg(cmd, msg){
    SendContent(cmd, encodeMsg(msg))
}
function SendContent(cmd, content){
    if (g_debug_mode)
        g_sys_msg('发送消息', content)
    flashExt().SendMsg(1, cmd, content);
}
function Close(socket_){
}

function HandleMsg(socketId, cmd, data, len){
    cmd = parseInt(cmd);
    if (true == g_register_callback.hasOwnProperty(cmd)){
        //g_sys_msg('debug', '收到消息cmd:' + " len:" + len +":"+ cmd + ":" + data);
        var funcConfig = g_register_callback[cmd];
        var msgType = funcConfig[0];
        var func    = funcConfig[1];
        var msg     = ''
        try {
            msg = decdoeMsg(msgType, data);
        }catch(err){
            g_sys_msg('debug', '异常:'+err.message );
        }
        //g_sys_msg('debug', '解析ok');
        func(msg);
    }
    else{
        g_sys_msg('error:', cmd + ':no registered');
    }
}

//! 注册回调函数
function RegCallBack(cmd, func){
    g_register_callback[cmd] = func;
}
//! 注册回调函数集合
function MultiRegCallBack(funcDict){
    for (var cmd in funcDict)
        g_register_callback[cmd] = funcDict[cmd];
}


//调用flash中的方法，"my_mv"为html页中swf的id
function flashExt() {
    return thisMovie("flashExt");
}
//搭建js与flash互通的环境
function thisMovie(movieName) {
    if (navigator.appName.indexOf("Microsoft") != -1) {
        return window[movieName]
    }else{
        return document[movieName]
    }
}

function insertSwfInfo(destId, url,w,h){
    var EmbedStr = "";
    EmbedStr = "<object classid='clsid:d27cdb6e-ae6d-11cf-96b8-444553540000' codebase='http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=8,0,0,0' width='" + w + "' height='" + h + "'>";
    EmbedStr += "<param name='allowScriptAccess' value='always' />";
    EmbedStr += "<param name='movie' value='" + url + "' />";
    EmbedStr += "<param name='quality' value='high' />";
    EmbedStr += "<param name='wmode' value='transparent' />";
    EmbedStr += "<param name='menu' value='false' />";
    EmbedStr += "<embed src='" + url + "' id='flashExt' name='flashExt' quality='high' menu='false' wmode='transparent' bgcolor='#ffffff' width='" + w + "' height='" + h + "' allowScriptAccess='always' type='application/x-shockwave-flash' pluginspage='http://www.macromedia.com/go/getflashplayer' />";
    EmbedStr += "</object>";

    $(destId).html(EmbedStr);
    return;
}
