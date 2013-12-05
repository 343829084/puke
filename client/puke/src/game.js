/*
Array.prototype.remove=function(dx)
　{
　　if(isNaN(dx)||dx>this.length){return false;}
　　for(var i=0,n=0;i<this.length;i++)
　　{
　　　　if(this[i]!=this[dx])
　　　　{
　　　　　　this[n++]=this[i]
　　　　}
　　}
　　this.length-=1
　}
*/
function array_remove(arr, index){
    var ret = [];
    for (var i = 0 ;i < arr.length; ++i){
        if (i != index)
            ret.push(arr[i]);
    }
    return ret;
}
var g_room_info= new room_info_ret_t();
var g_table_info = new table_info_ret_t();
var g_alloc_puke_t = new alloc_puke_ret_t();//! 发牌
//! 当前自己手里的牌
var g_my_puke = [];
//! 某人要出的牌
var g_show_puke = new show_puke_ret_t();
g_show_puke.nTableIndex = 3;
g_show_puke.listPuke = []
//g_show_puke.listPuke.push(1);
//! 上次出的牌
g_last_show_puke = [];
//!游戏的状态
WAIT_READY = 0;
BATTLE = 1;
IN_ROOM = 2; // 在房间中
//! 已经准备好的人
g_ready_ret = new ready_ret_t();
g_username = '';
g_connected = false;
function SetName(n){
    g_username = n;
    if (g_connected == true)
        SendContent(0, g_username);
}
function initReadyInfo(){
    g_ready_ret.listReady = [];
}
initReadyInfo();


g_game_info = {
	status : IN_ROOM,
	ready_objs : {},//! 显示准备的对象
    //! 全局talbe对象
    table_obj : false,
    //! 全局按钮保存
    btn_obj : {},
    //! 保存所有的名字对象
    name_obj:{},//!索引对应的obj
    //! 保存所有的tips
    tips_obj: {},
    //! 保存各个玩家对应的牌的数量
    puke_nums:{},
    //!  该谁出牌了的索引
    chupai_turn: 0,
    //! 闹钟
    naozhong: 0,
}

//! 初始化扑克数量
function initAllPukeNum(){
    g_game_info.puke_nums[0] = 13;
    g_game_info.puke_nums[1] = 13;
    g_game_info.puke_nums[2] = 13;
    g_game_info.puke_nums[3] = 13;
}
function getPukeNumByIndex(i){
    if (g_game_info.puke_nums.hasOwnProperty(i))
        return g_game_info.puke_nums[i];
    else
        return 0;
}
//减少
function subPukeNumByIndex(i, num){
    g_game_info.puke_nums[i] -= num;
}
g_table_info.all_names = []
g_room_info.all_tables = [g_table_info, g_table_info, g_table_info, g_table_info, g_table_info, g_table_info];
g_room_info.nCurRoomIndex = 0; //! 当前房间号
g_room_info.nCurTableIndex= 3; //! 当前的座位号
g_alloc_puke_t.listPuke = []
for (var i = 1; i <= 13; ++i){
    g_alloc_puke_t.listPuke.push(i);
}

var game_width = 800;
var game_height= 800;
var g_id = 0;

//! 获取自己的名字
function getName(){
    return g_username;
}

//! 获取桌子索引对应的角色名
function getNameByTableIndex(j){
    all_names = g_room_info.all_tables[g_room_info.nCurRoomIndex].all_names;
    var n = parseInt((g_room_info.nCurTableIndex + j) % 4);
    for (var i = 0; i < all_names.length; ++i){
        if (i == n)
            return all_names[i];
    }
    return '';
}
//! 桌子索引对应的真是的索引
function toRealTableIndex(j){
    for (var i = 0; i < 4; ++i){
        if (parseInt((i + g_room_info.nCurTableIndex)) % 4 == j)
            return i;
    }
}

