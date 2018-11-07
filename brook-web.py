#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  brook-web.py                               
#。                                           
#。 @Time    : 18-10-27 下午4:09                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________
from __future__ import print_function  #  同时兼容python2、Python3
from __future__ import division        #  同时兼容python2、Python3

from flask import Flask,render_template,send_from_directory
from flask_apscheduler import APScheduler
from flask_restful import Api
from flask_restful import Resource,reqparse
import json, os, re, sys
from qr import *
from iptables import release_port,refuse_port

# 判断当前Python执行大版本
python_version = sys.version
if python_version.startswith('2.'):
    python_version = '2'
elif python_version.startswith('3.'):
    python_version = '3'

# 服务进程号
brook_pid = ''
ss_pid = ''
socks5_pid = ''

# 主机ip
host_ip = None

# 模拟同步的标志 当进行配置信息的保存操作(文件写入)时必须对busy进行赋值为True,保存后赋值为False
busy = False

# 服务类型
SERVICE_TYPE_BROOK = 0
SERVICE_TYPE_SS = 1
SERVICE_TYPE_SOCKS5 = 2


# Resource封装类，简化数据参数的配置
class BaseResource(Resource):
    def __init__(self):
        Resource.__init__(self)
        self.parser = reqparse.RequestParser()
        self.add_args()
        self.create_args()

    # 等待子类重写
    def add_args(self):
        pass

    def add_argument(self,*args,**kwargs):
        self.parser.add_argument(*args,**kwargs)

    def create_args(self):
        self.args = self.parser.parse_args()

    def get_arg(self,key):
        return self.args[key]


app = Flask(__name__)
api = Api(app)
default_port = 5000
debug = True


# 默认服务信息（随机端口）
def default_config_json():
    import random
    random_port = random.randint(10000, 30000)
    random_port2 = random.randint(10000, 30000)
    random_port3 = random.randint(10000, 30000)
    while random_port == random_port2:
        random_port2 = random.randint(10000, 30000)
    while random_port3 == random_port2 or random_port == random_port2:
        random_port3 = random.randint(10000, 30000)
    init_config_json = {
        'brook': [{'port': random_port, 'psw': str(random_port), 'state': 0}],
        'shadowsocks': [{'port': random_port2, 'psw': str(random_port2), 'state': 0}],
        'socks5': [{'port': random_port3, 'psw': '', 'username': '', 'state': 0}],
    }
    return init_config_json


# 默认用户信息
def default_user(username="admin", password="admin"):
    return {"user":{"username": username, "password": password}}


# 当前服务实时状态对象
current_brook_state={}


import sys
# 用户信息保存路径
default_userjson_path = os.path.join(sys.path[0],"static/json/user.json")
# 服务信息配置保存路径
config_json_path = os.path.join(sys.path[0],"static/json/brook_state.json")


# 基类json对象格式输出函数
def base_result(msg="", data=None, code=-1):
    return {"msg": msg, "data": data, "code": code}

# 读取json文件，若没有对应文件则创建一个json文件、写入myjson的内容
def load_json(path,myjson):
    if not os.path.exists(path):
        os.system("touch %s" % path)
    f = open(path,'r')
    json_str = f.read()
    f.close()
    if json_str == '':
        with open(path, 'w') as f2:
            f2.write(json.dumps(myjson,ensure_ascii=False))
    f = open(path,'r')
    json_str = f.read()
    config_json = json.loads(json_str)
    f.close()
    return config_json


# 读取服务配置信息
def load_config_json():
    return load_json( config_json_path, default_config_json() )


# 读取用户信息
def load_default_userjson():
    return load_json( default_userjson_path, default_user() )


# 保存当前用户信息
def save_userjson(userjson):
    with open(default_userjson_path,'w') as f:
        f.write(json.dumps(userjson,ensure_ascii=False))


# 保存当前服务配置
def save_config_json(config_json):
    with open(config_json_path,'w') as f:
        f.write(json.dumps(config_json,ensure_ascii=False))


# 输出ico文件
class Favicon(BaseResource):
    def get(self):
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')

