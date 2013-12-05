
package org.apache.thrift.transport {

  import flash.errors.EOFError;
  import flash.events.Event;
  import flash.events.IOErrorEvent;
  import flash.events.SecurityErrorEvent;
  import flash.net.URLLoader;
  import flash.net.URLLoaderDataFormat;
  import flash.net.URLRequest;
  import flash.net.URLRequestMethod;
  import flash.system.Capabilities;
  import flash.utils.ByteArray;

  public class FFMemoryTransport extends TTransport {

    private var byteBuffer_:ByteArray = null;
    
    public function getBuffer():ByteArray {
      return byteBuffer_;
    }
    
    public function FFMemoryTransport(responseBufferArg_:ByteArray):void {
		byteBuffer_ = responseBufferArg_;
    }
    
    public override function open():void {
    }

    public override function close():void {
    }
 
    public override function isOpen():Boolean {
      return true;
    }
    
    public override function read(buf:ByteArray, off:int, len:int):int {
		try {
	        byteBuffer_.readBytes(buf, off, len);
		}
		catch (e:EOFError) {
            trace("No more data available.");
			return 0;
        }
		return len;
    }

    public override function write(buf:ByteArray, off:int, len:int):void {
      byteBuffer_.writeBytes(buf, off, len);
    }

    public override function flush(callback:Function=null):void {
    }
  }
}