//! 创建桌子图标
function createTableIcon(x_, y_, content_, id_, callback_){
    var ret =Crafty.e("HTML")
           .attr({x:x_, y:y_, w:100})
           .replace('<div id= "'+ id_ +'" class="btn btn-inverse">' + content_ + '</div>');
           //.bind('Click', callback_);
    $('#'+id_).click(callback_);;
    return ret;
}
//! 响应点击房间的事件
function clickTableIcon(nTableIndex){
    Debug('您点击了赌桌:'+(nTableIndex+1));
    //Crafty.scene('show_battle');
    var msg = new join_table_req_t(nTableIndex);
    SendMsg(client_cmd_e.JOIN_TABLE_REQ, msg);
}

function createTableIconCallback(i){
    return function(){
        clickTableIcon(i);
    }
}

function show_room(){//显示房间界面
    Crafty.scene("show_room", function() {
        //Crafty.background("#000");
        Crafty.e("2D, DOM, Text, Mouse, Tween")
                          .attr({ w:300, h:100, x: 300, y: 10 })
                          .text('打储')
                          .textFont({ size: '40px', weight: 'bold' })
                          .css({ "text-align": "left"})
                          .textColor("#FFFFFF");

        Crafty.e("2D, DOM, Text")
                      .attr({ w:300, h:150, x: 0, y: 80 })
                      .text('点击图标进入房间,当前对战情况如下:')
                      .css({ "text-align": "left"})
                      .textColor("#FFFFFF");

        for (var i = 0; i < g_room_info.all_tables.length; ++i){
            var tmpX = 30 + 200*parseInt(i%3);
            var tmpY = 200 + parseInt(i/3)*200;
            var f = createTableIconCallback(i);
            var e_table = createTableIcon(tmpX, tmpY, (i+1)+'桌', 'table_'+i, f);
            e_table.nTableIndex = i;
            /*
            Crafty.e('2D, DOM, Image, Mouse')//
                                  .attr({x: 50 + 200*parseInt(i%3), y: 200 + parseInt(i/3)*200, w: 50, h: 50})
                                  .image('./img/table.jpg')
                                  .bind('Click', function() {
                                        alert('TODO 加入房间!!');
                                    });
            */
            all_names = g_room_info.all_tables[i].all_names;
            for (var j = 0; j < all_names.length; ++j){
                var tmp_x = 0; var tmp_y = 0;
                if (j == 0){
                    tmp_x = e_table.x + 10;
                    tmp_y = e_table.y + 40;
                }
                else if (j == 1){
                    tmp_x = e_table.x + 60;
                    tmp_y = e_table.y + 10;
                }
                else if (j == 2){
                    tmp_x = e_table.x + 10;
                    tmp_y = e_table.y - 20;
                }
                else if (j == 3){
                    tmp_x = e_table.x - 30;
                    tmp_y = e_table.y + 10;
                }
                Crafty.e("2D, DOM, Text")
                      .attr({ w:50, x: tmp_x, y: tmp_y })
                      .text(all_names[j])
                      .css({ "text-align": "left"})
                      .textColor("#FFFFFF");

            }
        }
    });
}

function show_join_table(){ //!显示加入某桌的准备场景
    Crafty.scene("show_join_table", function() {
        if (g_room_info.nCurRoomIndex < 0 || g_room_info.nCurTableIndex < 0)
        {
            alert('无法获取当前房间号');
            return;
        }
        var e = Crafty.e("2D, DOM, Text, Mouse, Tween")
                          .attr({ w:300, h:100, x: 300, y: 10 })
                          .text('打储')
                          .textFont({ size: '40px', weight: 'bold' })
                          .css({ "text-align": "left"})
                          .textColor("#FFFFFF");
        Crafty.e("2D, DOM, Text")
                          .attr({ w:300, h:150, x: 0, y: 80 })
                          .text('房间[' + (g_room_info.nCurRoomIndex + 1) + ']:')
                          .css({ "text-align": "left"})
                          .textColor("#FFFFFF");
    
        //!载入背景图片
        /*
        Crafty.e('2D, DOM, Image, Mouse')
              .attr({x: 200, y: 200 , w: 10, h: 10})
              .image('./img/puke/0.jpg')
              .bind('Click', function() {
                        alert('TODO 加入房间!!');
                });
        */
        
        var e_table = Crafty.e('2D, DOM, Color')
            .attr({x: 50, y: 110 , w: 700, h: 600})
            .color('rgb(20, 125, 40)');
        all_names = g_room_info.all_tables[g_room_info.nCurRoomIndex].all_names;
        for (var j = 0; j < all_names.length; ++j){
            var n = parseInt((g_room_info.nCurTableIndex + j) % 4);
            var tmp_x = 0; var tmp_y = 0;
            if (j == 0){
                tmp_x = e_table.x - 50;
                tmp_y = e_table.y + e_table.h/2;
            }
            else if (j == 1){
                tmp_x = e_table.x + e_table.w/2;
                tmp_y = e_table.y - 20;
            }
            else if (j == 2){
                tmp_x = e_table.x + e_table.w  +10;
                tmp_y = e_table.y + e_table.h/2;
            }
            else if (j == 3){
                tmp_x = e_table.x + e_table.w/2;
                tmp_y = e_table.y  + e_table.h + 10;
            }

            Crafty.e("2D, DOM, Text")
                  .attr({ w:50, x: tmp_x, y: tmp_y })
                  .text(all_names[n])
                  .css({ "text-align": "left"})
                  .textColor("#FFFFFF");
        }
    });
}