# 登录api
class Login(BaseResource):
    def add_args(self):
        self.add_argument('username', type=str, help='Username')
        self.add_argument('password', type=str, help='Password')

    def login(self):
        username = self.get_arg('username')
        password = self.get_arg('password')
        name = load_default_userjson()['user']['username']
        psw = load_default_userjson()['user']['password']
        if name == username and psw == password:
            return base_result(msg="Login Successful!", code=0)
        return base_result(msg="Login failed!")

    def post(self):
        return self.login()

    def get(self):
        return self.login()

# 重置用户信息api
class ResetPsw(BaseResource):
    def add_args(self):
        self.add_argument('old_username',type=str,help='Old Username')
        self.add_argument('old_password',type=str,help='Old Password')
        self.add_argument('username',type=str,help='New Username')
        self.add_argument('password',type=str,help='New Password')
    #
    # code : 1 新用户名为空
    # code : 2 新密码名为空
    # code : -1 旧用户信息不正确
    #
    def reset_psw(self):
        username = self.get_arg('username')
        password = self.get_arg('password')
        old_username = self.get_arg('old_username')
        old_password = self.get_arg('old_password')
        code = 0
        if old_username == load_default_userjson()['user']['username'] and old_password == load_default_userjson()['user']['password']:
            if len(username) <= 0:
                code = 1
                return base_result(msg='Reset User Failed!', code=code)
            if len(password) <= 0:
                code = 2
                return base_result(msg='Reset User Failed!', code=code)
            save_userjson(default_user(username=username,password=password))
            return base_result(msg='Reset User Successful!',code=code)
        return base_result(msg='Reset User Failed!')

    def post(self):
        return self.reset_psw()

    def get(self):
        return self.reset_psw()

# 开启服务api
# code : 3 服务开启失败
# code : 4 操作繁忙
# code : -1 用户信息不正确
#
class StartService(BaseResource):
    def add_args(self):
        self.add_argument('username', type=str, help='Username')
        self.add_argument('password', type=str, help='Password')
        self.add_argument('type', type=int, help='Service Type')
        self.add_argument('port', type=int, help='Port')

    def start_service(self):
        username = self.get_arg('username')
        password = self.get_arg('password')
        if username != load_default_userjson()['user']['username'] or password != load_default_userjson()['user']['password']:
            return base_result(msg='Loin Failed')
        type = self.get_arg('type')
        port = self.get_arg('port')
        if busy:
            return base_result(msg='Server Busy!,Try Again Later.',code=4)

        if type == -1:
            stop_service(SERVICE_TYPE_BROOK)
            result1 = start_service(SERVICE_TYPE_BROOK)
            stop_service(SERVICE_TYPE_SS)
            result2 = start_service(SERVICE_TYPE_SS)
            stop_service(SERVICE_TYPE_SOCKS5)
            result3 = start_service(SERVICE_TYPE_SOCKS5)
            if result1*result2*result3 == 0:
                return base_result(msg='Start All Services Successful!',code=0)
        else:
            if port == -1:
                if type == SERVICE_TYPE_BROOK:
                    stop_service(SERVICE_TYPE_BROOK)
                    result = start_service(SERVICE_TYPE_BROOK)
                elif type == SERVICE_TYPE_SS:
                    stop_service(SERVICE_TYPE_SS)
                    result = start_service(SERVICE_TYPE_SS)
                elif type == SERVICE_TYPE_SOCKS5:
                    stop_service(SERVICE_TYPE_SOCKS5)
                    result = start_service(SERVICE_TYPE_SOCKS5)
                else:
                    result = -1
                if result == 0:
                    return base_result(msg='Start Service Successful!', code=0)
            else:
                if type == SERVICE_TYPE_BROOK:
                    stop_service(SERVICE_TYPE_BROOK,port)
                    result = start_service(SERVICE_TYPE_BROOK,port)
                elif type == SERVICE_TYPE_SS:
                    stop_service(SERVICE_TYPE_SS,port)
                    result = start_service(SERVICE_TYPE_SS,port)
                elif type == SERVICE_TYPE_SOCKS5:
                    stop_service(SERVICE_TYPE_SOCKS5,port)
                    result = start_service(SERVICE_TYPE_SOCKS5,port)
                else:
                    result = -1
                if result == 0:
                    return base_result(msg='Start Service Successful!', code=0)

        return base_result(msg='Failed to Start Service',code=3)

    def get(self):
        return self.start_service()

    def post(self):
        return self.start_service()

