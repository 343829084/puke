#
# Autogenerated by Thrift Compiler (0.9.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class client_cmd_e:
  CHUPAI_REQ = 1
  CHAT_REQ = 2
  READY_REQ = 3
  PASS_REQ = 4
  QUIT_REQ = 5

  _VALUES_TO_NAMES = {
    1: "CHUPAI_REQ",
    2: "CHAT_REQ",
    3: "READY_REQ",
    4: "PASS_REQ",
    5: "QUIT_REQ",
  }

  _NAMES_TO_VALUES = {
    "CHUPAI_REQ": 1,
    "CHAT_REQ": 2,
    "READY_REQ": 3,
    "PASS_REQ": 4,
    "QUIT_REQ": 5,
  }

class server_cmd_e:
  CHUPAI_RET = 1
  CHAT_RET = 2
  READY_RET = 3
  PASS_RET = 4
  QUIT_RET = 5
  ROOM_RET = 6

  _VALUES_TO_NAMES = {
    1: "CHUPAI_RET",
    2: "CHAT_RET",
    3: "READY_RET",
    4: "PASS_RET",
    5: "QUIT_RET",
    6: "ROOM_RET",
  }

  _NAMES_TO_VALUES = {
    "CHUPAI_RET": 1,
    "CHAT_RET": 2,
    "READY_RET": 3,
    "PASS_RET": 4,
    "QUIT_RET": 5,
    "ROOM_RET": 6,
  }


