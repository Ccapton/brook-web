
function getCookie(){ //获取cookie
    var username = $.cookie("username"); //获取cookie中的用户名
    var psw =  $.cookie("psw"); //获取cookie中的登陆密码
    return {"username":username,"password":psw}
}

function setCookie(){ //设置cookie
    var username = $("#login-name").val(); //获取用户名信息
    var psw = $("#login-pass").val(); //获取登陆密码信息

    $.cookie("username",username,{ expires: 7 });//调用jquery.cookie.js中的方法设置cookie中的用户名
    $.cookie("psw",psw,{ expires: 7 });//调用jquery.cookie.js中的方法设置cookie中的登陆密码，并使用base64（jquery.base64.js）进行加密

}

function login(){
    var userName = $('#login-name').val();
    if(userName === undefined || userName === null || userName === ""){
        alert("请输入用户名");
        return;
    }
    var userPass = $('#login-pass').val();
    if(userPass === undefined || userPass === null || userPass === ""){
        alert("请输入密码");
        return;
    }
    setCookie();

    autoLogin(false);

}

function fillUserInfo(username,psw) {
    if(username){//用户名存在的话把用户名填充到用户名文本框
        $("#login-name").val(username);
    }
    if(psw){//密码存在的话把密码填充到密码文本框
        $("#login-pass").val(psw);
    }
}

function logout() {

    if (confirm('确定要退出该账号？')){
        $.cookie('username', '', { expires: -1 });
        $.cookie('psw', '', { expires: -1 });
        $(location).attr('href', 'login');
    }
}


function editUser() {
     $(location).attr('href', 'user');
}