# 停止服务api
class StopService(BaseResource):
    def add_args(self):
        self.add_argument('username', type=str, help='Username')
        self.add_argument('password', type=str, help='Password')
        self.add_argument('type', type=int, help='Service Type')
        self.add_argument('port', type=int, help='Port')

    def stop_service(self):
        username = self.get_arg('username')
        password = self.get_arg('password')
        if username != load_default_userjson()['user']['username'] or password != load_default_userjson()['user'][
            'password']:
            return base_result(msg='Loin Failed')
        type = self.get_arg('type')
        port = self.get_arg('port')
        if type == -1:
            stop_service(SERVICE_TYPE_BROOK)
            stop_service(SERVICE_TYPE_SS)
            stop_service(SERVICE_TYPE_SOCKS5)
        else:
            if port == -1:
                if type == SERVICE_TYPE_BROOK:
                    stop_service(SERVICE_TYPE_BROOK,force=True)
                elif type == SERVICE_TYPE_SS:
                    stop_service(SERVICE_TYPE_SS,force=True)
                elif type == SERVICE_TYPE_SOCKS5:
                    stop_service(SERVICE_TYPE_SOCKS5,force=True)
            else:
                if type == SERVICE_TYPE_BROOK:
                    stop_service(SERVICE_TYPE_BROOK, port)
                    start_service(SERVICE_TYPE_BROOK,port=-1)
                elif type == SERVICE_TYPE_SS:
                    stop_service(SERVICE_TYPE_SS, port)
                    start_service(SERVICE_TYPE_SS,port=-1)
                elif type == SERVICE_TYPE_SOCKS5:
                    stop_service(SERVICE_TYPE_SOCKS5, port)
                    start_service(SERVICE_TYPE_SOCKS5,port=-1)
        return base_result(msg='Stop Service Successful!', code=0)

    def get(self):
        return self.stop_service()

    def post(self):
        return self.stop_service()

# 获取服务状态api
class ServiceState(BaseResource):
    def add_args(self):
         pass

    def service_state(self):
        return current_brook_state

    def get(self):
        return base_result(msg='', code=0, data=self.service_state())

    def post(self):
        return base_result(msg='', code=0, data=self.service_state())

# 增加端口api
class AddPort(BaseResource):
    def add_args(self):
        self.add_argument('type',type=int,help='Service Type')
        self.add_argument('port',type=int,help='Service Port')
        self.add_argument('password',type=str,help='Service Password')
        self.add_argument('username',type=str,help='Service Username')
        self.add_argument('info',type=str,help='Service Info')

    def add(self):
        type = self.get_arg('type')
        port = self.get_arg('port')
        password = self.get_arg('password')
        username = self.get_arg('username')
        info = self.get_arg('info')
        if busy:
            return base_result(msg='Server Busy!,Try Again Later.',code=4)
        if is_port_used(port,current_brook_state):
            return base_result(msg='Port has been used!',code=-2)
        if add_port(service_type=type,port=port,psw=password,username=username,info=info):
            return base_result(msg='Add Port Successful!',code=0)
        return base_result(msg='Add Port Failed!',code=-1)

    def get(self):
        return self.add()

    def post(self):
        return self.add()

# 删除端口api
class DelPort(BaseResource):
    def add_args(self):
        self.add_argument('type', type=int, help='Service Type')
        self.add_argument('port', type=int, help='Service Port')
        self.add_argument('password',type=str,help='Service Password')

    def del_port(self):
        type = self.get_arg('type')
        port = self.get_arg('port')
        password = self.get_arg('password')
        if busy:
            return base_result(msg='Server Busy!,Try Again Later.',code=4)
        if del_port(service_type=type,port=port):
            return base_result(msg='Delete Port Successful!',code=0)
        return base_result(msg='Delete Port Failed!',code=-1)

    def get(self):
        return self.del_port()

    def post(self):
        return self.del_port()


