# [brook](https://github.com/txthinking/brook)-web ![](https://sonarcloud.io/api/project_badges/measure?project=Ccapton_brook-web&metric=alert_status)[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)


### [brook](https://github.com/txthinking/brook)程序服务端Web后台管理服务器（Linux|MacOS），基于python、flask、flask-restful

### [安全性说明WiKi](https://github.com/Ccapton/brook-web/wiki/%E5%AE%89%E5%85%A8%E6%80%A7%E8%AF%B4%E6%98%8E)
### [点我查看项目WiKi](https://github.com/Ccapton/brook-web/wiki)

<div align="center">
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web.jpeg" height="350" width="400" >        
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web6.png" height="350" width="400" > 
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web7.png" height="350" width="400" > 
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web8.png" height="350" width="400" > 
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web4.jpeg" height="350" width="400" >  
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web5.jpeg" height="350" width="400" >  
</div>

# 方式一、[Docker部署](https://github.com/Ccapton/brook-web/wiki/Docker%E9%83%A8%E7%BD%B2%E6%95%99%E7%A8%8B) 


# 方式二、常规部署
### 1、打开终端，以root用户登录
### 2、使用 cd 命令 进入brook-web文件夹 
### 3、安装所依赖的库、框架
``` bash
pip install -r requirements.txt
```
或 python3环境下的pip3安装
``` bash
pip3 install -r requirements.txt
```
### 4、下载brook主体程序到brook-web文件夹内
``` bash
python install-brook.py
```

### 5、开启brook-web服务
前台模式
``` bash
python brook-web.py
```
后台模式
``` bash
nohup python brook-web.py >/dev/null 2>log &
```

**默认端口5000**
若要修改服务端口，参考：
``` bash
python brook-web.py --port=8080
```
或
``` bash
python brook-web.py 8080
```

### 说明
**请确保你的服务器（Linux|MacOS）已安装 python、curl**
- **python** 

本项目依赖的语言环境
- **curl** 

install-brook.py程序用到的下载程序

# 开始访问

### 请访问 http://主机ip:端口号 例如：

> ##  http://123.123.123.123:5000 

### 初始用户信息
#### 初始账号 admin 

#### 初始密码 admin

# [安全性说明](https://github.com/Ccapton/brook-web/wiki/%E5%AE%89%E5%85%A8%E6%80%A7%E8%AF%B4%E6%98%8E)
# License
``` bash
MIT License

Copyright (c) 2018 Ccapton

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

# 996.ICU License
``` bash
Copyright (c) 2019 ccapton

"Anti 996" License Version 1.0 (Draft)

Permission is hereby granted to any individual or legal entity
obtaining a copy of this licensed work (including the source code,
documentation and/or related items, hereinafter collectively referred
to as the "licensed work"), free of charge, to deal with the licensed
work for any purpose, including without limitation, the rights to use,
reproduce, modify, prepare derivative works of, distribute, publish 
and sublicense the licensed work, subject to the following conditions:

1. The individual or the legal entity must conspicuously display,
without modification, this License and the notice on each redistributed 
or derivative copy of the Licensed Work.

2. The individual or the legal entity must strictly comply with all
applicable laws, regulations, rules and standards of the jurisdiction
relating to labor and employment where the individual is physically
located or where the individual was born or naturalized; or where the
legal entity is registered or is operating (whichever is stricter). In
case that the jurisdiction has no such laws, regulations, rules and
standards or its laws, regulations, rules and standards are
unenforceable, the individual or the legal entity are required to
comply with Core International Labor Standards.

3. The individual or the legal entity shall not induce, metaphor or force
its employee(s), whether full-time or part-time, or its independent
contractor(s), in any methods, to agree in oral or written form, to
directly or indirectly restrict, weaken or relinquish his or her
rights or remedies under such laws, regulations, rules and standards
relating to labor and employment as mentioned above, no matter whether
such written or oral agreement are enforceable under the laws of the
said jurisdiction, nor shall such individual or the legal entity
limit, in any methods, the rights of its employee(s) or independent
contractor(s) from reporting or complaining to the copyright holder or
relevant authorities monitoring the compliance of the license about
its violation(s) of the said license.

THE LICENSED WORK IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN ANY WAY CONNECTION WITH THE
LICENSED WORK OR THE USE OR OTHER DEALINGS IN THE LICENSED WORK.
```
