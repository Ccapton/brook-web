# brook-web
### brook程序服务端Web后台管理服务器（Linux|MacOS），基于python、flask、flask-restful

<div align="center">
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web.jpeg" height="350" width="400" >  
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web2.jpeg" height="350" width="400" >  
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web3.jpeg" height="350" width="400" >  
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web4.jpeg" height="350" width="400" >  
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web5.jpeg" height="350" width="400" >  
</div>

# Docker部署

### 1、拉取镜像
``` bash
docker pull capton/brook-web
```
### 2、运行镜像
``` bash
docker run --net=host -d capton/brook-web /bin/bash -c "python brook-web.py 5000"
```
**默认端口5000**
若要修改服务端口，参考：
``` bash
docker run --net=host -d capton/brook-web /bin/bash -c "python brook-web.py 8080"
```

# 常规部署
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

> ### http://111.222.202.34:5000 

### 初始用户信息
初始账号 admin 

初始密码 admin


 
