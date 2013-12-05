namespace cpp ff  
namespace as3 ff  
namespace py ff  

enum client_cmd_e {
    CHUPAI_REQ = 1
    CHAT_REQ
    READY_REQ
    PASS_REQ
    QUIT_REQ
    JOIN_TABLE_REQ //! ����ĳһ��
}

enum server_cmd_e {
    CHUPAI_RET = 1
    CHAT_RET
    READY_RET
    PASS_RET
    QUIT_RET
    ROOM_RET //��������
    JOIN_TABLE_RET //! ����ĳһ��
    ALLOC_PUKE_RET //!����
    CHANGE_TURN //! �仯������
}

// ���ﶨ����һ���ṹ�壬û�ж��巽������Ӧ�����ɵĴ�����gen-cpp�е�shared_types.h�У�������һ��class��SharedStruct,  
// ��û�п�������������������read��write���������������������л�������л��ķ���.  
// ���ˣ����е�i32��Thrift IDL�ж���ı������ͣ���Ӧ��c++�����е�int32_t  
// thrift-0.9.0.exe -gen as3 -o as3
// thrift-0.9.0.exe -gen py -o py


struct table_info_ret_t{//ÿһ��������
    1:list<string>  all_names
}

struct room_info_ret_t {//��������
  1:list<table_info_ret_t> all_tables
  2:i32 nCurRoomIndex  = -1 //!��ǰ���ڵķ���������0-N
  3:i32 nCurTableIndex = -1 //!��ǰ���ڵķ���������0-N
}

//! ����
struct alloc_puke_ret_t{
    1:i32 nAllocIndex = 0 //! �ȴ�˭����
    2:list<i32> listPuke //! ������˿�������
}
//! ����ĳһ��
struct join_table_req_t{
    1:i16 table_index = 0
}
struct join_talbe_ret_t{
    1:room_info_ret_t room_info_ret
}
//! �����߱仯
struct chagne_turn_ret_t{
    1:i16 turn_index = 0
}


//!����
//!����
struct chat_req_t{
    1:string content
}
//! ������Ϣ����
struct chat_ret_t{
    1:string content
    2:string name //! �������
    3:i16 flag = 0 //! 0��ʾ��������ʾ
}

//!����
struct show_puke_req_t{
    1:i32 nTableIndex = 0 //! ��������
    2:list<i32> listPuke //! Ҫ�����Ƶ�����
}

//! ĳ�˳���
struct show_puke_ret_t{
    1:i32 nTableIndex = 0
    2:list<i32> listPuke //! Ҫ�����Ƶ�����
}

//! ׼��
struct ready_req_t{
    1:i32 nTableIndex = 0 //! ��������
}
//! ׼������
struct ready_ret_t{
    1:list<i32> listReady //! �������� �Ѿ�׼���õ�
}

//! ����/��
struct pass_req_t{
    1:i32 nTableIndex = 0 //! ��������
}
//! ����/�� ����
struct pass_ret_t{
    1:i32 nTableIndex = 0 //! ��������
}

//! Ͷ��
struct quit_req_t{
    1:i32 nTableIndex = 0 //! ��������
}
//! Ͷ�� ����
struct quit_ret_t{
    1:i32 nTableIndex = 0 //! ��������
}

