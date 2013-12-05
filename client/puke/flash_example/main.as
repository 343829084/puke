import flash.external.ExternalInterface
import ff.chat_msg_t;
import ff.FFUtil;

//mc_page1.visible = true;
var socket:Socket = new Socket();
var isConn:Boolean = false;
var EnableLogflag:Boolean = true;
var recvByteArray:ByteArray = new ByteArray();

var curCmd:int = 0;
var curBodyLen = 0;
var curMsg:String = "";

function log(content: String):void
{
	if (EnableLogflag)
		mc_page1.incomingChat_txt.htmlText += "<font color='#ff0000' face='宋体' size='12'>" + content + "</font>"; 
}

function onConnectCB(e:Event):void 
{//连接成功
	socket.removeEventListener(Event.CONNECT, onConnectCB);
	socket.removeEventListener(IOErrorEvent.IO_ERROR, onError);
	socket.removeEventListener(SecurityErrorEvent.SECURITY_ERROR, onSecurity);

	socket.addEventListener(Event.CLOSE, onClose);
	socket.addEventListener(ProgressEvent.SOCKET_DATA,onReceiveData);
	isConn = true;
	log("连接server成功！");
	ExternalInterface.call("onConnect", 1);
}

function onError(e:IOErrorEvent):void
{//IO error
	socket.removeEventListener(Event.CONNECT, onConnectCB);
	socket.removeEventListener(IOErrorEvent.IO_ERROR,onError);
	socket.removeEventListener(SecurityErrorEvent.SECURITY_ERROR,onSecurity);
	isConn = false;
	log("IOError");
	ExternalInterface.call("HandleError");
}

function onSecurity(e:SecurityErrorEvent):void 
{//SecurityError
	socket.removeEventListener(SecurityErrorEvent.SECURITY_ERROR,onSecurity);
	socket.removeEventListener(Event.CONNECT,onConnectCB);
	socket.removeEventListener(IOErrorEvent.IO_ERROR,onError);
	socket.close();
	isConn=false;
	log("SecurityError");
	ExternalInterface.call("HandleError");
}

function onClose(e:Event):void {
	socket.removeEventListener(Event.CLOSE,onClose);
	isConn=false;
	ExternalInterface.call("HandleError");
}

function sendBytesData( cmd:int, byteArray:ByteArray):void 
{
	if (isConn) 
	{
		//head
		socket.writeInt(byteArray.length);
		socket.writeShort(cmd);
		socket.writeShort(0);
		//body
		socket.writeBytes(byteArray, 0, byteArray.length); 
		socket.flush();
	}
	else 
	{
		log("sendBytesData已断开连接，请重新连接！");
	}
}

function onReceiveData(e:ProgressEvent):void
{//收到消息
	while (socket.bytesAvailable) 
	{
		//var ba:ByteArray = new ByteArray();
		var curLen:int = recvByteArray.length;
	    socket.readBytes(recvByteArray, recvByteArray.length, socket.bytesAvailable);
	}
	//if (recvByteArray.length < 300)
		//return;
	var left:int = recvByteArray.length - recvByteArray.position;
	while(left > 0)
	{
		if (curBodyLen == 0)//!需要解析包头
		{
			if (recvByteArray.length < 8)
			{
				break;
			}

			curBodyLen = recvByteArray.readInt();
			curCmd     = recvByteArray.readShort();
			var res:int= recvByteArray.readShort();

			//curMsg     = recvByteArray.readUTFBytes(curBodyLen);
			
			//log("curCmd:" + curCmd + " curBodyLen:"+curBodyLen);
		}
		//! 包头已经读取完毕, 读取body
		var needLen = curBodyLen - curMsg.length;
		left = recvByteArray.length - recvByteArray.position;
		//log("curCmd:" + curCmd + " left:"+left + " needLen:" + needLen + " position=" + recvByteArray.position);
		if (left >= needLen)
		{
			if (needLen > 0)
				curMsg += recvByteArray.readUTFBytes(needLen);
			CallJsHandleMsg(curCmd, curMsg, curBodyLen);
			
			curCmd = 0;
			curBodyLen = 0;
			curMsg = "";
			var tmpByteArray:ByteArray = new ByteArray();
			tmpByteArray.writeBytes(recvByteArray, recvByteArray.position, recvByteArray.length - recvByteArray.position); 
			recvByteArray.clear();
			recvByteArray = tmpByteArray;
			recvByteArray.position = 0;
			//log("callHandleMsg:" + curCmd + " recvByteArray.length:"+recvByteArray.length);
		}
		else if (left > 0)
		{
			curMsg += recvByteArray.readUTFBytes(left);
			recvByteArray.clear();
		}
	}
}

//! 提供给js的接口

function Connect(host: String, port: int):void
{
	Security.loadPolicyFile("xmlsocket://"+ host + ":" + port);
	
	socket.addEventListener(Event.CONNECT,onConnectCB);
	socket.addEventListener(IOErrorEvent.IO_ERROR,onError);
	socket.addEventListener(SecurityErrorEvent.SECURITY_ERROR,onSecurity);

	socket.connect(host, port);
	log("开始连接server=" + host + ":" + port);
}

function SendMsg(socketId:int, cmd:int, content:String):void
{
	var thisStringBytes :ByteArray = new ByteArray();
	thisStringBytes.writeMultiByte(content, "utf-8");
	sendBytesData(cmd, thisStringBytes);
	log("SendMsg cmd="+cmd);
}

function Close(socketId:int)
{
	if (isConn){
		socket.close();
		isConn=false;
	}
	log("Close");
}
function CallJsHandleMsg(cmd:int, buff:String, len:int){
	//! js function HandleMsg(socketId, cmd, data, len){
	ExternalInterface.call("HandleMsg", 1, cmd, buff, len);
}
function EnableLog(opt: int)
{
	if (opt != 0)
		EnableLogflag = true;
	else
		EnableLogflag = false;
}

ExternalInterface.addCallback("Connect", Connect);
ExternalInterface.addCallback("SendMsg", SendMsg);
ExternalInterface.addCallback("Close", Close);
ExternalInterface.addCallback("EnableLog", EnableLog);
ExternalInterface.call("FlashReady");
