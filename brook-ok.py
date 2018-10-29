# coding:utf-8
from __future__ import print_function
from __future__ import division
import sys
import os
import platform
import ssl
import random
import imp

imp.reload(sys)

brook_pid = ''
ss_pid = ''
socks5_pid = ''

brook_version = ''

version = '0.9.8'
title = ' Brook服务端配置程序 v%s ' % version
title_c = ' Brook客户端配置程序 v%s ' % version
headline = '-'*10 + title + '-'*10
headline2 = '-'*10 + title_c + '-'*10

config_json_path = 'brook-ok_config.json'


def default_config_json():
    random_port = random.randint(10000, 30000)
    random_port2 = random.randint(10000, 30000)
    random_port3 = random.randint(10000, 30000)
    while random_port == random_port2:
        random_port2 = random.randint(10000, 30000)
    while random_port3 == random_port2 or random_port == random_port2:
        random_port3 = random.randint(10000, 30000)
    init_config_json = {
        'brook': [{'port': random_port, 'psw': str(random_port)}],
        'shadowsocks': [{'port': random_port2, 'psw': str(random_port2)}],
        'socks5': [{'port': random_port3, 'psw': '', 'username': ''}],
    }
    return init_config_json


SERVICE_TYPE_BROOK = 0
SERVICE_TYPE_SS = 1
SERVICE_TYPE_SOCKS5 = 2

INDEX_BACK = '0'

INDEX_BROOK_ACTION = '1'
INDEX_MANAGE_BROOK = '2'
INDEX_CURRENT_CONFIG = '3'
INDEX_UPGRADE = '4'
INDEX_ABOUT = '5'
INDEX_EXIT = '6'
INDEX_SWITCH = '7'

INDEX_BROOK_ACTION_START = '1'
INDEX_BROOK_ACTION_STOP = '2'
INDEX_BROOK_ACTION_RESTART = '3'
INDEX_SS_ACTION_START = '4'
INDEX_SS_ACTION_STOP = '5'
INDEX_SS_ACTION_RESTART = '6'
INDEX_SOCKS5_ACTION_START = '7'
INDEX_SOCKS5_ACTION_STOP = '8'
INDEX_SOCKS5_ACTION_RESTART = '9'
INDEX_BROOK_ACTION_UPGRADE = '10'
INDEX_BROOK_ACTION_DELETE = '11'

INDEX_MANAGE_BROOK_ADDBROOK = '1'
INDEX_MANAGE_BROOK_EDITBROOK = '2'
INDEX_MANAGE_BROOK_DELETEBROOK = '3'
INDEX_MANAGE_BROOK_ADDSS = '4'
INDEX_MANAGE_BROOK_EDITSS = '5'
INDEX_MANAGE_BROOK_DELETESS = '6'
INDEX_MANAGE_BROOK_ADDSOCKS5 = '7'
INDEX_MANAGE_BROOK_EDITSOCKS5 = '8'
INDEX_MANAGE_BROOK_DELETESOCKS5 = '9'

INDEX_MANAGE_BROOK_EDIT_PORT = '1'
INDEX_MANAGE_BROOK_EDIT_PSW = '2'
INDEX_MANAGE_BROOK_EDIT_USERNAME = '3'

'''颜色代码'''
RED = "31m"      # Error message
GREEN = "32m"    # Success message
YELLOW = "33m"   # Warning message
PURPLE = "35m"     # key message
BLUE = "34m"     # Info message

python_version = sys.version
if python_version.startswith('2.'):
    python_version = '2'
elif python_version.startswith('3.'):
    python_version = '3'


def ok_input(promt):
    if python_version == '2':
        try:
            return raw_input(promt)
        except KeyboardInterrupt or ValueError:
            print('')
            exit(0)
    else:
        try:
            return input(promt)
        except KeyboardInterrupt or ValueError:
            print('')
            exit(0)


# 指定颜色打印
def color_print(color,text):
    print("\033[%s%s\033[0m" % (color, text))


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


def guest_platform(is_upgrade=False):
    sys_name = platform.system()
    machine_name = platform.machine().lower()
    if 'Darwin' == sys_name:
        is_mac(is_upgrade)
    elif 'Linux' == sys_name:
        arch = os.popen('uname -m').read()
        arch = arch[:len(arch) - 1]
        is_linux(is_upgrade,arch)
    elif 'Windows' == sys_name:
        print('暂不支持Windows平台,请期待作者完成')
        #isWindows(is_upgrade,machine_name)
    else:
        print('暂不支持此平台')


def is_mac(is_upgrade,):
    brook_list = brook_release_json(match_brook_release_list())
    for brook in brook_list:
        if 'darwin'in brook['name'] :
            download_brook(is_upgrade,brook['url'])
            break


