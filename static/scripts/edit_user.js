function hideEditUser() {
    $("#edit-user").hide();
}
hideEditUser();

function showEditUser() {
    $("#edit-user").show();
}

function checkLogin() {
    if(getCookie().username && getCookie().password){
        $.post("api/login",{"username":getCookie().username,"password":getCookie().password},function (result) {
            console.log(result);
            if(result.code == 0){
                 showEditUser();
            }else {
                 hideEditUser();
            }
        })
    } else {
        hideEditUser();
    }
}

checkLogin();

function showUserInfo() {
    $("#username-btn").text($.base64.decode($.base64.decode(getCookie().username).split(splitWord)[1]));
    $("#password-btn").text($.base64.decode($.base64.decode(getCookie().password).split(splitWord)[1]));
}
showUserInfo();

function submitEditUser() {
    let username = $("#username-new").val();
    let password = $("#password-new").val();
    if (username == null || username === undefined || username === ''){
        alert('请输入新用户名');
        return
    }
    if (password == null || password === undefined || password === ''){
        alert('请输入新密码');
        return
    }
    var old_username = $.base64.encode($.base64.encode(salt) + splitWord + $.base64.encode(getCookie().username));
    var old_password = $.base64.encode($.base64.encode(salt) + splitWord + $.base64.encode(getCookie().password));
    var new_username = $.base64.encode($.base64.encode(salt) + splitWord + $.base64.encode(username));
    var new_password = $.base64.encode($.base64.encode(salt) + splitWord + $.base64.encode(password));

    $.post('api/resetpsw', {'old_username':old_username,'old_password':old_password,'username':new_username,
        'password':new_password}, function (result) {
        if (result.code == 0){
             $.cookie("username",new_username,{ expires: 7 });
             $.cookie("password",new_password,{ expires: 7 });
             showUserInfo();
             alert('修改成功');
             $(location).attr('href', '/');
        } else {
            alert('修改失败')
        }
    })
}