function create_btn(x_, y_, content_, id_, callback_){
    var ret =Crafty.e("HTML")
           .attr({x:x_, y:y_, w:100})
           .replace('<div id= "'+ id_ +'" class="btn btn-block btn-lg btn-inverse">' + content_ + '</div>');
           //.bind('Click', callback_);
    $('#'+id_).click(callback_);;
    return ret;
}
//! 显示闹钟
function showNaoZhong(){
    if (g_game_info.naozhong != 0){
       g_game_info.naozhong.destroy();
       Debug('showNaoZhong 1111');
    }

    var tmp_x = 0; var tmp_y = 0;
    var j = toRealTableIndex(g_game_info.chupai_turn);
    var e_table = g_game_info.table_obj;
    if (j == 0){
        tmp_x = e_table.x + e_table.w - 180;
        tmp_y = e_table.y + e_table.h - 220;
    }
    else if (j == 1){
        tmp_x = e_table.x + e_table.w - 160;
        tmp_y = e_table.y + e_table.h - 300;
    }
    else if (j == 2){
        tmp_x = e_table.x + e_table.w/2  +10;
        tmp_y = e_table.y + 100;
    }
    else if (j == 3){
        tmp_x = e_table.x + 150;
        tmp_y = e_table.y  + e_table.h/2 + 10;
    }
        
    Debug('showNaoZhong 222');
    g_game_info.naozhong = Crafty.e("HTML")
       .attr({x:tmp_x, y:tmp_y, w:100})
       .replace('<div id= "divNaoZhong" > <img src="./img/naozhong.jpg"  width="30px" height="30px" /> </div>');
       //.bind('Click', callback_);
}

//! 创建一个牌对象
function create_puke(x_, y_, idPuke_, table_x, table_y){
    var tmpE = Crafty.e('2D, DOM, Image, Mouse, Tween')
              .attr({x: x_, y: y_, w: 10, h: 10})
              .image('./img/puke/' + idPuke_ + '.jpg')
              .bind('Click', function() {
                    if (tmpE.hasClicked == false){
                        tmpE.hasClicked = true;
                        this.y -= 20;
                    }
                    else{
                        tmpE.hasClicked = false;
                        this.y += 20;
                    }
                });
            tmpE.hasClicked = false;
            tmpE.idPuke = idPuke_;
            tmpE.table_x = table_x;
            tmpE.table_y = table_y;
    return tmpE;
}