def is_linux(is_upgrade,arch):
    brook_list = brook_release_json(match_brook_release_list())
    for brook in brook_list:
        if str(brook['name']).endswith('brook') and arch == 'x86_64':
            download_brook(is_upgrade,brook['url'])
            break
        elif 'linux' in brook['name']  and arch == 'x86' and '386' in brook['name']:
            download_brook(is_upgrade,brook['url'])
            break
        elif 'linux' in brook['name'] and arch in brook['name']:
            download_brook(is_upgrade,brook['url'])
            break
        else:
            download_brook(is_upgrade,brook_list[0]['url'])
            break


def is_windows(is_upgrade,machine_name):
    brook_list = brook_release_json(match_brook_release_list())
    for brook in brook_list:
        if str(brook['name']).endswith('amd64.exe') and machine_name == 'amd64':
            download_brook(is_upgrade,brook['url'],is_exe=True)
            break
        elif str(brook['name']).endswith('386.exe'):
            download_brook(is_upgrade,brook['url'],is_exe=True)
            break


def get_html_source(url):
    html_source = ''
    context = ssl._create_unverified_context()
    if python_version == '3':
        import urllib.request as req
    else:
        import urllib as req
    try:
        try:
            f = req.urlopen(url, context=context)
            html_source = f.read()
            f.close()
        except KeyboardInterrupt:
            print('\n取消请求')
    except Exception:
        print('请求错误，请重试')
    return html_source


def download_brook(is_upgrade,url,is_exe=False):
    if is_upgrade:
        stop_brook()
    print(' 开始下载brook ' + url)
    command = 'curl -o brook_temp -L ' + url
    code = os.system(command)
    if code != 0:
        print('')
        color_print(RED,' 下载brook错误，请重新运行本程序')
        os.system('rm -rf brook_temp')
        return
    brook_name = 'brook'
    if not is_exe:
        command2 = 'rm -rf brook && mv brook_temp brook'
        os.system(command2)
        command3 = 'chmod +x brook'
        os.system(command3)
    else:
        brook_name = 'brook.exe'
        os.remove(os.path.join(sys.path[0], brook_name))
        os.rename(os.path.join(sys.path[0], 'brook_temp'), os.path.join(sys.path[0], brook_name))
    color_print(PURPLE, " brook下载完毕!保存在："+os.path.join(sys.path[0],brook_name))


def show_state():
    print('当前服务状态：')
    started_service=''
    if has_brook_start():
        started_service += ' Brook'
    if has_shadowsocks_start():
        started_service += ' ShadowSocks'
    if has_socks5_start():
        started_service += ' Socks5'
    if started_service == '':
        color_print(RED,' 服务未运行')
    else:
        color_print(GREEN,started_service+' 运行中')


def main_menu(clear=True):
    print_program_info(clear)
    print_version_info()
    show_state()
    color_print(BLUE, '-' * 30)
    print('')
    color_print(PURPLE, ' 1、管理服务')
    color_print(PURPLE, ' 2、配置节点')
    color_print(PURPLE, ' 3、显示节点')
    print('')
    color_print(PURPLE, ' 4、升级')
    color_print(PURPLE, ' 5、关于')
    color_print(PURPLE, ' 6、退出')
    print('')
    #color_print(PURPLE, ' 7、切换到客户端配置程序')
    #print('')
    color_print(BLUE, '-' * 30)
    option_index = ok_input('输入对应数字（ctrl+c退出）：')
    if  option_index == INDEX_BROOK_ACTION:
        brook_action()
    elif option_index == INDEX_MANAGE_BROOK:
        manage_brook()
    elif option_index == INDEX_CURRENT_CONFIG:
        show_current_config(show_all=True)
    elif option_index == INDEX_UPGRADE:
        upgrade()
    elif option_index == INDEX_EXIT:
        exit(0)
    elif option_index == INDEX_ABOUT:
        os.system('clear')
        about_brook()
    # elif option_index == INDEX_SWITCH:
    #     client_main_menu()
    else:
        main_menu()


def load_config_json():
    import json
    if not os.path.exists(config_json_path):
        os.system("touch %s" % config_json_path)
    f = open(config_json_path,'r')
    json_str = f.read()
    f.close()
    if json_str == '':
        with open(config_json_path, 'w') as f2:
            f2.write(json.dumps(default_config_json(),ensure_ascii=False))
    f = open(config_json_path,'r')
    json_str = f.read()
    config_json = json.loads(json_str)
    f.close()
    return config_json

def save_config_json(config_json):
    import json
    with open(config_json_path,'w') as f:
        f.write(json.dumps(config_json,ensure_ascii=False))


