
function hideEditUser() {
    $("#edit-user").hide();
}
hideEditUser();

function autoLogin(auto){

    if(getCookie().username && getCookie().password){
        $.post("api/login",{"username":getCookie().username,"password":getCookie().password},function (result) {
            console.log(result);
            if(result.code == 0){
                $(location).attr('href', '/');
            }else {
                fillUserInfo(getCookie().username,getCookie().password);
                if(!auto){
                    alert("登录失败，请检查用户名和密码");
                }
            }
        })

    }else{
        fillUserInfo(getCookie().username,getCookie().password);
    }
}
autoLogin(true);