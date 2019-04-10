function getCookie() { //获取cookie
    var username = $.cookie("username"); //获取cookie中的用户名
    var password = $.cookie("password"); //获取cookie中的登陆密码
    return {"username": username, "password": password}
}

function setCookie() { //设置cookie
    var username = $.base64.encode($.base64.encode(salt) + splitWord + $.base64.encode($("#login-name").val())); //获取用户名信息
    var password = $.base64.encode($.base64.encode(salt) + splitWord + $.base64.encode($("#login-pass").val())); //获取登陆密码信息

    $.cookie("username", username, {expires: 7});//调用jquery.cookie.js中的方法设置cookie中的用户名
    $.cookie("password", password, {expires: 7});//调用jquery.cookie.js中的方法设置cookie中的登陆密码，并使用base64（jquery.base64.js）进行加密

}

function login() {
    var userName = $('#login-name').val();
    if (userName === undefined || userName === null || userName === "") {
        alert("请输入用户名");
        return;
    }
    var userPass = $('#login-pass').val();
    if (userPass === undefined || userPass === null || userPass === "") {
        alert("请输入密码");
        return;
    }
    setCookie();

    autoLogin(false);

}

function fillUserInfo(username, psw) {
    if (username) {//用户名存在的话把用户名填充到用户名文本框
        $("#login-name").val($.base64.decode($.base64.decode(getCookie().username).split(splitWord)[1]));
    }
    if (psw) {//密码存在的话把密码填充到密码文本框
        $("#login-pass").val($.base64.decode($.base64.decode(getCookie().password).split(splitWord)[1]));
    }
}

function logout() {

    if (confirm('确定要退出该账号？')) {
        $.cookie('username', '', {expires: -1});
        $.cookie('password', '', {expires: -1});
        $(location).attr('href', 'login');
    }
}


function editUser() {
    $(location).attr('href', 'user');
}