def show_current_config(just_show=False,service_type=SERVICE_TYPE_BROOK,show_all=False):
    print('')
    print('当前配置:')
    print('')
    config_json = load_config_json()
    host_ip = get_host_ip()
    if service_type == SERVICE_TYPE_BROOK or show_all:
        brook_list = config_json['brook']
        print(' 服务类型：Brook')
        for index in range(len(brook_list)):
            brook = brook_list[index]
            print(" (%d)" % (index + 1))
            color_print(GREEN, "----地址：" + host_ip)
            color_print(GREEN, "----端口：" + str(brook['port']))
            color_print(GREEN, "----密码：" + str(brook['psw']))
        print('')
    if service_type == SERVICE_TYPE_SS or show_all:
        ss_list = config_json['shadowsocks']
        print(' 服务类型：ShadowSocks')
        for index in range(len(ss_list)):
            ss = ss_list[index]
            print(" (%d)" % (index + 1))
            color_print(GREEN, "----地址：" + host_ip)
            color_print(GREEN, "----端口：" + str(ss['port']))
            color_print(GREEN, "----密码：" + str(ss['psw']))
            color_print(GREEN, "----加密协议：aes-256-cfb")
        print('')
    if service_type == SERVICE_TYPE_SOCKS5 or show_all:
        try:
            ss_list = config_json['socks5']
            print(' 服务类型：Socks5')
            for index in range(len(ss_list)):
                ss = ss_list[index]
                print(" (%d)" % (index + 1))
                if ss['username'] == '':
                    color_print(YELLOW, " 说明：账号为空则客户端可直接通过地址、端口连接")
                color_print(GREEN, "----地址：" + host_ip)
                color_print(GREEN, "----端口：" + str(ss['port']))
                color_print(GREEN, "----账号：" + str(ss['username']))
                color_print(GREEN, "----密码：" + str(ss['psw']))
            print('')
        except Exception:
            pass
    option_index = INDEX_BACK
    if not just_show:
        option_index = ok_input('输入数字0返回上级 (其他字符退出）：')
        if option_index == INDEX_BACK:
            main_menu()
        else:
            exit(0)


def manage_brook():
    color_print(BLUE, '-' * 30)
    print('')
    color_print(PURPLE, ' 1、添加Brook节点')
    color_print(PURPLE, ' 2、修改Brook节点')
    color_print(PURPLE, ' 3、删除Brook节点')
    print('')
    color_print(PURPLE, ' 4、添加ShadowSocks节点')
    color_print(PURPLE, ' 5、修改ShadowSocks节点')
    color_print(PURPLE, ' 6、删除ShadowSocks节点')
    print('')
    color_print(PURPLE, ' 7、添加socks5节点')
    color_print(PURPLE, ' 8、修改socks5节点')
    color_print(PURPLE, ' 9、删除socks5节点')
    print('')
    color_print(BLUE, '-' * 30)
    option_index = INDEX_BACK
    option_index = ok_input('输入数字0返回上级 (其他字符退出）：')
    if option_index == INDEX_MANAGE_BROOK_ADDBROOK:
        add_port(SERVICE_TYPE_BROOK)
    elif option_index == INDEX_MANAGE_BROOK_EDITBROOK:
        edit_port(SERVICE_TYPE_BROOK)
    elif option_index == INDEX_MANAGE_BROOK_DELETEBROOK:
        del_port(SERVICE_TYPE_BROOK)
    elif option_index == INDEX_MANAGE_BROOK_ADDSS:
        add_port(SERVICE_TYPE_SS)
    elif option_index == INDEX_MANAGE_BROOK_EDITSS:
        edit_port(SERVICE_TYPE_SS)
    elif option_index == INDEX_MANAGE_BROOK_DELETESS:
        del_port(SERVICE_TYPE_SS)
    elif option_index == INDEX_MANAGE_BROOK_ADDSOCKS5:
        add_port(SERVICE_TYPE_SOCKS5)
    elif option_index == INDEX_MANAGE_BROOK_EDITSOCKS5:
        edit_port(SERVICE_TYPE_SOCKS5)
    elif option_index == INDEX_MANAGE_BROOK_DELETESOCKS5:
        del_port(SERVICE_TYPE_SOCKS5)
    elif option_index == INDEX_BACK:
        main_menu()
    else:
        exit(0)


