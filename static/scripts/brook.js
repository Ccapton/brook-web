

function switchMenu() {
    var menu_items = $("#footer").children();
    if ($(".menu-item-hidden").length == 0){
        $(menu_items[0]).addClass('menu-item-hidden');
        $(menu_items[1]).addClass('menu-item-hidden');
        $(menu_items[2]).addClass('menu-item-hidden');
        $(menu_items[3]).children().first().removeClass('fui-arrow-left');
        $(menu_items[3]).children().first().addClass('fui-arrow-right');
    }else {
        $(menu_items[0]).removeClass('menu-item-hidden');
        $(menu_items[1]).removeClass('menu-item-hidden');
        $(menu_items[2]).removeClass('menu-item-hidden');
        $(menu_items[3]).children().first().removeClass('fui-arrow-right');
        $(menu_items[3]).children().first().addClass('fui-arrow-left');
    }
}

function addPort() {
    clearInterval(state_interval);
    $(function () { $('#myModal').on('hide.bs.modal', function () {
        clearInterval(state_interval);
        state_interval = setInterval(brook_state, 2000);
      })
    });
    if (state_jsons[2].length !== 0){
        $("#socks5").hide();
    } else {
        $("#socks5").show();
    }
    $("#service-type").children().find('input').click(function () {
        console.log('click radio');
        var service_type = $(this).val();
        if (service_type == 2)
            $("#username").show();
        else
            $("#username").hide();
    })
}

function refreshPort(){
    $("#port-info-del").children().remove();
    var services_list = [];
    var type = -1;
    if ($("#radio-brook-del").prop('checked')){
        type = 0;
        services_list = state_jsons[0];
    }else if($("#radio-ss-del").prop('checked')){
        type = 1;
        services_list = state_jsons[1];
    }else if($("#radio-socks5-del").prop('checked')){
        type = 2;
        services_list = state_jsons[2];
    }
    for (var i = 0; i < services_list.length; i++) {
        var port = -1;
        port = services_list[i].port;
        var using_port = '';
        var opened_port = '<button type="button" class="btn btn-success" style="margin-bottom: 4px;margin-left: 2px;"' +
            ' onclick="submit_delport('+type+','+port+')">'+port+'</button>';
        var closed_port = '<button type="button" class="btn btn-danger" style="margin-bottom: 4px;margin-left: 2px;"' +
            ' onclick="submit_delport('+type+','+port+')">'+port+'</button>';
        if (services_list[i].state == 0)
            using_port = closed_port;
        else
            using_port = opened_port;
        var port_item = $(using_port);
        port_item.data('type',type);
        port_item.data('port',port);
        $("#port-info-del").append(port_item);
    }
}

function delPort() {
    clearInterval(state_interval);
    $(function () { $('#myModal2').on('hide.bs.modal', function () {
        clearInterval(state_interval);
        state_interval = setInterval(brook_state, 2000);
      })
    });

    refreshPort();

    $("#service-type-del").children().find('input').click(function () {
        refreshPort();
    });

}

function submit_addport() {

    var type = -1;
    if ($("#radio-brook").prop('checked')){
        type = 0;
    }else if($("#radio-ss").prop('checked')){
        type = 1;
    }else if($("#radio-socks5").prop('checked')){
        type = 2;
    }
    var port = $('#port').val();
    var psw = $('#psw').val();
    var username = $('#username').val();
    if (port <= 0 || Number.isInteger(port)) {
        alert('端口号请使用正整数');
        return;
    }
    if (username == null || username === undefined || username == '') {
        console.log('增加一个不使用账号的端口服务');
        username = '';
    } else{
        if (psw == null || psw === undefined || psw == ''){
            alert('密码不能为空');
            return;
        }
    }
    if ( type !== 2 && (psw == null || psw === undefined || psw == '')){
            alert('密码不能为空');
            return;
    }
    $.get('api/addport',{'type':type,'port':Number(port),'password':psw,'username':username},function (result,status) {
        console.log(status);
        if (result.code == 0){
                $('#port').val(null);
                $('#psw').val('');
                $('#username').val('');
                $("#radio-brook").prop('checked',true);
                $("#radio-ss").prop('checked',false);
                $("#radio-socks5").prop('checked',false);
                console.log('添加服务成功！');
                $('#myModal').modal('hide');
        }else if (result.code == -2){
            alert('端口已被占用，请换一个端口');
        }else {
            alert('端口开启失败')
        }
    });
}