class table_info_ret_t:
  """
  Attributes:
   - all_names
  """

  thrift_spec = (
    None, # 0
    (1, TType.LIST, 'all_names', (TType.STRING,None), None, ), # 1
  )

  def __init__(self, all_names=None,):
    self.all_names = all_names

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.LIST:
          self.all_names = []
          (_etype3, _size0) = iprot.readListBegin()
          for _i4 in xrange(_size0):
            _elem5 = iprot.readString();
            self.all_names.append(_elem5)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('table_info_ret_t')
    if self.all_names is not None:
      oprot.writeFieldBegin('all_names', TType.LIST, 1)
      oprot.writeListBegin(TType.STRING, len(self.all_names))
      for iter6 in self.all_names:
        oprot.writeString(iter6)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class room_info_ret_t:
  """
  Attributes:
   - all_tables
   - nCurRoomIndex
   - nCurTableIndex
  """

  thrift_spec = (
    None, # 0
    (1, TType.LIST, 'all_tables', (TType.STRUCT,(table_info_ret_t, table_info_ret_t.thrift_spec)), None, ), # 1
    (2, TType.I32, 'nCurRoomIndex', None, -1, ), # 2
    (3, TType.I32, 'nCurTableIndex', None, -1, ), # 3
  )

  def __init__(self, all_tables=None, nCurRoomIndex=thrift_spec[2][4], nCurTableIndex=thrift_spec[3][4],):
    self.all_tables = all_tables
    self.nCurRoomIndex = nCurRoomIndex
    self.nCurTableIndex = nCurTableIndex

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.LIST:
          self.all_tables = []
          (_etype10, _size7) = iprot.readListBegin()
          for _i11 in xrange(_size7):
            _elem12 = table_info_ret_t()
            _elem12.read(iprot)
            self.all_tables.append(_elem12)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.nCurRoomIndex = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I32:
          self.nCurTableIndex = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('room_info_ret_t')
    if self.all_tables is not None:
      oprot.writeFieldBegin('all_tables', TType.LIST, 1)
      oprot.writeListBegin(TType.STRUCT, len(self.all_tables))
      for iter13 in self.all_tables:
        iter13.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.nCurRoomIndex is not None:
      oprot.writeFieldBegin('nCurRoomIndex', TType.I32, 2)
      oprot.writeI32(self.nCurRoomIndex)
      oprot.writeFieldEnd()
    if self.nCurTableIndex is not None:
      oprot.writeFieldBegin('nCurTableIndex', TType.I32, 3)
      oprot.writeI32(self.nCurTableIndex)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class alloc_puke_ret_t:
  """
  Attributes:
   - nAllocIndex
   - listPuke
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'nAllocIndex', None, 0, ), # 1
    (2, TType.LIST, 'listPuke', (TType.I32,None), None, ), # 2
  )

  def __init__(self, nAllocIndex=thrift_spec[1][4], listPuke=None,):
    self.nAllocIndex = nAllocIndex
    self.listPuke = listPuke

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.nAllocIndex = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.LIST:
          self.listPuke = []
          (_etype17, _size14) = iprot.readListBegin()
          for _i18 in xrange(_size14):
            _elem19 = iprot.readI32();
            self.listPuke.append(_elem19)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('alloc_puke_ret_t')
    if self.nAllocIndex is not None:
      oprot.writeFieldBegin('nAllocIndex', TType.I32, 1)
      oprot.writeI32(self.nAllocIndex)
      oprot.writeFieldEnd()
    if self.listPuke is not None:
      oprot.writeFieldBegin('listPuke', TType.LIST, 2)
      oprot.writeListBegin(TType.I32, len(self.listPuke))
      for iter20 in self.listPuke:
        oprot.writeI32(iter20)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class chat_req_t:
  """
  Attributes:
   - content
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'content', None, None, ), # 1
  )

  def __init__(self, content=None,):
    self.content = content

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.content = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('chat_req_t')
    if self.content is not None:
      oprot.writeFieldBegin('content', TType.STRING, 1)
      oprot.writeString(self.content)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class chat_ret_t:
  """
  Attributes:
   - content
   - name
   - flag
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'content', None, None, ), # 1
    (2, TType.STRING, 'name', None, None, ), # 2
    (3, TType.I16, 'flag', None, 0, ), # 3
  )

  def __init__(self, content=None, name=None, flag=thrift_spec[3][4],):
    self.content = content
    self.name = name
    self.flag = flag

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.content = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.name = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I16:
          self.flag = iprot.readI16();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('chat_ret_t')
    if self.content is not None:
      oprot.writeFieldBegin('content', TType.STRING, 1)
      oprot.writeString(self.content)
      oprot.writeFieldEnd()
    if self.name is not None:
      oprot.writeFieldBegin('name', TType.STRING, 2)
      oprot.writeString(self.name)
      oprot.writeFieldEnd()
    if self.flag is not None:
      oprot.writeFieldBegin('flag', TType.I16, 3)
      oprot.writeI16(self.flag)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class show_puke_req_t:
  """
  Attributes:
   - nTableIndex
   - listPuke
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'nTableIndex', None, 0, ), # 1
    (2, TType.LIST, 'listPuke', (TType.I32,None), None, ), # 2
  )

  def __init__(self, nTableIndex=thrift_spec[1][4], listPuke=None,):
    self.nTableIndex = nTableIndex
    self.listPuke = listPuke

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.nTableIndex = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.LIST:
          self.listPuke = []
          (_etype24, _size21) = iprot.readListBegin()
          for _i25 in xrange(_size21):
            _elem26 = iprot.readI32();
            self.listPuke.append(_elem26)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('show_puke_req_t')
    if self.nTableIndex is not None:
      oprot.writeFieldBegin('nTableIndex', TType.I32, 1)
      oprot.writeI32(self.nTableIndex)
      oprot.writeFieldEnd()
    if self.listPuke is not None:
      oprot.writeFieldBegin('listPuke', TType.LIST, 2)
      oprot.writeListBegin(TType.I32, len(self.listPuke))
      for iter27 in self.listPuke:
        oprot.writeI32(iter27)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class show_puke_ret_t:
  """
  Attributes:
   - nTableIndex
   - listPuke
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'nTableIndex', None, 0, ), # 1
    (2, TType.LIST, 'listPuke', (TType.I32,None), None, ), # 2
  )

  def __init__(self, nTableIndex=thrift_spec[1][4], listPuke=None,):
    self.nTableIndex = nTableIndex
    self.listPuke = listPuke

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.nTableIndex = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.LIST:
          self.listPuke = []
          (_etype31, _size28) = iprot.readListBegin()
          for _i32 in xrange(_size28):
            _elem33 = iprot.readI32();
            self.listPuke.append(_elem33)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('show_puke_ret_t')
    if self.nTableIndex is not None:
      oprot.writeFieldBegin('nTableIndex', TType.I32, 1)
      oprot.writeI32(self.nTableIndex)
      oprot.writeFieldEnd()
    if self.listPuke is not None:
      oprot.writeFieldBegin('listPuke', TType.LIST, 2)
      oprot.writeListBegin(TType.I32, len(self.listPuke))
      for iter34 in self.listPuke:
        oprot.writeI32(iter34)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class ready_req_t:
  """
  Attributes:
   - nTableIndex
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'nTableIndex', None, 0, ), # 1
  )

  def __init__(self, nTableIndex=thrift_spec[1][4],):
    self.nTableIndex = nTableIndex

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.nTableIndex = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('ready_req_t')
    if self.nTableIndex is not None:
      oprot.writeFieldBegin('nTableIndex', TType.I32, 1)
      oprot.writeI32(self.nTableIndex)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class ready_ret_t:
  """
  Attributes:
   - listReady
  """

  thrift_spec = (
    None, # 0
    (1, TType.LIST, 'listReady', (TType.I32,None), None, ), # 1
  )

  def __init__(self, listReady=None,):
    self.listReady = listReady

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.LIST:
          self.listReady = []
          (_etype38, _size35) = iprot.readListBegin()
          for _i39 in xrange(_size35):
            _elem40 = iprot.readI32();
            self.listReady.append(_elem40)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('ready_ret_t')
    if self.listReady is not None:
      oprot.writeFieldBegin('listReady', TType.LIST, 1)
      oprot.writeListBegin(TType.I32, len(self.listReady))
      for iter41 in self.listReady:
        oprot.writeI32(iter41)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class pass_req_t:
  """
  Attributes:
   - nTableIndex
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'nTableIndex', None, 0, ), # 1
  )

  def __init__(self, nTableIndex=thrift_spec[1][4],):
    self.nTableIndex = nTableIndex

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.nTableIndex = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('pass_req_t')
    if self.nTableIndex is not None:
      oprot.writeFieldBegin('nTableIndex', TType.I32, 1)
      oprot.writeI32(self.nTableIndex)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class pass_ret_t:
  """
  Attributes:
   - nTableIndex
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'nTableIndex', None, 0, ), # 1
  )

  def __init__(self, nTableIndex=thrift_spec[1][4],):
    self.nTableIndex = nTableIndex

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.nTableIndex = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('pass_ret_t')
    if self.nTableIndex is not None:
      oprot.writeFieldBegin('nTableIndex', TType.I32, 1)
      oprot.writeI32(self.nTableIndex)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class quit_req_t:
  """
  Attributes:
   - nTableIndex
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'nTableIndex', None, 0, ), # 1
  )

  def __init__(self, nTableIndex=thrift_spec[1][4],):
    self.nTableIndex = nTableIndex

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.nTableIndex = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('quit_req_t')
    if self.nTableIndex is not None:
      oprot.writeFieldBegin('nTableIndex', TType.I32, 1)
      oprot.writeI32(self.nTableIndex)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class quit_ret_t:
  """
  Attributes:
   - nTableIndex
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'nTableIndex', None, 0, ), # 1
  )

  def __init__(self, nTableIndex=thrift_spec[1][4],):
    self.nTableIndex = nTableIndex

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.nTableIndex = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('quit_ret_t')
    if self.nTableIndex is not None:
      oprot.writeFieldBegin('nTableIndex', TType.I32, 1)
      oprot.writeI32(self.nTableIndex)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)