def add_port(service_type=SERVICE_TYPE_BROOK):
    config_json = load_config_json()
    new_config_json = config_json
    try:
        if service_type == SERVICE_TYPE_SOCKS5 and len(config_json['socks5']) >= 1:
            color_print(RED, '只允许一个socks5端口')
            ok_input('回车返回上一级：')
            manage_brook()
            return
    except Exception:
        pass
    username = ''
    if service_type==SERVICE_TYPE_SOCKS5:
        username = ok_input('输入socks5用户名：')
    import random
    random_port = random.randint(10000, 30000)
    port = ok_input('输入一个端口号(回车使用随机端口：%d):' % random_port)
    if port == '':
        port = random_port
    try:
        port = int(port)
    except:
        color_print(RED, '端口号必须为大于1023的数字')
        manage_brook()
    if port <= 1023:
        color_print(RED, '端口号必须为大于1023的数字')
        manage_brook()
    if is_port_used(port, config_json):
        color_print(RED, '端口 ' + str(port) + ' 已被占用了')
        manage_brook()
    else:
        random_psw = random.randint(10000, 30000)
        psw = ok_input('输入密码(回车使用随机密码：%d):' % random_psw)
        if psw == '':
            psw = random_psw
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
                new_config_json_str = config_json_str[:len(config_json_str)-1]+', "socks5": '+json.dumps(socks5_list_json)+'}'
                new_config_json = json.loads(new_config_json_str)

        save_config_json(new_config_json)
        stop_service(service_type)
        start_service(service_type=service_type)
        manage_brook()


def edit_port(service_type=SERVICE_TYPE_BROOK):
    config_json = load_config_json()
    show_current_config(just_show=True,service_type= service_type)
    length = 0
    if service_type == SERVICE_TYPE_BROOK:
        length = len(config_json['brook'])
    elif service_type == SERVICE_TYPE_SS:
        length = len(config_json['shadowsocks'])
    elif service_type == SERVICE_TYPE_SOCKS5:
        try:
            length = len(config_json['socks5'])
        except Exception:
            if length == 0:
                color_print(RED, '当前服务没有节点，请添加一个节点端口吧')
                ok_input('回车返回上一级:')
                manage_brook()
                return
    if length == 0:
        color_print(RED, '当前服务没有节点，请添加一个节点端口吧')
        manage_brook()
        return
    index = ok_input('输入你想要修改的节点序号:')
    try:
        index = int(index)
        if index > length or index <= 0:
            color_print(RED, '节点的序号不在范围内，请查看配置信息进行操作')
            edit_port(service_type)
    except:
        color_print(RED, '节点的序号必须为大于0的数字，请查看配置信息进行操作')
        edit_port(service_type)
    index -= 1
    if service_type == SERVICE_TYPE_BROOK:
        currentService = config_json['brook'][index]
    elif service_type == SERVICE_TYPE_SS:
        currentService = config_json['shadowsocks'][index]
    else:
        currentService = config_json['socks5'][index]
    color_print(BLUE, '-' * 30)
    if service_type == SERVICE_TYPE_BROOK:print('修改Brook端口')
    elif service_type == SERVICE_TYPE_SS:print('修改ShadowSocks端口')
    elif service_type == SERVICE_TYPE_SOCKS5:print('修改Socks5端口')
    #if service_type == SERVICE_TYPE_SOCKS5:
    print('')
    color_print(PURPLE, " 1、修改端口号 (当前" + str(currentService['port']) + ")")
    color_print(PURPLE, " 2、修改密码   (当前" + str(currentService['psw']) + ")")
    if service_type == SERVICE_TYPE_SOCKS5:
        color_print(PURPLE, " 3、修改用户名 (当前"+str(currentService['username']+")"))
    print('')
    color_print(BLUE, '-' * 30)
    option_index = ok_input('选择修改一项 (其他字符退出）：')
    if option_index == INDEX_MANAGE_BROOK_EDIT_PORT:
        import random
        random_port_l = random.randint(10000, 30000)
        new_port = ok_input('输入一个新的端口号(回车使用随机端口：%d):' % random_port_l)
        if new_port == '':
            new_port = random_port_l
        try:
            new_port = int(new_port)
        except:
            color_print(RED, '端口号必须为大于1023的数字')
            edit_port(service_type)
        if new_port <= 1023:
            color_print(RED, '端口号必须为大于1023的数字')
            edit_port(service_type)
        if is_port_used(new_port, config_json):
            color_print(RED, '端口 ' + str(new_port) + ' 已被占用了')
            edit_port(service_type)
            return
        currentService['port'] = new_port
        color_print(YELLOW, '修改中...')
        save_config_json(config_json)
        color_print(GREEN, '修改成功')
        has_service_start(service_type)
        stop_service(service_type)
        start_service(service_type=service_type)
    elif option_index == INDEX_MANAGE_BROOK_EDIT_PSW:
        new_psw = ok_input('输入新密码（回车使用原密码 %s）：' % str(currentService['psw']))
        if new_psw == '':
            new_psw = currentService['psw']
        currentService['psw'] = new_psw
        color_print(YELLOW, '修改中...')
        save_config_json(config_json)
        color_print(GREEN, '修改成功')
        has_service_start(service_type)
        stop_service(service_type)
        start_service(service_type=service_type)
    elif option_index == INDEX_MANAGE_BROOK_EDIT_USERNAME:
        new_username = ok_input('输入新用户名（为空则不使用账号 %s）' % str(currentService['username']))
        currentService['username'] = new_username
        color_print(YELLOW, '修改中...')
        save_config_json(config_json)
        color_print(GREEN, '修改成功')
        has_service_start(service_type)
        stop_service(service_type)
        start_service(service_type=service_type)
    else:
        edit_port(service_type)