function UpdateTable(){//更新游戏数据
    var strReady = '';
    if (g_game_info.status == WAIT_READY){
        strReady = '准备';
    }else{//! 准备文字消失
        for (var i = 0; i < 4; ++i){
            if (g_game_info.ready_objs.hasOwnProperty(i) == true)
                g_game_info.ready_objs[i].text(strReady);;
        }
    }
    for (var i = 0; i < g_ready_ret.listReady.length; ++i){
        var tableIndex = toRealTableIndex(g_ready_ret.listReady[i]);
        //Debug('UpdateTable index='+g_ready_ret.listReady[i]+ ' real index=' + tableIndex);
        
        if (g_game_info.ready_objs.hasOwnProperty(tableIndex) == false){
            var tmpX = 0;
            var tmpY = 0;
            if (tableIndex == 3){
                tmpX = 100;
                tmpY = 460;
            }
            else if (tableIndex == 1){
                tmpX = 680;
                tmpY = 460;
            }
            else if (tableIndex == 2){
                tmpX = 360;
                tmpY = 180;
            }
            else if (tableIndex == 0){
                tmpX = 360;
                tmpY = 550;
            }
            g_game_info.ready_objs[tableIndex] = Crafty.e("2D, DOM, Text, Mouse, Tween")
                      .attr({ w:300, h:100, x: tmpX, y: tmpY })
                      .text(strReady)
                      //.textFont({ size: '40px', weight: 'bold' })
                      .css({ "text-align": "left"})
                      .textColor("#FFFFFF");
        }else{
            g_game_info.ready_objs[tableIndex].text(strReady);
        }
	}
    //! 显示tips
    UpdateTips();
    //! 更新button
    UpdateBtn();
}
//! 更新tips 显示有多少张牌
function UpdateTips(){
    for (var i =0 ; i < 4; ++i){
        var tmpX = 0;
        var tmpY = 0;
        if (i == 3){
            tmpX = 100;
            tmpY = 480;
        }
        else if (i == 2){
            tmpX = 400;
            tmpY = 180;
        }
        else if (i == 1){
            tmpX = 680;
            tmpY = 480;
        }
        else if (i == 0){
            tmpX = 400;
            tmpY = 550;
        }

        if (g_game_info.tips_obj.hasOwnProperty(i) == true){//! 不显示文字
            g_game_info.tips_obj[i].text(getPukeNumByIndex(i)+'张牌');
        }else{
            g_game_info.tips_obj[i] = Crafty.e("2D, DOM, Text, Mouse, Tween")
                      .attr({ w:300, h:100, x: tmpX, y: tmpY })
                      .text(getPukeNumByIndex(i) + '张牌!')
                      .css({ "text-align": "left"})
                      .textColor("#FB3004");
        }
    }
    
    all_names = g_room_info.all_tables[g_room_info.nCurRoomIndex].all_names;
    var e_table = g_game_info.table_obj;
    //Debug('UpdateTips nCurRoomIndex:'+g_room_info.nCurRoomIndex+ 'name_len:' + g_room_info.all_tables[g_room_info.nCurRoomIndex].all_names.length);
    for (var j = 0; j < all_names.length; ++j){
        //Debug('UpdateTips name:'+all_names[j]);

        var n = toRealTableIndex(j);
        var tmp_x = 0; var tmp_y = 0;
        if (n == 3){
            tmp_x = e_table.x + 10;
            tmp_y = e_table.y + e_table.h/2;
        }
        else if (n == 2){
            tmp_x = e_table.x + e_table.w/2;
            tmp_y = e_table.y  + 10;
        }
        else if (n == 1){
            tmp_x = e_table.x + e_table.w - 50;
            tmp_y = e_table.y + e_table.h/2;
        }
        else if (n == 0){
            tmp_x = e_table.x + e_table.w/2;
            tmp_y = e_table.y  + e_table.h - 20;
        }

        playerName = getNameByTableIndex(n);
        //Debug('对手:'+playerName);
        if (g_game_info.name_obj.hasOwnProperty(j) == false){
            g_game_info.name_obj[j] = Crafty.e("2D, DOM, Text")
                  .attr({ w:50, x: tmp_x, y: tmp_y })
                  .text(playerName)
                  .css({ "text-align": "left"})
                  .textColor("#FFFFFF");
        }else{
            g_game_info.name_obj[j].text(playerName);
        }
    }
}

