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
from flask import Flask,render_template
from flask_apscheduler import APScheduler
from flask_restful import Api
from flask_restful import Resource,reqparse
import json, os, re

brook_pid = ''
ss_pid = ''
socks5_pid = ''

busy = False

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
ip = "0.0.0.0"
port = 5000
debug = False


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
        'brook': [{'port': random_port, 'psw': str(random_port), 'state':0}],
        'shadowsocks': [{'port': random_port2, 'psw': str(random_port2), 'state':0}],
        'socks5': [{'port': random_port3, 'psw': '', 'username': '', 'state':0}],
    }
    return init_config_json


def default_user(username="admin", password="admin"):
    return {"user":{"username": username, "password": password}}


current_brook_state={}

default_userjson_path = "static/json/user.json"
config_json_path = "static/json/brook_state.json"


def base_result(msg="", data=None, code=-1):
    return {"msg": msg, "data": data, "code": code}


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


def load_config_json():
    return load_json( config_json_path, default_config_json() )


def load_default_userjson():
    return load_json( default_userjson_path, default_user() )


def save_userjson(userjson):
    with open(default_userjson_path,'w') as f:
        f.write(json.dumps(userjson,ensure_ascii=False))


def save_config_json(config_json):
    with open(config_json_path,'w') as f:
        f.write(json.dumps(config_json,ensure_ascii=False))


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

#
# code : 3 服务开启失败
# code : 4 服务开启失败
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


class ServiceState(BaseResource):
    def add_args(self):
         pass

    def service_state(self):
        return current_brook_state

    def get(self):
        return base_result(msg='', code=0, data=self.service_state())

    def post(self):
        return base_result(msg='', code=0, data=self.service_state())


class AddPort(BaseResource):
    def add_args(self):
        self.add_argument('type',type=int,help='Service Type')
        self.add_argument('port',type=int,help='Service Port')
        self.add_argument('password',type=str,help='Service Password')
        self.add_argument('username',type=str,help='Service Username')

    def add(self):
        type = self.get_arg('type')
        port = self.get_arg('port')
        password = self.get_arg('password')
        username = self.get_arg('username')
        if busy:
            return base_result(msg='Server Busy!,Try Again Later.',code=4)
        if is_port_used(port,current_brook_state):
            return base_result(msg='Port has been used!',code=-2)
        if add_port(service_type=type,port=port,psw=password,username=username):
            return base_result(msg='Add Port Successful!',code=0)
        return base_result(msg='Add Port Failed!',code=-1)

    def get(self):
        return self.add()

    def post(self):
        return self.add()


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

api.add_resource(Login,'/api/login')
api.add_resource(ResetPsw,'/api/resetpsw')
api.add_resource(StartService,'/api/startservice')
api.add_resource(StopService,'/api/stopservice')
api.add_resource(ServiceState,'/api/servicestate')
api.add_resource(AddPort,'/api/addport')
api.add_resource(DelPort,'/api/delport')

@app.route("/")
def brook_web():
    title='Brook后台管理'
    return render_template('index.html',title=title)

@app.route("/login")
def user_login():
    title='Brook管理登录'
    return render_template('login.html',title=title)

@app.route("/test")
def test_html():
    return render_template('test.html')


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
        res = os.popen('lsof -i:'+str(port)).read()
        if res != '':
            return True
    return False


def add_port(username,service_type=SERVICE_TYPE_BROOK, port=-1, psw=''):
    print(service_type,port,psw,username)
    if port == -1 :
        return False
    if username != '' and username != None:
        if psw == '' or psw == None:
            return False
    config_json = load_config_json()
    new_config_json = config_json
    if service_type == SERVICE_TYPE_BROOK:
        config_json['brook'].append({'port': port, 'psw': str(psw)})
    elif service_type == SERVICE_TYPE_SS:
        config_json['shadowsocks'].append({'port': port, 'psw': str(psw)})
    elif service_type == SERVICE_TYPE_SOCKS5:
        try:
            config_json['socks5'].append({'port': port, 'psw': str(psw), 'username': str(username)})
        except Exception:
            import json
            socks5_list_json = []
            socks5_list_json.append({'port': port, 'psw': str(psw), 'username': str(username)})
            config_json_str = json.dumps(config_json)
            new_config_json_str = config_json_str[:len(config_json_str) - 1] + ', "socks5": ' + json.dumps(
                socks5_list_json) + '}'
            new_config_json = json.loads(new_config_json_str)
    global busy
    busy = True
    save_config_json(new_config_json)
    busy = False
    stop_service(service_type=service_type)
    start_service(service_type=service_type,port=port)
    return True


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


def get_host_ip():
    import socket
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        if s:s.close()
    return ip


def record_all_state():
    #print('record_brook_state')
    record_state(SERVICE_TYPE_BROOK)
    record_state(SERVICE_TYPE_SS)
    record_state(SERVICE_TYPE_SOCKS5)


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
    result = os.popen('ps aux|grep brook\ %s' % service_cmomand_name).read()
    all_results = re.findall("-l :\d+", result)
    final_results = []
    for node in all_results:
        final_results.append(int(node[4:]))
    #print(final_results)
    config_json = load_config_json()
    global current_brook_state
    current_brook_state[service_name]=[]
    for server in config_json[service_name]:
        current_server = {}
        current_server['port'] = server['port']
        current_server['psw'] = server['psw']
        if server['port'] in final_results:
            current_server['state'] = 1
        else:
            current_server['state'] = 0
        if service_type == SERVICE_TYPE_SOCKS5:
            current_server['username'] = server['username']
        current_server['ip'] = get_host_ip()
        current_brook_state[service_name].append(current_server)


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
            if service_type == SERVICE_TYPE_BROOK:
                code1 = os.system('nohup ./brook servers ' + server_list_str + '>/dev/null 2>log &')
            elif service_type == SERVICE_TYPE_SS:
                code1 = os.system('nohup ./brook ssservers ' + server_list_str + '>/dev/null 2>log &')
            elif service_type == SERVICE_TYPE_SOCKS5:
                if server_list[0]['username'] != '':
                    user_mode = ' --username ' + server_list[0]['username'] + ' --password ' + server_list[0]['psw']
                else:
                    user_mode = ''
                code1 = os.system(
                    'nohup ./brook socks5 ' + server_list_str + '-i ' + get_host_ip() + user_mode + ' >/dev/null 2>log &')
        if code1 == 0:
            # 这时 brook_pid,ss_pid 未被记录
            has_service_start(service_type)  # 为了记录brook_pid,ss_pid
            print('%s服务开启成功！' % service_name)
            busy = True
            save_config_json(config_json)
            busy = False
            return 0
        else:
            has_service_start(service_type)
            if code1 == -2:
                print(' %s节点为空，请添加一些节点' % service_name)
            else:
                print(' %s服务开启失败' % service_name)


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



def has_service_start(service_type=SERVICE_TYPE_BROOK):
    result = os.popen('ps aux | grep brook').read()
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


def clear_log():
    if os.path.exists('nohup.out'):
        with open('nohup.out','w+') as f:
            f.write('')
            print('已清理当前日志')


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




if __name__ == '__main__':
    os.system('killall brook')
    start_service(SERVICE_TYPE_BROOK)
    start_service(SERVICE_TYPE_SS)
    start_service(SERVICE_TYPE_SOCKS5)
    app.config.from_object(Config())

    scheduler = APScheduler()
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    app.run(get_host_ip(),port,debug=debug)