def del_port(service_type=SERVICE_TYPE_BROOK):
    config_json = load_config_json()
    show_current_config(just_show=True,service_type=service_type)
    length=0
    if service_type == SERVICE_TYPE_BROOK:
        length = len(config_json['brook'])
    elif service_type == SERVICE_TYPE_SS:
        length = len(config_json['shadowsocks'])
    elif service_type == SERVICE_TYPE_SOCKS5:
        try:
            length = len(config_json['socks5'])
        except Exception:
            if length == 0:
                color_print(RED, '当前服务没有节点，请添加一个节点端口吧')
                ok_input('回车返回上一级:')
                manage_brook()
                return
    if length == 0:
        color_print(RED, '当前服务没有节点，请添加一个节点端口吧')
        manage_brook()
    index = ok_input('输入你想要删除的节点序号:')
    try:
        index = int(index)
        if index > length or index <= 0:
            color_print(RED, '节点的序号不在范围内，请查看配置信息进行操作')
            manage_brook()
    except:
        color_print(RED, '节点的序号必须为大于0的数字，请查看配置信息进行操作')
        manage_brook()
    index -= 1
    try:
        if service_type == SERVICE_TYPE_BROOK:
            config_json['brook'].remove(config_json['brook'][index])
            save_config_json(config_json)
            restart_brook()
        elif service_type == SERVICE_TYPE_SS:
            config_json['shadowsocks'].remove(config_json['shadowsocks'][index])
            save_config_json(config_json)
            restart_shadowsocks()
        elif service_type == SERVICE_TYPE_SOCKS5:
            config_json['socks5'].remove(config_json['socks5'][index])
            save_config_json(config_json)
            restart_socks5()
    except IndexError:
        pass
    manage_brook()


def is_port_used(port,config_json):
    if port > 0:
        brook_list = config_json['brook']
        ss_list = config_json['shadowsocks']
        for brook in brook_list:
            if port == brook['port']:
                return True
        for ss in ss_list:
            if port == ss['port']:
                return True
        res = os.popen('lsof -i:'+str(port)).read()
        if res != '':
            return True
    return False


def brook_action():
    if not check_brook_existed():
        main_menu()
        return
    color_print(BLUE, '-' * 30)
    print('')
    color_print(PURPLE, ' 1、开启brook')
    color_print(PURPLE, ' 2、停止brook')
    color_print(PURPLE, ' 3、重启brook')
    print('')
    color_print(PURPLE, ' 4、开启shadowsocks')
    color_print(PURPLE, ' 5、停止shadowsocks')
    color_print(PURPLE, ' 6、重启shadowsocks')
    print('')
    color_print(PURPLE, ' 7、开启socks5')
    color_print(PURPLE, ' 8、停止socks5')
    color_print(PURPLE, ' 9、重启socks5')
    print('')
    color_print(PURPLE, ' 10、升级brook')
    color_print(PURPLE, ' 11、删除brook')
    print('')
    color_print(BLUE, '-' * 30)
    option_index = ok_input('输入数字0返回上级 (其他字符退出）：')
    if option_index == INDEX_BROOK_ACTION_START:
        print(' 开启brook服务...')
        start_brook(False)
        print_program_info()
        main_menu()
    elif option_index == INDEX_BROOK_ACTION_STOP:
        print(' 停止brook服务...')
        stop_brook()
        color_print(GREEN, ' 已停止brook服务!')
        main_menu(clear=False)
    elif option_index == INDEX_BROOK_ACTION_RESTART:
        print(' 重启brook服务...')
        restart_brook()
    elif option_index == INDEX_SS_ACTION_START:
        print('开启shadowsocks服务...')
        start_shadowsocks(False)
        main_menu()
    elif option_index == INDEX_SS_ACTION_STOP:
        print(' 停止shadowsocks服务...')
        stop_shadowsocks()
        color_print(GREEN, ' 已停止shadowsock服务!')
        main_menu(clear=False)
    elif option_index == INDEX_SS_ACTION_RESTART:
        print(' 重启shadowsocks服务...')
        restart_shadowsocks()
    elif option_index == INDEX_SOCKS5_ACTION_START:
        print('开启socks5服务...')
        start_socks5(state_mode=False)
        main_menu()
    elif option_index == INDEX_SOCKS5_ACTION_STOP:
        print(' 停止socks5服务...')
        stop_socks5()
        color_print(GREEN, ' 已停止shadowsock服务!')
        main_menu(clear=False)
    elif option_index == INDEX_SOCKS5_ACTION_RESTART:
        print(' 重启socks5服务...')
        restart_socks5()
    elif option_index == INDEX_BROOK_ACTION_UPGRADE:
        upgrade_brook()
    elif option_index == INDEX_BROOK_ACTION_DELETE:
        print(' 删除brook程序...')
        confirm = ok_input(' 确定要删除brook吗？(y/n)：')
        if confirm.lower() == 'y':
            stop_service(SERVICE_TYPE_BROOK)
            stop_service(SERVICE_TYPE_SS)
            stop_service(SERVICE_TYPE_SOCKS5)
            os.system('rm -rf brook')
            color_print(GREEN,' 删除brook成功！')
        main_menu(clear=False)
    elif option_index == INDEX_BACK:
        main_menu()