# 生成二维码api
class GenerateQrImg(BaseResource):
    def add_args(self):
        self.add_argument('type',type=int,help='Service Type')
        self.add_argument('ip',type=str,help='Service Ip')
        self.add_argument('password',type=str,help='Service Password')
        self.add_argument('port',type=int,help='Service Port')

    def generate_qr_image(self):
        type = self.get_arg('type')
        port = self.get_arg('port')
        password = self.get_arg('password')
        ip = self.get_arg('ip')
        if type == SERVICE_TYPE_SS:
            if port <= 0 :
                return base_result(msg='Port must > 0',code=-2)
            if generate_qr_image(format_ss_link(ip,password,port,python_version),port):
                return base_result('GenerateQrImg successful!',code=0)
        return base_result('GenerateQrImg failed')
    def get(self):
        return self.generate_qr_image()
    def post(self):
        return self.generate_qr_image()


# 检查目标端口是否被占用、根据配置信息判断端口是否已被记录
def is_port_used(port,config_json):
    if port > 0:
        brook_list = config_json['brook']
        ss_list = config_json['shadowsocks']
        socks5_list = config_json['socks5']
        for brook in brook_list:
            if port == brook['port']:
                return True
        for ss in ss_list:
            if port == ss['port']:
                return True
        for socks5 in socks5_list:
            if port == socks5['port']:
                return True
        pi = os.popen('lsof -i:'+str(port))
        res = pi.read()
        pi.close()
        if res != '':
            return True
    return False


# 增加端口
def add_port(username,service_type=SERVICE_TYPE_BROOK, port=-1, psw='',info=''):
    print(service_type,port,psw,username)
    if port == -1 :
        return False
    if username != '' and username != None:
        if psw == '' or psw == None:
            return False
    config_json = load_config_json()
    new_config_json = config_json
    if service_type == SERVICE_TYPE_BROOK:
        config_json['brook'].append({'port': port, 'psw': str(psw),'info':info})
    elif service_type == SERVICE_TYPE_SS:
        config_json['shadowsocks'].append({'port': port, 'psw': str(psw),'info':info})
    elif service_type == SERVICE_TYPE_SOCKS5:
        config_json['socks5'].append({'port': port, 'psw': str(psw), 'username': str(username),'info':info})
    global busy
    busy = True
    save_config_json(new_config_json)
    busy = False
    refuse_port([port])
    release_port([port])
    stop_service(service_type=service_type)
    start_service(service_type=service_type,port=port)
    return True


# 删除端口
def del_port(service_type=SERVICE_TYPE_BROOK,port=-1):
    if port == -1:
        return False
    config_json = load_config_json()
    service_list = [config_json['brook'],config_json['shadowsocks'],config_json['socks5']]
    def get_index(service):
        index = -1
        for i in range(len(service)):
            if service[i]['port'] == port:
                index = i
                break
        return index
    try:
        if service_type == SERVICE_TYPE_BROOK:
            index = get_index(service_list[0])
            if index == -1:return  False
            config_json['brook'].remove(config_json['brook'][index])
            global busy
            busy = True
            save_config_json(config_json)
            busy = False
        elif service_type == SERVICE_TYPE_SS:
            index = get_index(service_list[1])
            if index == -1: return False
            config_json['shadowsocks'].remove(config_json['shadowsocks'][index])
            busy = True
            save_config_json(config_json)
            busy = False
        elif service_type == SERVICE_TYPE_SOCKS5:
            index = get_index(service_list[2])
            if index == -1: return False
            config_json['socks5'].remove(config_json['socks5'][index])
            busy = True
            save_config_json(config_json)
            busy = False
        stop_service(service_type=service_type, port=port)
        start_service(service_type=service_type)
        return True
    except IndexError:
        pass
    return False


# 获取本机实际对外通信的地址
def get_host_ip():
    import socket
    s = None
    ip = '0.0.0.0'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        pass
    finally:
        if s:s.close()
    return ip


# 记录所有服务的状态
def record_all_state():
    #print('record_brook_state')
    record_state(SERVICE_TYPE_BROOK)
    record_state(SERVICE_TYPE_SS)
    record_state(SERVICE_TYPE_SOCKS5)

