function hideEditUser() {
    $("#edit-user").hide();
}
hideEditUser();

function showEditUser() {
    $("#edit-user").show();
}

function checkLogin() {
    if(getCookie().username && getCookie().password){
        $.get("api/login",{"username":getCookie().username,"password":getCookie().password},function (result) {
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
    $("#username-btn").text(getCookie().username);
    $("#password-btn").text(getCookie().password);
}
showUserInfo();

function submitEditUser() {
    username = $("#username-new").val();
    password = $("#password-new").val();
    if (username == null || username === undefined || username === ''){
        alert('请输入新用户名');
        return
    }
    if (password == null || password === undefined || password === ''){
        alert('请输入新密码');
        return
    }
    $.get('api/resetpsw',{'old_username':getCookie().username,'old_password':getCookie().password,'username':username,
        'password':password},function (result) {
        if (result.code == 0){
             $.cookie("username",username,{ expires: 7 });
             $.cookie("psw",password,{ expires: 7 });
             showUserInfo();
             alert('修改成功');
             $(location).attr('href', '/');
        } else {
            alert('修改失败')
        }
    })
}