function show_battle(){ //!显示对战
    Crafty.scene("show_battle", function() {
        if (g_room_info.nCurRoomIndex < 0 || g_room_info.nCurTableIndex < 0)
        {
            alert('无法获取当前房间号');
            return;
        }
        var e = Crafty.e("2D, DOM, Text, Mouse, Tween")
                          .attr({ w:300, h:100, x: 300, y: 10 })
                          .text('打储')
                          .textFont({ size: '40px', weight: 'bold' })
                          .css({ "text-align": "left"})
                          .textColor("#FFFFFF");
        Crafty.e("2D, DOM, Text")
                          .attr({ w:300, h:150, x: 0, y: 80 })
                          .text('房间[' + (g_room_info.nCurRoomIndex + 1) + ']:')
                          .css({ "text-align": "left"})
                          .textColor("#FFFFFF");
    
        //!载入背景图片
        /*
        Crafty.e('2D, DOM, Image, Mouse')
              .attr({x: 200, y: 200 , w: 10, h: 10})
              .image('./img/puke/0.jpg')
              .bind('Click', function() {
                        alert('TODO 加入房间!!');
                });
        */
        
        var e_table = Crafty.e('2D, DOM, Color')
            .attr({x: 0, y: 100 , w: 800, h: 660})
            .color('rgb(20, 125, 40)');
        g_game_info.table_obj = e_table;
        all_names = g_room_info.all_tables[g_room_info.nCurRoomIndex].all_names;
        for (var j = 0; j < all_names.length; ++j){
            var n = toRealTableIndex(j);
            var tmp_x = 0; var tmp_y = 0;
            if (n == 3){
                tmp_x = e_table.x + 10;
                tmp_y = e_table.y + e_table.h/2;
            }
            else if (n == 2){
                tmp_x = e_table.x + e_table.w/2;
                tmp_y = e_table.y  + 10;
            }
            else if (n == 1){
                tmp_x = e_table.x + e_table.w - 50;
                tmp_y = e_table.y + e_table.h/2;
            }
            else if (n == 0){
                tmp_x = e_table.x + e_table.w/2;
                tmp_y = e_table.y  + e_table.h - 20;
            }

            playerName = getNameByTableIndex(n);
            if (g_game_info.name_obj.hasOwnProperty(j) == false){
                g_game_info.name_obj[j] = Crafty.e("2D, DOM, Text")
                      .attr({ w:50, x: tmp_x, y: tmp_y })
                      .text(playerName)
                      .css({ "text-align": "left"})
                      .textColor("#FFFFFF");
            }else{
                g_game_info.name_obj[j].text(playerName);
            }
        }
        //! 显示别人的牌，只显示背面
        Crafty.e("2D, DOM, Image")
                          .attr({ w:300, h:150, x: 10, y: 450 })
                          .image('./img/puke/heng_0.jpg');
        Crafty.e("2D, DOM, Image")
                          .attr({ w:300, h:150, x: 720, y: 450 })
                          .image('./img/puke/heng_0.jpg');
        Crafty.e("2D, DOM, Image")
                          .attr({ w:300, h:150, x: 350, y: 100 })
                          .image('./img/puke/0.jpg');
        //!显示按钮
        g_game_info.btn_obj ['Ready']    = create_btn(e_table.x + e_table.w - 120, e_table.y + e_table.h - 180, '准备', 'Ready', clickReady);
        g_game_info.btn_obj ['XuanZhan'] = create_btn(e_table.x + e_table.w - 120, e_table.y + e_table.h - 130, '宣战', 'XuanZhan', clickXuanZhan);
        //! 显示准备
		UpdateTable();
    });
}
//! 销毁所有的牌
function destroyAllPuke(){
    for (var i = 0; i < g_my_puke.length; ++i){
        g_my_puke[i].destroy();
    }
    g_my_puke = [];
}
//! 响应发牌的事件
function handleFaPai(){
    destroyLastPuke();
    //! 发牌动画
    destroyAllPuke();
    var tmpIndex = 0;
    var e_table = g_game_info.table_obj;
    var f = function (){
        var tmpE = create_puke(80 + 35*tmpIndex, e_table.y + e_table.h - 180, g_alloc_puke_t.listPuke[tmpIndex], e_table.x, e_table.y);
        tmpIndex += 1;
        g_my_puke.push(tmpE);//! 保存自己手里的牌
        if (tmpIndex >= g_alloc_puke_t.listPuke.length){
            //! 发牌结束了,重新整理牌,把老的牌都先销毁掉
            Crafty.e('Delay').delay(resortPuke, 1000, 0);
            //! 显示当前牌的数量
            initAllPukeNum();
            g_game_info.status = BATTLE;
            //! 准备tips关掉
            initReadyInfo();
            UpdateTable();
        }
    }
    Crafty.e('Delay').delay(f, 100, g_alloc_puke_t.listPuke.length-1);
}
//! 获取某张扑克牌的战斗数值
function GetBattleValByPukeId(id){
    var n = parseInt((id-1) % 13);
    if (n == 0){//'A'
        return 14;
    }else if (n == 1){//!'2'
        return 15;
    }
    else{
        return n+1;
    }
}