# 记录服务状态
def record_state(service_type=-1):
    if service_type == SERVICE_TYPE_BROOK:
        service_name = 'brook'
        service_cmomand_name = 'servers'
    elif service_type == SERVICE_TYPE_SS:
        service_name = 'shadowsocks'
        service_cmomand_name = 'ssservers'
    elif service_type == SERVICE_TYPE_SOCKS5:
        service_name = 'socks5'
        service_cmomand_name = 'socks5'
    else:
        return
    pi = os.popen('ps aux|grep brook\ %s' % service_cmomand_name)
    result = pi.read()
    pi.close()
    # 正则匹配查找出当前服务的所有端口
    all_results = re.findall("-l :\d+", result)
    final_results = []
    for node in all_results:
        final_results.append(int(node[4:]))
    #print(final_results)
    config_json = load_config_json()
    global current_brook_state
    current_brook_state[service_name]=[]
    # 判断当前服务所有端口的状态，并保存到全局变量current_brook_state中去
    for server in config_json[service_name]:
        current_server = {}
        if service_type == SERVICE_TYPE_BROOK:
            current_server['link'] = format_brook_link(host_ip,server['psw'],server['port'])
            current_server['qr_img_path'] = os.path.join('static/img/qr', str(server['port']) + '.png')
        elif service_type == SERVICE_TYPE_SS:
            current_server['link'] = format_ss_link(host_ip,server['psw'],server['port'],pv=python_version)
            current_server['qr_img_path'] = os.path.join('static/img/qr',str(server['port'])+'.png')
        if is_linux():
            current_server['linked_num'] = port_linked_num(server['port'])
        else:
            current_server['linked_num'] = 0
        current_server['port'] = server['port']
        current_server['psw'] = server['psw']
        if server['port'] in final_results:
            current_server['state'] = 1
        else:
            current_server['state'] = 0
        if service_type == SERVICE_TYPE_SOCKS5:
            current_server['username'] = server['username']
        current_server['ip'] = host_ip
        if server.get('info'):
            current_server['info'] = server['info']
        else:
            current_server['info'] = ''
        current_brook_state[service_name].append(current_server)

# 开启服务
def start_service(service_type,port=-1,force=False):
    service_name = 'brook'
    if service_type == SERVICE_TYPE_BROOK:
        service_name = 'brook'
    elif service_type == SERVICE_TYPE_SS:
        service_name = 'shadowsocks'
    elif service_type == SERVICE_TYPE_SOCKS5:
        service_name = 'socks5'
    config_json = load_config_json()
    server_list = config_json[service_name]
    server_list_str = ''
    for server in server_list:
        if service_type != SERVICE_TYPE_SOCKS5:
            server_str = '-l ":%d %s" ' % (server['port'], server['psw'])
        else:
            server_str = '-l :%d ' % (server['port'])
        if port != -1:
            if port == server['port']:
                server['state'] = 1
        else:
            if force:
                server['state'] = 1
        if server['state'] != 0:
            server_list_str += server_str
    if has_service_start(service_type):
        print(' %s服务已经开启，不要重复操作' % service_name)
        global busy
        busy = True
        save_config_json(config_json)
        busy = False
        return 0
    else:
        code1 = -2
        if len(server_list_str) != 0:
            # 采用brook程序一次开启多个服务端口的命令
            if service_type == SERVICE_TYPE_BROOK:
                code1 = os.system('nohup ./brook servers ' + server_list_str + '>/dev/null 2>log &')
            elif service_type == SERVICE_TYPE_SS:
                code1 = os.system('nohup ./brook ssservers ' + server_list_str + '>/dev/null 2>log &')
            elif service_type == SERVICE_TYPE_SOCKS5:
                if server_list[0]['username'] != '':
                    user_mode = ' --username ' + server_list[0]['username'] + ' --password ' + server_list[0]['psw']
                else:
                    # 当socks5服务没有设置用户名时，认为这个socks5服务是无账号、无密码服务
                    user_mode = ''
                code1 = os.system(
                    'nohup ./brook socks5 ' + server_list_str + '-i ' + host_ip + user_mode + ' >/dev/null 2>log &')
        if code1 == 0:
            # 这时 brook_pid,ss_pid,socks5_pid未被记录
            has_service_start(service_type)  # 为了记录brook_pid,ss_pid,socks5_pid
            print('%s Service Start Successful' % service_name)
            busy = True
            save_config_json(config_json)
            busy = False
            return 0
        else:
            has_service_start(service_type)
            if code1 == -2:
                pass
            else:
                print(' %s Service Start Failed' % service_name)


