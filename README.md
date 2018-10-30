# brook-web
brook程序服务端Web后台管理

<div align="center">
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web.jpeg" height="350" width="400" >  
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web2.jpeg" height="350" width="400" >  
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web3.jpeg" height="350" width="400" >  
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web4.jpeg" height="350" width="400" >  
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web5.jpeg" height="350" width="400" >  
</div>

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
 #### 当出现模块引入错误时，以上命令中的 python 可用 python3 替换后尝试运行

# 默认账号
初始账号 admin 

初始密码 admin
# 说明
**请确保你的服务器（Linux|MacOS）已安装 python、curl**
- **python** 

本项目依赖的语言环境
- **curl** 

install-brook.py程序用到的下载程序

# Docker部署

未完成、待续