function destroyBtnById(id){
    if (g_game_info.btn_obj.hasOwnProperty(id) == true){
        g_game_info.btn_obj[id].destroy();
    }
}
//删除所有的btn
function destroyAllBtn(){
    for (var k in g_game_info.btn_obj){
        destroyBtnById(k);
    }
    g_game_info.btn_obj = {};
}

//! 点击过
function clickPassBtn(){
    Debug('clickPassBtn');
    var msg = new pass_req_t();
    SendMsg(client_cmd_e.PASS_REQ, msg);
}
//更新显示button
function UpdateBtn(){
    Debug('UpdateBtn');
    destroyAllBtn();
    var e_table = g_game_info.table_obj;
    if (g_game_info.status == WAIT_READY)
    {
        g_game_info.btn_obj ['Ready']    = create_btn(e_table.x + e_table.w - 120, e_table.y + e_table.h - 180, '准备', 'Ready', clickReady);
        g_game_info.btn_obj ['XuanZhan'] = create_btn(e_table.x + e_table.w - 120, e_table.y + e_table.h - 130, '宣战', 'XuanZhan', clickXuanZhan);
    }
    else if (g_game_info.status == BATTLE){
        if (g_game_info.chupai_turn == g_room_info.nCurTableIndex){//! 该自己出牌
            Debug('UpdateBtn show chupai:'+g_game_info.chupai_turn + ':' + g_room_info.nCurTableIndex);
            g_game_info.btn_obj ['Pass'] = create_btn(e_table.x + e_table.w - 120, e_table.y + e_table.h - 130, '不管', 'Pass', clickPassBtn);
            g_game_info.btn_obj ['ChuPai'] = create_btn(e_table.x + e_table.w - 120, e_table.y + e_table.h - 80, '出牌', 'ChuPai', clickChuPai);
        }
    }
}

//! 发牌结束了,重新整理牌,把老的牌都先销毁掉
function resortPuke(){
    for (var i = 0; i < g_my_puke.length; ++i){
        g_my_puke[i].destroy();
    }
    g_my_puke = [];
    
    var arrayPuke = g_alloc_puke_t.listPuke.concat();
    arrayPuke.sort(function(x,y){return GetBattleValByPukeId(y)-GetBattleValByPukeId(x);}); 

    var tmpIndex = 0;
    var e_table = g_game_info.table_obj;
    var f = function (){
        var tmpE = create_puke(80 + 35*tmpIndex, e_table.y + e_table.h - 180, arrayPuke[tmpIndex], e_table.x, e_table.y);
        tmpIndex += 1;
        g_my_puke.push(tmpE);//! 保存自己手里的牌
        if (tmpIndex >= g_alloc_puke_t.listPuke.length){
            //! 发牌结束了，才能显示出牌按钮 
            UpdateTable();
        }
    }
    for (var i = 0; i < arrayPuke.length; ++i){
        f();
    }
}

//! 响应点击准备按钮
function clickReady(){
    var msg = new ready_req_t();
    SendMsg(client_cmd_e.READY_REQ, msg);
}


