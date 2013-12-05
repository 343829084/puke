namespace cpp ff  
namespace as3 ff  
namespace py ff  

enum client_cmd_e {
    CHUPAI_REQ = 1
    CHAT_REQ
    READY_REQ
    PASS_REQ
    QUIT_REQ
    JOIN_TABLE_REQ //! 加入某一桌
}

enum server_cmd_e {
    CHUPAI_RET = 1
    CHAT_RET
    READY_RET
    PASS_RET
    QUIT_RET
    ROOM_RET //房间数据
    JOIN_TABLE_RET //! 加入某一桌
    ALLOC_PUKE_RET //!发牌
    CHANGE_TURN //! 变化出牌人
}

// 这里定义了一个结构体，没有定义方法，对应于生成的代码在gen-cpp中的shared_types.h中，其中有一个class叫SharedStruct,  
// 有没有看到其中有两个方法叫read和write，这就是用来对其进行序列化与把序列化的方法.  
// 对了，其中的i32是Thrift IDL中定义的变量类型，对应于c++语言中的int32_t  
// thrift-0.9.0.exe -gen as3 -o as3
// thrift-0.9.0.exe -gen py -o py


struct table_info_ret_t{//每一桌的数据
    1:list<string>  all_names
}

struct room_info_ret_t {//房间数据
  1:list<table_info_ret_t> all_tables
  2:i32 nCurRoomIndex  = -1 //!当前所在的房间索引号0-N
  3:i32 nCurTableIndex = -1 //!当前所在的房间索引号0-N
}

//! 发牌
struct alloc_puke_ret_t{
    1:i32 nAllocIndex = 0 //! 先从谁发起
    2:list<i32> listPuke //! 分配的扑克牌内容
}
//! 加入某一桌
struct join_table_req_t{
    1:i16 table_index = 0
}
struct join_talbe_ret_t{
    1:room_info_ret_t room_info_ret
}
//! 出牌者变化
struct chagne_turn_ret_t{
    1:i16 turn_index = 0
}


//!请求
//!聊天
struct chat_req_t{
    1:string content
}
//! 聊天消息返回
struct chat_ret_t{
    1:string content
    2:string name //! 玩家名称
    3:i16 flag = 0 //! 0表示房间内显示
}

//!出牌
struct show_puke_req_t{
    1:i32 nTableIndex = 0 //! 桌子索引
    2:list<i32> listPuke //! 要出的牌的内容
}

//! 某人出牌
struct show_puke_ret_t{
    1:i32 nTableIndex = 0
    2:list<i32> listPuke //! 要出的牌的内容
}

//! 准备
struct ready_req_t{
    1:i32 nTableIndex = 0 //! 桌子索引
}
//! 准备返回
struct ready_ret_t{
    1:list<i32> listReady //! 桌子索引 已经准备好的
}

//! 不管/过
struct pass_req_t{
    1:i32 nTableIndex = 0 //! 桌子索引
}
//! 不管/过 返回
struct pass_ret_t{
    1:i32 nTableIndex = 0 //! 桌子索引
}

//! 投降
struct quit_req_t{
    1:i32 nTableIndex = 0 //! 桌子索引
}
//! 投降 返回
struct quit_ret_t{
    1:i32 nTableIndex = 0 //! 桌子索引
}

