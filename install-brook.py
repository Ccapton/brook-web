#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  install-brook.py                               
#。                                           
#。 @Time    : 2018/10/30 下午5:54                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________
from __future__ import print_function
from __future__ import division
import platform
import ssl
import sys
import os

SERVICE_TYPE_BROOK = 0
SERVICE_TYPE_SS = 1
SERVICE_TYPE_SOCKS5 = 2

python_version = sys.version
if python_version.startswith('2.'):
    python_version = '2'
elif python_version.startswith('3.'):
    python_version = '3'


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

# def has_service_start(service_type=SERVICE_TYPE_BROOK):
#     result = os.popen('ps aux | grep brook').read()
#     try:
#         global brook_pid,ss_pid,socks5_pid
#         if service_type == SERVICE_TYPE_BROOK:
#             brook_pid = match_pid(result, service_type)
#         elif service_type == SERVICE_TYPE_SS:
#             ss_pid = match_pid(result, service_type)
#         elif service_type == SERVICE_TYPE_SOCKS5:
#             socks5_pid = match_pid(result, service_type)
#     except Exception:
#         if service_type == SERVICE_TYPE_BROOK:brook_pid = ''
#         elif service_type == SERVICE_TYPE_SS:ss_pid = ''
#         elif service_type == SERVICE_TYPE_SOCKS5:socks5_pid = ''
#     started = False
#     if service_type == SERVICE_TYPE_BROOK:
#         if str(result).find(' servers -l') != -1:
#                 started = True
#     elif service_type == SERVICE_TYPE_SS:
#         if str(result).find(' ssservers -l') != -1:
#                 started = True
#     elif service_type == SERVICE_TYPE_SOCKS5:
#         if str(result).find(' socks5 -l') != -1:
#                 started = True
#     return started
#
# def stop_service(service_type=SERVICE_TYPE_BROOK):
#     has_service_start(service_type)
#     try:
#         global brook_pid,ss_pid
#         if service_type == SERVICE_TYPE_BROOK:
#             if brook_pid != '':
#                 os.system('kill ' + brook_pid)
#         elif service_type == SERVICE_TYPE_SS:
#             if ss_pid != '':
#                 os.system('kill ' + ss_pid)
#         elif service_type == SERVICE_TYPE_SOCKS5:
#             if socks5_pid != '':
#                 os.system('kill ' + socks5_pid)
#     finally:
#         pass
#
# def has_brook_start():
#     return has_service_start(SERVICE_TYPE_BROOK)
#
#
# def stop_brook():
#     has_brook_start()
#     stop_service(SERVICE_TYPE_BROOK)


def download_brook(url,is_exe=False):
    print(' 开始下载brook ' + url)
    command = 'curl -o brook_temp -L ' + url
    code = os.system(command)
    if code != 0:
        print('')
        print(' 下载brook错误，请重新运行本程序')
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
    print(" brook下载完毕!保存在："+os.path.join(sys.path[0],brook_name))


def is_mac():
    brook_list = brook_release_json(match_brook_release_list())
    for brook in brook_list:
        if 'darwin'in brook['name'] :
            download_brook(brook['url'])
            break


def is_linux(arch):
    brook_list = brook_release_json(match_brook_release_list())
    for brook in brook_list:
        if str(brook['name']).endswith('brook') and arch == 'x86_64':
            download_brook(brook['url'])
            break
        elif 'linux' in brook['name']  and arch == 'x86' and '386' in brook['name']:
            download_brook(brook['url'])
            break
        elif 'linux' in brook['name'] and arch in brook['name']:
            download_brook(brook['url'])
            break
        else:
            download_brook(brook_list[0]['url'])
            break


def guest_platform():
    sys_name = platform.system()
    #machine_name = platform.machine().lower()
    if 'Darwin' == sys_name:
        is_mac()
    elif 'Linux' == sys_name:
        arch = os.popen('uname -m').read()
        arch = arch[:len(arch) - 1]
        is_linux(arch)
    elif 'Windows' == sys_name:
        print('暂不支持Windows平台,请期待作者完成')
        #isWindows(is_upgrade,machine_name)
    else:
        print('暂不支持此平台')


if __name__ == "__main__":
    guest_platform()