function submit_delport(type,port){
    console.log('删除端口',type,port);
    var service = '';
    if (type == 0)
        service = 'Brook';
    else if (type == 1)
        service = 'ShadowSocks';
    else if (type == 2)
        service = 'Socks5';
    var delete_confirm = confirm('确定要删除端口：'+port+'上的'+service+'服务?');
    if (delete_confirm){
        $.get('api/delport',{'type':type,'port':port},function (result) {
            if (result.code == 0){
                alert('成功删除端口！');
                $('#myModal2').modal('hide');
            }
        });
    }
}

function turnoffAllPort(){
    clearInterval(state_interval);
    $(function () { $('#myModal3').on('hide.bs.modal', function () {
        clearInterval(state_interval);
        state_interval = setInterval(brook_state, 2000);
      })
    });
}

function submitTurnoff(){
    var type = -1;
    if ($("#radio-brook-2").prop('checked')){
        type = 0;
    }else if($("#radio-ss-2").prop('checked')){
        type = 1;
    }else if($("#radio-socks5-2").prop('checked')){
        type = 2;
    }
    $.get('api/stopservice',{'username':getCookie().username,'password':getCookie().password,'type':type,'port':-1},function (result) {
        if (result.code == 0){
            $('#myModal3').modal('hide');
            console.log('关闭服务')
        }
    })

}

accordion0 = '<div class="accordion" id="accordion-0"></div>'
accordion1 = '<div class="accordion" id="accordion-1"></div>'
accordion2 = '<div class="accordion" id="accordion-2"></div>'

accordions = [accordion0,accordion1,accordion2];

function brook_state(){
    $.get("api/servicestate",function (result) {
        if (result.code == 0) {
            update_ui(result.data);
        }
    })
}

brook_state();
state_interval = setInterval(brook_state, 2000);


function judgeCookie(cookie) {
    $("#login-form").hide();
    if(cookie.username && cookie.password) {
         $.get("api/login",{"username":getCookie().username,"password":getCookie().password},function (result) {
            console.log(result);
            if(result.code != 0){
                 $(location).attr('href', 'login');
            }else {
                $("#login-form").show();
            }
        })
    }else {
        $(location).attr('href', 'login');
    }
}

judgeCookie(getCookie());


