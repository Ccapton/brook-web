# [brook](https://github.com/txthinking/brook)-web
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
nohup python brook-web.py &
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