# 停止服务
def stop_service(service_type=SERVICE_TYPE_BROOK,port=-1,force=False):
    has_service_start(service_type)
    service_name = 'brook'
    if service_type == SERVICE_TYPE_BROOK:
        service_name = 'brook'
    elif service_type == SERVICE_TYPE_SS:
        service_name = 'shadowsocks'
    elif service_type == SERVICE_TYPE_SOCKS5:
        service_name = 'socks5'
    config_json = load_config_json()
    server_list = config_json[service_name]
    for server in server_list:
        if port != -1:
            if port == server['port']:
                server['state'] = 0
        else:
            if force:
                server['state'] = 0
    global busy
    busy = True
    save_config_json(config_json)
    busy = False
    try:
        global brook_pid,ss_pid
        if service_type == SERVICE_TYPE_BROOK:
            if brook_pid != '':
                os.system('kill ' + brook_pid)
        elif service_type == SERVICE_TYPE_SS:
            if ss_pid != '':
                os.system('kill ' + ss_pid)
        elif service_type == SERVICE_TYPE_SOCKS5:
            if socks5_pid != '':
                os.system('kill ' + socks5_pid)
    finally:
        pass


# 获取端口已连接的ip数量
def port_linked_num(port):
    num=0
    c = "ss state connected sport = :%d -tn|sed '1d'|awk '{print $NF}'|awk -F ':' '{print $(NF-1)}'|sort -u|wc -l" % port
    try:
        pi = os.popen(c)
        num = int(pi.read())
        pi.close()
    except:
        pass
    return num


# 检查服务是否开启（记录对应的服务进程号）
def has_service_start(service_type=SERVICE_TYPE_BROOK):
    pi = os.popen('ps aux | grep brook')
    result = pi.read()
    pi.close()
    try:
        global brook_pid,ss_pid,socks5_pid
        if service_type == SERVICE_TYPE_BROOK:
            brook_pid = match_pid(result, service_type)
        elif service_type == SERVICE_TYPE_SS:
            ss_pid = match_pid(result, service_type)
        elif service_type == SERVICE_TYPE_SOCKS5:
            socks5_pid = match_pid(result, service_type)
    except Exception:
        if service_type == SERVICE_TYPE_BROOK:brook_pid = ''
        elif service_type == SERVICE_TYPE_SS:ss_pid = ''
        elif service_type == SERVICE_TYPE_SOCKS5:socks5_pid = ''
    started = False
    if service_type == SERVICE_TYPE_BROOK:
        if str(result).find(' servers -l') != -1:
                started = True
    elif service_type == SERVICE_TYPE_SS:
        if str(result).find(' ssservers -l') != -1:
                started = True
    elif service_type == SERVICE_TYPE_SOCKS5:
        if str(result).find(' socks5 -l') != -1:
                started = True
    return started


# 正则匹配查找对应服务的进程号
def match_pid(text,service_type=SERVICE_TYPE_BROOK):
    import re
    if service_type == SERVICE_TYPE_BROOK:
        re_result = re.search('.+\s{1}servers -l.+', str(text))
    elif service_type == SERVICE_TYPE_SS:
        re_result = re.search('.+\s{1}ssservers -l.+', str(text))
    else:
        re_result = re.search('.+\s{1}socks5 -l.+', str(text))
    target_line = re_result.group()
    re_result2 = re.search("\S+\s+[\d]+[\s]{0,1}[\d]+\s+\d\.\d", target_line)
    target_line2 = re_result2.group()
    final_result = re.search("[\d]+[\s]{0,1}[\d]+", target_line2)
    return final_result.group()