def check_brook_existed():
    if not os.path.exists('brook'):
        confirm = ok_input('brook软件不存在,现在下载？(y/n):')
        if confirm.lower() == 'y' or confirm.lower() == 'yes':
            guest_platform()
            if os.path.exists('brook'):
                return True
        return False
    else:
        return True


def start_brook(state_mode):
    return start_service(state_mode,SERVICE_TYPE_BROOK)


def start_shadowsocks(state_mode):
    return start_service(state_mode,SERVICE_TYPE_SS)


def start_socks5(state_mode):
    return start_service(state_mode,SERVICE_TYPE_SOCKS5)


def stop_brook():
    has_brook_start()
    stop_service(SERVICE_TYPE_BROOK)


def stop_shadowsocks():
    has_shadowsocks_start()
    stop_service(SERVICE_TYPE_SS)


def stop_socks5():
    has_socks5_start()
    stop_service(SERVICE_TYPE_SOCKS5)


def restart_brook(state_mode=False):
    stop_brook()
    start_brook(state_mode)


def restart_shadowsocks(state_mode=False):
    stop_shadowsocks()
    start_shadowsocks(state_mode)


def restart_socks5(state_mode=False):
    stop_socks5()
    start_socks5(state_mode)


def has_brook_start():
    return has_service_start(SERVICE_TYPE_BROOK)


def has_shadowsocks_start():
    return has_service_start(SERVICE_TYPE_SS)


def has_socks5_start():
    return has_service_start(SERVICE_TYPE_SOCKS5)


def start_service(state_mode=False,service_type=SERVICE_TYPE_BROOK):
    service_name = 'brook'
    if service_type == SERVICE_TYPE_BROOK:
        service_name = 'brook'
    elif service_type == SERVICE_TYPE_SS:
        service_name = 'shadowsocks'
    elif service_type == SERVICE_TYPE_SOCKS5:
        service_name = 'socks5'
    try:
        load_config_json()[service_name]
    except Exception:
        color_print(RED,'当前服务开启错误')
        ok_input('回车返回上级：')
        brook_action()
        return
    server_list = load_config_json()[service_name]
    server_list_str = ''
    for server in server_list:
        if service_type != SERVICE_TYPE_SOCKS5:
            server_str = '-l ":%d %s" ' % (server['port'], server['psw'])
        else:
            server_str = '-l :%d ' % (server['port'])
        server_list_str += server_str
    if not state_mode:
        if has_service_start(service_type):
            color_print(YELLOW, ' %s服务已经开启，不要重复操作' % service_name)
            show_current_config(service_type=service_type)
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
                        user_mode = ' --username '+server_list[0]['username']+' --password '+server_list[0]['psw']
                    else:
                        user_mode = ''
                    code1 = os.system('nohup ./brook socks5 ' + server_list_str +'-i '+get_host_ip() + user_mode + ' >/dev/null 2>log &')
            if code1 == 0:
                # 这时 brook_pid,ss_pid 未被记录
                has_service_start(service_type)  # 为了记录brook_pid,ss_pid
                color_print(GREEN, '%s服务开启成功！' % service_name)
                show_current_config(service_type=service_type)
                return 0
            else:
                has_service_start(service_type)
                if code1 != 0:
                    color_print(RED, ' %s服务开启失败' % service_name)
                else:
                    color_print(GREEN, ' %s服务开启成功' % service_name)
                if code1 == -2:
                    color_print(RED, ' %s节点为空，请添加一些节点' % service_name)
    else:
        if has_service_start(service_type) :
            return 1
        else:
            return 0
    return 1


