
pin=;
ad_name='brook-web';
api_path='';

function getAd(){
    $.get(api_path,{'pin':pin,'ad_name':ad_name},function (result) {
         if (result.code == 0){
             $("#notice").show();
             $("#notice").append(result.data);

         }else {
             console.warn('公告信息获取失败')
         }

     })
}

$(document).ready(function () {
     getAd()
});
