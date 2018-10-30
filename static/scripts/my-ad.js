
pin=1125;
ad_name='brook-web';
api_path='http://111.230.231.107:5001/api/webad';
//api_path='http://192.168.1.106:5001/api/webad';

function getAd(){
    $.get(api_path,{'pin':1125,'ad_name':ad_name},function (result) {
         if (result.code == 0){
             $("#notice").append(result.data);

         }else {
             console.warn('公告信息获取失败')
         }

     })
}

$(document).ready(function () {
     getAd()
});
