#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  qr.py                               
#。                                           
#。 @Time    : 18-11-6 下午2:53                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

def generate_qr_image(content,port):
    try:
        import qrcode, os, sys
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(content)
        qr.make(fit=True)
        img = qr.make_image()
        if not os.path.exists(os.path.join(sys.path[0], 'static/img/qr')):
            os.mkdir(os.path.join(sys.path[0], 'static/img/qr'))
        img.save(os.path.join(sys.path[0], 'static/img/qr', str(port) + '.png'))
    except:
        return False
    return True


def base64encode(content,pv='2'):
    import base64
    if pv == '2':
        return base64.urlsafe_b64encode(content)
    elif pv == '3':
        return base64.urlsafe_b64encode(content.encode(encoding='utf8')).decode()

def base64decode(content,pv='2'):
    import base64
    if pv == '2':
        return base64.urlsafe_b64decode(content)
    elif pv == '3':
        return base64.urlsafe_b64decode(content.encode(encoding='utf8')).decode()


def format_brook_link(ip,psw,port,type='default'):
    return 'brook://'+type+'%20'+ip+":"+str(port)+'%20'+str(psw)


def format_ss_link(ip,psw,port,pv='2'):
    return 'ss://'+base64encode('aes-256-cfb:'+str(psw)+'@'+ip+':'+str(port),pv)

if __name__ == '__main__':
    # 判断当前Python执行大版本
    import sys
    python_version = sys.version
    if python_version.startswith('2.'):
        python_version = '2'
    elif python_version.startswith('3.'):
        python_version = '3'
    if python_version == '2':
        reload(sys)  # python3解释器下可能会提示错误，没关系，因为只有python2运行本程序才会走到这步
        sys.setdefaultencoding("utf-8")  # 同上

    print(format_brook_link('192.168.1.106','123456',10086))
    generate_qr_image(format_ss_link('192.168.1.106','123456',9996,python_version),9996)