# 清理后台模式的日志
def clear_log():
    if os.path.exists('nohup.out'):
        with open('nohup.out','w') as f:
            f.write('')
            print('Clear Log')


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': record_all_state,
            #'args': (1, 2),
            'trigger': 'interval',
            'seconds': 2
        },
        {
            'id': 'job2',
            'func': clear_log,
            # 'args': (1, 2),
            'trigger': 'interval',
            'seconds': 300
        }
    ]
    SCHEDULER_API_ENABLED = True


#
# flask-restful的api对象添加路由信息
#
api.add_resource(Favicon,'/favicon.ico')
api.add_resource(Login,'/api/login')
api.add_resource(ResetPsw,'/api/resetpsw')
api.add_resource(StartService,'/api/startservice')
api.add_resource(StopService,'/api/stopservice')
api.add_resource(ServiceState,'/api/servicestate')
api.add_resource(AddPort,'/api/addport')
api.add_resource(DelPort,'/api/delport')
api.add_resource(GenerateQrImg,'/api/generateqrimg')

@app.route("/")
def brook_web():
    title='Brook后台管理'
    return render_template('index.html',title=title)

@app.route("/login")
def user_login():
    title='Brook管理登录'
    return render_template('login.html',title=title)

@app.route("/user")
def user_edit():
    title='Brook后台管理'
    return render_template('user.html',title=title)

@app.route("/test")
def test_html():
    return render_template('test.html')


# 修改默认web端口是否错误的标志
port_error = False


def config_param(port=5000,email='',domain=''):
    global default_port, port_error
    if isinstance(port, int):
        if port > 0:
            default_port = port
        else:
            port_error = True
            print('端口必须大于0')
    else:
        port_error = True
        print('端口号必须为正整数')
    if email == '':
        return
    if domain == '':
        return

# command_tag = 'apt'
# def guest_command_tag():
#     global command_tag
#     system_type = ''
#     content = os.popen('cat /proc/version').read()
#     if 'debian' in content.lower() or 'ubuntu' in content.lower():
#         system_type = 'debian'
#     elif 'centos' in content.lower() or 'red hat' in content.lower() or 'redhat' in content.lower():
#         system_type = 'centos'
#     if system_type == 'debian':
#         command_tag = 'apt-get'
#     elif system_type == 'centos':
#         command_tag = 'yum -y'
# guest_command_tag()


# 定时器服务，用于心跳记录当前服务信息
app.config.from_object(Config())
scheduler = APScheduler()
# it is also possible to enable the API directly
# scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


def is_linux():
    import platform
    sys_name = platform.system()
    # machine_name = platform.machine().lower()
    if 'Darwin' == sys_name:
        return False
    elif 'Linux' == sys_name:
        return True
    return False

if __name__ == '__main__':
    if python_version == '2':
        reload(sys)  # python3解释器下可能会提示错误，没关系，因为只有python2运行本程序才会走到这步
        sys.setdefaultencoding("utf-8")  # 同上

    try:
        larger_ram = 'ulimit -n 51200'
        os.popen(larger_ram).close()
    except:
        pass

    host_ip = get_host_ip()
    import fire
    fire.Fire(config_param)

    if not port_error:
        # import platform
        # sys_name = platform.system()
        # machine_name = platform.machine().lower()
        # if 'Darwin' == sys_name:
        #      pass
        # elif 'Linux' == sys_name:
        #     p = os.popen(command_tag + ' install psmisc')
        #     p.read()
        #     p.close()
        #
        # kill_result = os.system('killall brook')

        # 记录当前运行中的服务，并停止该服务
        if has_service_start(SERVICE_TYPE_BROOK):stop_service(SERVICE_TYPE_BROOK,port=-1)
        if has_service_start(SERVICE_TYPE_SS):stop_service(SERVICE_TYPE_SS,port=-1)
        if has_service_start(SERVICE_TYPE_SOCKS5):stop_service(SERVICE_TYPE_SOCKS5,port=-1)

        if not os.path.exists('brook'):
            print('当前目录下不存在brook程序！请执行 python install-brook.py 后重试')
        else:
            start_service(SERVICE_TYPE_BROOK)
            start_service(SERVICE_TYPE_SS)
            start_service(SERVICE_TYPE_SOCKS5)


        app.run(host=host_ip, port=default_port, debug=debug)