//!响应点击宣战
function clickXuanZhan(){
    alert('TODO宣战');
}
//! 响应出牌按钮
function clickChuPai(){
    var msg = new show_puke_req_t();
    msg.listPuke = [];
    for (var i = 0; i < g_my_puke.length; ++i){
        if (g_my_puke[i].hasClicked == true){
            msg.listPuke.push(g_my_puke[i].idPuke);
        }
    }
    SendMsg(client_cmd_e.CHUPAI_REQ, msg);
    
    
    //! debug 模式自己赋值选中的牌
    /*
    g_show_puke.listPuke = [];
    for (var i = 0; i < g_my_puke.length; ++i){
        if (g_my_puke[i].hasClicked == true){
            g_show_puke.listPuke.push(g_my_puke[i].idPuke);
        }
    }
    ShowChuPai();
    */
}
//! 响应聊天按钮
function clickChat(){
    var msg = new chat_req_t();
    msg.content = $("#chatContent").val();
    if (msg.content != ''){
        SendMsg(client_cmd_e.CHAT_REQ, msg);
        $("#chatContent").val('');
    }
}
//! 输出聊天内容
function SysMsg(head, content){
    var tmpHtml = '<div style="margin:0px 0px 5px 0px;"><font color="red">' + head + ':</font>' + content + '</div>';
    $("#msgOutput").append(tmpHtml);
    $("#msgOutput").scrollTop(100000);
}
function Debug(content){
    SysMsg('系统', content);
}
g_client_cmd = client_cmd_e;
g_sys_msg = SysMsg;

//! 消除掉原来的牌
function destroyLastPuke(){
    for (var i = 0; i < g_last_show_puke.length; ++i){
        g_last_show_puke[i].destroy();
    }
    g_last_show_puke = [];
}
//! 出牌
function ShowChuPai(){
    var listSelect = [];

    //! 先把上次出的牌删掉
    destroyLastPuke();
    //! 从当前牌数量中减去
    subPukeNumByIndex(toRealTableIndex(g_game_info.chupai_turn), g_show_puke.listPuke.length);
    if (g_game_info.chupai_turn != g_room_info.nCurTableIndex) { //! 轮到别人出牌
        //! 直接显示牌就行了
        for (var i = 0; i < g_show_puke.listPuke.length; ++i){
            var idPuke = g_show_puke.listPuke[i];
            var x = g_my_puke[0].table_x + 350 + (i - parseInt(g_show_puke.listPuke.length/2))*35;
            var y = g_my_puke[0].table_y + 200;
            var tmpNewE = create_puke(x, y, idPuke,  g_my_puke[0].table_x, g_my_puke[0].table_y);
            g_last_show_puke.push(tmpNewE);
        }
        //! 更新一下tips
        UpdateTable();
        if (getPukeNumByIndex(toRealTableIndex(g_game_info.chupai_turn)) == 0){//!赢啦
            handleEnd();
        }
        return true;
    }
    //! 轮到我出牌
    var GetSelect = function (idPuke) {
        for (var i = 0; i < g_my_puke.length; ++i){
            if (g_my_puke[i].idPuke == idPuke)
                return i;
        }
        return -1;
    }
    for (var i = 0; i < g_show_puke.listPuke.length; ++i){
    //for (var i = 0; i < g_my_puke.length; ++i){
        var idPuke = g_show_puke.listPuke[i];
        var ret = GetSelect(idPuke);
        if (ret >= 0){
            tmpE = g_my_puke[ret];
            listSelect.push(tmpE);
            //! 重现创建扑克牌，展示动画
            //alert(tmpE.idPuke);
            
            var tmpNewE = create_puke(tmpE.x, tmpE.y, tmpE.idPuke,  tmpE.table_x, tmpE.table_y);
            tmpNewE.tween({
                x: tmpE.table_x + 350 + (i - parseInt(g_show_puke.listPuke.length/2))*35,
                y : tmpE.table_y + 200
            }, 5).bind("TweenEnd", function() {
                // todo
                //tmpNewE.destroy();
            });
            tmpE.destroy();
            g_last_show_puke.push(tmpNewE);
        }
    }
    //! 从当前手里的牌中删除已经出掉的牌，重新排序
    for (var i = 0; i < listSelect.length; ++i){
        for (var j = 0; j < g_my_puke.length; ++j){
            if (g_my_puke[j] == listSelect[i]){
                g_my_puke = array_remove(g_my_puke, j);
                break;
            }
        }
    }

    //! 重新显示牌
    for (var j = 0; j < g_my_puke.length; ++j){
        g_my_puke[j].x = 80 + 35*j;
    }
    //! 更新一下tips
    UpdateTable();
    if (getPukeNumByIndex(toRealTableIndex(g_game_info.chupai_turn)) == 0){//!赢啦
        handleEnd();
    }
}
//! 处理获胜
function handleEnd(){
    g_game_info.status = WAIT_READY;
    //! 发牌结束了，才能显示出牌按钮 
    destroyBtnById('ChuPai');
    UpdateTable();
    Debug('此局结束');
}