def stop_all_service():
    has_socks5_start()
    has_shadowsocks_start()
    has_brook_start()
    stop_socks5()
    stop_shadowsocks()
    stop_brook()



def stop_service(service_type=SERVICE_TYPE_BROOK):
    has_service_start(service_type)
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


def print_program_info(clear=True,is_server=True):
    if clear:
        os.system('clear')
    if is_server:
        text=headline
    else:
        text=headline2
    color_print(color=BLUE,text=text)


def print_version_info():
    if not os.path.exists('brook'):
        return
    print('当前Brook版本:')
    v = os.popen('./brook -version').read()
    color_print(GREEN, ' '+str(v).rstrip())
    global brook_version
    brook_version = str(v).rstrip().split(' ')[2]


def get_current_brook_version():
    v = os.popen('./brook -version').read()
    current_version = str(v).rstrip().split(' ')[2]
    return current_version


def upgrade_brook():
    global brook_version
    if brook_version == '':
        brook_version = get_current_brook_version()
    print('当前brook版本 v'+brook_version)
    print('获取最新brook版本中...')
    latest_version = get_brook_latest_version()
    if brook_version != '' and (brook_version in latest_version):
        color_print(YELLOW,'brook已是最新版本')
        confirm = ok_input('回车返回上级:')
        brook_action()
    elif brook_version != '' and (brook_version not in latest_version):
        color_print(YELLOW, '有brook新版本'+latest_version)
        confirm = ok_input('确定升级（y/n）:')
        if confirm.lower() == 'y' or confirm.lower() == 'yes' or confirm.lower() == 'ye':
            stop_brook()
            stop_shadowsocks()
            print('brook升级中...')
            guest_platform(is_upgrade=True)
        else:
            brook_action()


def download_latest_version(url):
    if os.system('curl -o brook-ok_temp.py -L %s' % url) == 0:
        if os.system('rm -rf brook-ok.py') == 0:
            if os.system('mv brook-ok_temp.py brook-ok.py') == 0:
                color_print(GREEN, '更新成功！')
                rest_time = 3
                color_print(YELLOW, '%ds后自动重启brook-ok.py' % rest_time)
                import time
                time.sleep(rest_time)
                if os.system('python brook-ok.py') == 0:
                    return
    color_print(RED, '更新出错,请重试')


def match_latest_url(html_source):
    try:
        import re
        if python_version == '2':
            source = html_source
        else:
            source = html_source.decode(encoding='utf-8')
        result = re.search('https://github.com/Ccapton/brook-ok/releases/download/.+/brook-ok\.py', source).group()
    except Exception:
        result = ''
    return result


def get_latest_version():
    import re
    url = 'https://raw.githubusercontent.com/Ccapton/brook-ok/master/README.md'
    if python_version == '2':
        source = get_html_source(url)
    else:
        source = get_html_source(url).decode(encoding='utf-8')
    version_str = re.search('#+\s{1,}\[v\S+\]', source).group()
    version = re.search("[\d\.]+", version_str).group()
    return version


def get_brook_latest_version():
    import re
    url = 'https://raw.githubusercontent.com/txthinking/brook/master/README.md'
    if python_version == '2':
        source = get_html_source(url)
    else:
        source = get_html_source(url).decode(encoding='utf-8')
    version_str = re.search('#+\s{1,}.{0,}v\d+', source).group()
    version_num = re.search('20\d+', version_str).group()
    return version_num


# 获取brook其github主页的所有release下载链接
def match_brook_release_list():
    url = 'https://github.com/txthinking/brook'
    if python_version == '2':
        source = get_html_source(url)
    else:
        source = get_html_source(url).decode(encoding='utf-8')
    import re
    result = re.findall('https://github.com/txthinking/brook/releases/download/.+"', source)
    link_list = []
    for raw_link in result:
        link = raw_link[:len(raw_link) - 1]
        link_list.append(link)
    return link_list


def brook_release_json(releaseLinkList):
    brook_release_list = []
    import os
    for link in releaseLinkList:
        released = {}
        released['url']=link
        released['name']=os.path.basename(link)
        brook_release_list.append(released)
    return brook_release_list