function update_ui(brook_state_json) {
    state_jsons = [brook_state_json.brook,brook_state_json.shadowsocks,brook_state_json.socks5];
            for (var j = 0; j < 3; j++) {
                if ($("#accordion-"+j).length == 0){
                    $("#panel-"+(j+1)).append(accordions[j]);
                    for (var i = 0; i < state_jsons[j].length; i++) {
                        if ($("#port-item"+j+"-"+i).length == 0){
                            var isenabled = 'port';
                            var icon_isenabled = 'icon-enabled';
                            var icon_isenabled_class = 'fui-check-circle';
                            var toogle_item = '<div class="toggle-button-wrapper"><input type="checkbox" class="toggle-button" id="toggle-button'+j+'-'+i+'" ' +
                                'name="switch"><label for="toggle-button'+j+'-'+i+'" class="button-label"><span class="circle"></span>' +
                                '<span class="text on" contenteditable="false">ON</span><span class="text off" contenteditable="false">OFF</span></label></div>';
                            if (state_jsons[j][i].state == 0){
                                isenabled = 'port-red';
                                icon_isenabled = 'icon-disabled';
                                icon_isenabled_class = 'fui-info-circle';
                            }
                            var psw_item = '<p class="port-detail-p">密码：'+state_jsons[j][i].psw+'</p>';
                            var encode_method_item = '<p class="port-detail-p">加密方式：aes-256-cfb</p>';
                            var username_item = '<p class="port-detail-p">用户：'+state_jsons[j][i].username+'</p>';
                            if (state_jsons[j][i].username == ''){
                                psw_item = '';
                            } else {
                                if (j == 2)
                                    psw_item = username_item + psw_item;
                                if (j == 1)
                                    psw_item = psw_item + encode_method_item;
                            }
                            var child_port = '<div class="accordion-group"  id="port-item'+j+'-'+i+'"><div class="accordion-heading '+isenabled+'"><a class=' +
                                '"accordion-toggle collapsed port-a" style="color:white" contenteditable="false" data-parent="#accordion-'+j+'" ' +
                                'data-toggle="collapse" href="#accordion-element'+j+'-'+i+'">端口：'+state_jsons[j][i].port+'</a>' +
                                '<span id="icon'+j+'-'+i+'" class="'+icon_isenabled_class+' '+icon_isenabled+'"></span></div><div class=' +
                                '"accordion-body collapse" id="accordion-element'+j+'-'+i+'" style="height: 0px;">' +
                                '<p class="port-detail-p">IP：'+state_jsons[j][i].ip+'</p>' +
                                '<p class="port-detail-p">端口：'+state_jsons[j][i].port+'</p>'+psw_item+toogle_item+'</div></div></div>';
                            $("#accordion-"+j).append(child_port);
                            if (state_jsons[j][i].state == 0){
                                $("#toggle-button"+j+"-"+i).prop("checked",false);
                            } else{
                                $("#toggle-button"+j+"-"+i).prop("checked",true);
                            }
                            this_toggle = $("#toggle-button"+j+"-"+i);
                            this_toggle.data('index',j);
                            this_toggle.data('index2',i);
                            this_toggle.click(function() {
                                var j = $(this).data('index');
                                var i = $(this).data('index2');
                                var ischecked = $(this).prop("checked");
                                console.log(ischecked);
                                clearInterval(state_interval);
                                var api_url = "";
                                var api_url1 = "api/startservice";
                                var api_url2 = "api/stopservice";
                                if (ischecked)
                                    api_url = api_url1;
                                else
                                    api_url = api_url2;
                                console.log(api_url);
                                $.get(api_url,{'username':getCookie().username,'password':getCookie().password,'type':j,'port':state_jsons[j][i].port},function (result) {
                                    state_interval = setInterval(brook_state,2000);
                                    console.log('已改变端口状态');
                                })
                            });
                        }
                    }

                }else {
                    for (var i = 0; i < state_jsons[j].length; i++) {
                        if ($("#port-item"+j+"-"+i).length != 0){
                            $("#port-item"+j+"-"+i).find('a').first().text('端口：'+state_jsons[j][i].port);
                            var isenabled = 'port';
                            var icon_isenabled = 'icon-enabled';
                            var icon_isenabled_class = 'fui-check-circle';
                            if (state_jsons[j][i].state == 0){
                                isenabled = 'port-red';
                                icon_isenabled = 'icon-disabled';
                                icon_isenabled_class = 'fui-info-circle';
                            }
                            $("#port-item"+j+"-"+i).find('div').first().removeClass('port').removeClass('port-red').addClass(isenabled);
                            $("#icon"+j+"-"+i).removeClass('icon-enabled').removeClass('icon-disabled').removeClass('fui-check-circle')
                                .removeClass('fui-info-circle').addClass(icon_isenabled).addClass(icon_isenabled_class);
                            $($("#accordion-element"+j+"-"+i).children(".port-detail-p")[0]).text("IP："+state_jsons[j][i].ip);
                            $($("#accordion-element"+j+"-"+i).children(".port-detail-p")[1]).text("端口："+state_jsons[j][i].port);
                            if (j == 2){
                                $($("#accordion-element"+j+"-"+i).children(".port-detail-p")[2]).text("用户："+state_jsons[j][i].username);
                                $($("#accordion-element"+j+"-"+i).children(".port-detail-p")[3]).text("密码："+state_jsons[j][i].psw);
                            }else {
                                $($("#accordion-element"+j+"-"+i).children(".port-detail-p")[2]).text("密码："+state_jsons[j][i].psw);
                            }
                        }
                        if (state_jsons[j][i].state == 0){
                            $("#toggle-button"+j+"-"+i).prop("checked",false);
                        } else{
                            $("#toggle-button"+j+"-"+i).prop("checked",true);
                        }
                    }
                    var existed_length = $("#accordion-"+j).children(".accordion-group").length;
                    var current_length = state_jsons[j].length;
                    if (existed_length !== current_length){
                        $("#accordion-"+j).remove();
                    }

               }
            }
}



