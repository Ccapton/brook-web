#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  iptables.py.py                               
#。                                           
#。 @Time    : 18-11-7 下午7:45                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________
from __future__ import print_function
from __future__ import division
import sys,os




def release_port(port_list):
    for port in port_list:
        tcp_cmd = 'iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport %d -j ACCEPT' % port
        udp_cmd = 'iptables -I INPUT -m state --state NEW -m udp -p udp --dport %d -j ACCEPT' % port
        os.system(tcp_cmd)
        os.system(udp_cmd)

def refuse_port(port_list):
    for port in port_list:
        tcp_cmd = 'iptables -D INPUT -m state --state NEW -m tcp -p tcp --dport %d -j ACCEPT' % port
        udp_cmd = 'iptables -D INPUT -m state --state NEW -m udp -p udp --dport %d -j ACCEPT' % port
        os.system(tcp_cmd)
        os.system(udp_cmd)

# 判断Python执行版本
python_version = sys.version
if python_version.startswith('2.'):
    python_version = '2'
elif python_version.startswith('3.'):
    python_version = '3'

if __name__ == '__main__':
    if python_version == '2':
        reload(sys)  # python3解释器下可能会提示错误，没关系，因为只有python2运行本程序才会走到这步
        sys.setdefaultencoding("utf-8")  # 同上