def upgrade():
    print(' 当前程序版本 v'+version)
    print(' 获取最新版本中...')
    url = 'https://raw.githubusercontent.com/Ccapton/brook-ok/master/README.md'
    latest_version = get_latest_version()
    if version in latest_version:
        color_print(YELLOW,'当前版本 v%s 已是最新版本！' % version)
        main_menu(clear=False)
    else:
        latest_url = ''
        try:
            latest_url = match_latest_url(get_html_source(url))
            if latest_url != '':
                color_print(YELLOW, '有新版本 ' + latest_version)
                confirm = ok_input('确定升级brook-ok（y/n）:')
                if confirm.lower() == 'y' or confirm.lower() == 'yes' or confirm.lower() == 'ye':
                    print('brook-ok升级中...')
                    download_latest_version(latest_url)
                else:
                    main_menu()
            else:
                color_print(YELLOW, '当前版本 v%s 已是最新版本！' % version)
                main_menu(clear=False)
        except KeyboardInterrupt:
            print('')
            main_menu()
        except Exception:
            color_print(RED,'连接失败，请重试')
            main_menu()


def about_brook():
    brook_url = 'https://github.com/txthinking/brook'
    brook_ok_url = 'https://github.com/ccapton/brook-ok'
    about = '\n    brook是一个跨平台(Linux/MacOS/Windows/Android/iOS)代理 / Vpn软件' \
            '\n一个墙外的服务器利用Brook程序开启brook或shadowsocks服务，墙内的主机利用brook程序开启客户端连接到brook服务器，' \
            '利用加密的数据，达到科学上网的目的。 \n'
    about2 = '\n   brook-ok 为了方便管理、开启brook、shadowsocks、socks5服务而生 !>_<! '
    color_print(BLUE, '-' * 30)
    print('')
    color_print(YELLOW, '----关于brook ')
    print(about)
    print('\nbrook项目地址：'+brook_url+'\n')
    color_print(YELLOW, '----关于brook-ok ')
    print(about2)
    print('\nbrook-ok项目地址：'+brook_ok_url+'\n')
    color_print(BLUE, '-' * 30)
    ok_input('回车返回上级：')
    print_program_info()
    print_version_info()
    main_menu()


def client_main_menu(clear=True):
    print_program_info(clear,is_server=False)
    print_version_info()
    show_state()
    color_print(BLUE, '-' * 30)
    print('')
    color_print(PURPLE, ' 1、连接服务器')
    color_print(PURPLE, ' 2、配置节点')
    color_print(PURPLE, ' 3、显示节点')
    print('')
    color_print(PURPLE, ' 4、升级')
    color_print(PURPLE, ' 5、关于')
    color_print(PURPLE, ' 6、退出')
    print('')
    color_print(PURPLE, ' 7、切换到服务端配置程序')
    print('')
    color_print(BLUE, '-' * 30)
    option_index = ok_input('输入对应数字（ctrl+c退出）：')
    if option_index == INDEX_BROOK_ACTION:
        pass
    elif option_index == INDEX_MANAGE_BROOK:
        pass
    elif option_index == INDEX_CURRENT_CONFIG:
        pass
    elif option_index == INDEX_UPGRADE:
        upgrade()
    elif option_index == INDEX_EXIT:
        exit(0)
    elif option_index == INDEX_ABOUT:
        os.system('clear')
        about_brook()
    elif option_index == INDEX_SWITCH:
        main_menu()
    else:
        client_main_menu()


def connect_to_server():
    pass


def connect_to_brook():
    pass


def connect_to_ss():
    pass


def show_current_client_config(just_show=False,show_brook=True,show_ss=True):
    print('')
    print('当前配置:')
    print('')
    config_json = load_config_json()
    host_ip = get_host_ip()
    if show_brook:
        brook_list = config_json['brook']
        print(' 服务类型：Brook')
        for index in range(len(brook_list)):
            brook = brook_list[index]
            print(" (%d)" % (index + 1))
            color_print(GREEN, "----地址：" + host_ip)
            color_print(GREEN, "----端口：" + str(brook['port']))
            color_print(GREEN, "----密码：" + str(brook['psw']))
        print('')
    if show_ss:
        ss_list = config_json['shadowsocks']
        print(' 服务类型：ShadowSocks')
        for index in range(len(ss_list)):
            ss = ss_list[index]
            print(" (%d)" % (index + 1))
            color_print(GREEN, "----地址：" + host_ip)
            color_print(GREEN, "----端口：" + str(ss['port']))
            color_print(GREEN, "----密码：" + str(ss['psw']))
            color_print(GREEN, "----加密协议：aes-256-cfb")
        print('')
    option_index = INDEX_BACK
    if not just_show:
        option_index = ok_input('输入数字0返回上级 (其他字符退出）：')
        if option_index == INDEX_BACK:
            main_menu()
        else:
            exit(0)


def entry():
    main_menu()


if __name__ == "__main__":
    entry()