function loadResource(callback){
    Crafty.init(game_width, game_height, document.getElementById('game'));
    show_room();
    show_join_table();
    show_battle();
    var res = [ "./img/puke/heng_0.jpg", "./flash/xinfeng.swf"];
    for (var i = 0; i <= 54; ++i){
        res.push("./img/puke/" +  i + ".jpg");
    }
    Crafty.load(res,
        function() {
            insertSwfInfo('#flashDiv', 'flash/xinfeng.swf', 0, 0);
            callback();
        },
        // on load progress
        function(e) {
            // do sth
        },
        // on error
        function(e) {
            // do sth
        });
  
    return;
}
function connectServer(){
    var f = function (){
        Debug('点击了Login按钮');
        try {
            flashExt().Connect('112.124.57.159', 20242);
            Debug('Connect调用完毕');
        }
        catch(err){
            Debug('异常:'+err.message );
        }
    }
    setTimeout(f, 1000);
    return;
}

function load_game(){
    Crafty.scene("show_room");
    return;
}

function  handleChat(msg){
    //Debug('handleChat收到消息');
    SysMsg(msg.name, msg.content);
}
function HandleError() {
    Debug('连接断开');
} 
function onConnect(socketId){
    Debug('连接建立');
    g_connected = true;
    if (g_username != '')
        SendContent(0, g_username);
}
function handleRoomInfo(msg){
    g_room_info = msg;
    Debug('handleRoomInfo:'+g_room_info.all_tables[0].all_names.length);
    for (var k in g_room_info.all_tables[0].all_names)
        Debug('handleRoomInfo name:'+g_room_info.all_tables[0].all_names[k])
    if (g_game_info.status == IN_ROOM)
        Crafty.scene("show_room");
    else
        UpdateTable();
}
function handleJoinTalbe(msg){
    g_room_info = msg.room_info_ret;
    Debug('handleJoinTalbe');
    g_game_info.status = WAIT_READY;
    Crafty.scene('show_battle');
}
//! 响应某人准备好了
function handleReadyMsg(msg){
    Debug('handleReadyMsg');
    g_ready_ret = msg;
    UpdateTable();
}
//! 发牌的消息
function handleFapaiMsg(msg){
    Debug('handleFapaiMsg');
    g_alloc_puke_t = msg;
    handleFaPai();
}
//! 处理某人出牌
function handleChuPaiMsg(msg){
    Debug('handleChuPaiMsg');
    g_show_puke = msg;
    ShowChuPai();
}
//! 变化出牌人
function handleChangeTurn(msg){
    Debug('handleChangeTurn');
    g_game_info.chupai_turn = msg.turn_index;
    UpdateBtn();
    showNaoZhong();
}
var regCmdDict = {
    //server_cmd_e['CHAT_RET']: [chat_ret_t, handleChat],
}
regCmdDict[server_cmd_e['CHAT_RET']] = [chat_ret_t, handleChat];
regCmdDict[server_cmd_e['ROOM_RET']] = [room_info_ret_t, handleRoomInfo];
regCmdDict[server_cmd_e['JOIN_TABLE_RET']] = [join_talbe_ret_t, handleJoinTalbe];
regCmdDict[server_cmd_e['READY_RET']] = [ready_ret_t, handleReadyMsg];
regCmdDict[server_cmd_e['ALLOC_PUKE_RET']] = [alloc_puke_ret_t, handleFapaiMsg];
regCmdDict[server_cmd_e['CHUPAI_RET']] = [show_puke_ret_t, handleChuPaiMsg];
regCmdDict[server_cmd_e['CHANGE_TURN']] = [chagne_turn_ret_t, handleChangeTurn];

MultiRegCallBack(regCmdDict);
