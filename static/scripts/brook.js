

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
    $('#myModal').on('hide.bs.modal', function () {
        clearInterval(state_interval);
        state_interval = setInterval(brook_state, 2000);
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
    $('#myModal2').on('hide.bs.modal', function () {
        clearInterval(state_interval);
        state_interval = setInterval(brook_state, 2000);
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
    var info = $('#info').val();
    if (info.length > 10) {
        alert('备注字符串长度不能大于10');
        return;
    }
    if (port <= 0 || Number.isInteger(port)) {
        alert('端口号请使用正整数');
        return;
    } else if (port < 1024){
        alert('0-1023为系统保留端口');
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
    $.post('api/addport',{'type':type,'port':Number(port),'password':psw,'username':username,'info':info},function (result,status) {
        console.log(status);
        if (result.code == 0){
                $('#port').val(null);
                $('#psw').val('');
                $('#username').val('');
                $('#info').val('');
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
        $.post('api/delport',{'type':type,'port':port},function (result) {
            if (result.code == 0){
                alert('成功删除端口！');
                $('#myModal2').modal('hide');
            }
        });
    }
}

function turnoffAllPort(){
    clearInterval(state_interval);
    $('#myModal3').on('hide.bs.modal', function () {
        clearInterval(state_interval);
        state_interval = setInterval(brook_state, 2000);
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
    $.post('api/stopservice',{'username':getCookie().username,'password':getCookie().password,'type':type,'port':-1},function (result) {
        if (result.code == 0){
            $('#myModal3').modal('hide');
            console.log('关闭服务')
        }
    })
}

$('#myModal4').on('hide.bs.modal', function () {
        clearInterval(state_interval);
        state_interval = setInterval(brook_state, 2000);
});

$('#myModal5').on('hide.bs.modal', function () {
        clearInterval(state_interval);
        state_interval = setInterval(brook_state, 2000);
        $("#myModelBody5").children().remove();
});

function qrImage(service_json){
    clearInterval(state_interval);
    $.post('api/generateqrimg',{'type':1,'ip':service_json.ip,'port':service_json.port,'password':service_json.psw},function (result) {
        if (result.code == 0){
            if ($("#myModelBody5").children().length == 0) {
                img = '<img id="qr-img" style="display: block;margin: auto;position: center" src="' + service_json.qr_img_path + '">';
                $("#myModelBody5").append(img);
            } else {
                $("#qr-img").attr('src',service_json.qr_img_path);
            }
        } else {
            console.log('获取二维码失败')
        }
    });
}

clipboard = new ClipboardJS('#copy-link-btn');
clipboard.on('success', function(e) {
    console.log('复制成功');
    e.clearSelection();
});
clipboard.on('error', function(e) {
    console.log('复制失败');
});

function copyLink(service_json){
    clearInterval(state_interval);
    $('#myModalLabel4').text('服务链接');
    if ($('#myModelBody4').children().length == 0)
        $('#myModelBody4').append("<p id='link-p' value='"+service_json.link+"' style='word-break:break-all;" +
            "white-space:normal;word-wrap:break-word;'>"+service_json.link+"</p>");
    else
        $('#link-p').text(service_json.link);
        $('#link-p').attr('value',service_json.link);
}


accordion0 = '<div class="accordion" id="accordion-0"></div>'
accordion1 = '<div class="accordion" id="accordion-1"></div>'
accordion2 = '<div class="accordion" id="accordion-2"></div>'

accordions = [accordion0,accordion1,accordion2];

function brook_state(){
    $.post("api/servicestate",function (result) {
        if (result.code == 0) {
            update_ui(result.data);
        }
    })
}

function judgeCookie(cookie) {
    if(cookie.username && cookie.password) {
         $.post("api/login",{"username":getCookie().username,"password":getCookie().password},function (result) {
            console.log(result);
            if(result.code != 0){
                $(location).attr('href', 'login');
            }else {
                brook_state();
                state_interval = setInterval(brook_state, 2000);
            }
        })
    }else {
        $(location).attr('href', 'login');
    }
}

judgeCookie(getCookie());


function update_ui(brook_state_json) {
    state_jsons = [brook_state_json.brook,brook_state_json.shadowsocks,brook_state_json.socks5];
        if (state_jsons.length == 0)
            return;
            for (var j = 0; j < 3; j++) {
                if ($("#accordion-"+j).length == 0){
                    $("#panel-"+(j+1)).append(accordions[j]);
                    for (var i = 0; i < state_jsons[j].length; i++) {
                        if ($("#port-item"+j+"-"+i).length == 0){
                            var isenabled = 'port';
                            var icon_isenabled = 'icon-enabled';
                            var icon_isenabled_class = 'fui-check-circle';
                            var toogle_item = '<div class="toggle-button-wrapper" style="display: inline-block">' +
                                '<input type="checkbox" class="toggle-button" id="toggle-button'+j+'-'+i+'" ' +
                                'name="switch"><label for="toggle-button'+j+'-'+i+'" class="button-label"><span class="circle"></span>' +
                                '<span class="text on" contenteditable="false">ON</span><span class="text off" contenteditable="false">OFF</span></label></div>';
                            if (state_jsons[j][i].state == 0){
                                isenabled = 'port-red';
                                icon_isenabled = 'icon-disabled';
                                icon_isenabled_class = 'fui-info-circle';
                            }
                            var linked_num_item = '<p class="port-detail-p">连接：'+state_jsons[j][i].linked_num+'</p>';
                            var psw_item = '<p class="port-detail-p">密码：'+state_jsons[j][i].psw+'</p>';

                            var username_item = '<p class="port-detail-p">用户：'+state_jsons[j][i].username+'</p>';
                            var info_items = '';
                            var link_copy_item = '<a href="#myModal4" data-toggle="modal"><span id="copy-link-btn'+j+'-'+i+'" class="fui-link copy-link-btn" ></span></a>';
                            var qr_img_item = '<a href="#myModal5" data-toggle="modal"><span id="qr-img-btn'+j+'-'+i+'" class="fui-image qr-img-btn" ></span></a>';
                            if (j == 2){
                                qr_img_item = '';
                                link_copy_item = '';
                                if (state_jsons[j][i].username == '')
                                    info_items = linked_num_item;
                                else
                                    info_items = username_item + psw_item +linked_num_item;
                            }else if (j == 1){
                                var encode_method_item = '<p class="port-detail-p">加密方式：'+state_jsons[j][i].encode_method+'</p>';
                                info_items = psw_item + encode_method_item + linked_num_item;
                            }else if (j == 0){
                                info_items = psw_item + linked_num_item;
                                qr_img_item = '<a href="#myModal4" data-toggle="modal" style="display: none;"><span id="qr-img-btn'+j+'-'+i+'" class="fui-image qr-img-btn" ></span></a>';
                            }
                            var child_port = '<div class="accordion-group"  id="port-item'+j+'-'+i+'"><div class="accordion-heading '+isenabled+'"><a class=' +
                                '"accordion-toggle collapsed port-a" style="color:white" contenteditable="false" data-parent="#accordion-'+j+'" ' +
                                'data-toggle="collapse" href="#accordion-element'+j+'-'+i+'">端口：'+state_jsons[j][i].port+
                                '<span class="port-info-span">'+state_jsons[j][i].info+'</span>'+'</a>' +
                                '<span id="icon'+j+'-'+i+'" class="'+icon_isenabled_class+' '+icon_isenabled+'"></span></div><div class=' +
                                '"accordion-body collapse" id="accordion-element'+j+'-'+i+'" style="height: 0px;">' +
                                '<p class="port-detail-p">IP：'+state_jsons[j][i].ip+'</p>' +
                                '<p class="port-detail-p">端口：'+state_jsons[j][i].port+'</p>'+info_items+toogle_item+
                                link_copy_item+qr_img_item+'</div></div></div>';
                            $("#accordion-"+j).append(child_port);

                            var copy_link_btn = $("#copy-link-btn"+j+"-"+i);
                            var qr_img_btn = $("#qr-img-btn"+j+"-"+i);
                            copy_link_btn.data('service',state_jsons[j][i]);
                            qr_img_btn.data('service',state_jsons[j][i]);
                            copy_link_btn.click(function () {
                                copyLink($(this).data('service'));
                            });
                            qr_img_btn.click(function () {
                                qrImage($(this).data('service'));
                            });

                            if (state_jsons[j][i].state == 0){
                                $("#toggle-button"+j+"-"+i).prop("checked",false);
                            } else{
                                $("#toggle-button"+j+"-"+i).prop("checked",true);
                            }
                            var this_toggle = $("#toggle-button"+j+"-"+i);
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
                                $.post(api_url,{'username':getCookie().username,'password':getCookie().password,'type':j,'port':state_jsons[j][i].port},function (result) {
                                    state_interval = setInterval(brook_state,2000);
                                    console.log('已改变端口状态');
                                })
                            });
                        }
                    }

                }else {
                    for (var i = 0; i < state_jsons[j].length; i++) {
                        if ($("#port-item"+j+"-"+i).length != 0){
                            $("#port-item"+j+"-"+i).find('a').first().html('端口：'+state_jsons[j][i].port+
                                '<span class="port-info-span">'+state_jsons[j][i].info+'</span>');
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
                            var port_detail_p = $("#accordion-element" + j + "-" + i).children(".port-detail-p");
                            if (j == 2){
                                if (state_jsons[j][i].username != '') {
                                    $(port_detail_p[2]).text("用户：" + state_jsons[j][i].username);
                                    $(port_detail_p[3]).text("密码：" + state_jsons[j][i].psw);
                                    $(port_detail_p[4]).text("连接：" + state_jsons[j][i].linked_num);
                                }else {
                                    $(port_detail_p[2]).text("连接：" + state_jsons[j][i].linked_num);
                                }
                            }else if(j == 1){
                                $(port_detail_p[2]).text("密码："+state_jsons[j][i].psw);
                                $(port_detail_p[3]).text("加密方式："+state_jsons[j][i].encode_method);
                                $(port_detail_p[4]).text("连接："+state_jsons[j][i].linked_num);
                            }else if(j == 0){
                                $(port_detail_p[2]).text("密码："+state_jsons[j][i].psw);
                                $(port_detail_p[3]).text("连接："+state_jsons[j][i].linked_num);
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



