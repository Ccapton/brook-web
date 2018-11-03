
pin=1125;
ad_name='brook-web';
api_path='http://tencent.ccapton.fun/api/webad';

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
