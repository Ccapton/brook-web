# [brook](https://github.com/txthinking/brook)-web
### [brook](https://github.com/txthinking/brook)程序服务端Web后台管理服务器（Linux|MacOS），基于python、flask、flask-restful，配合[caddy](https://github.com/mholt/caddy)反向代理https

<div align="center">      
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web3.jpeg" height="350" width="400" >  
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web4.jpeg" height="350" width="400" >  
<img src="https://raw.githubusercontent.com/Ccapton/brook-web/master/image/brook-web5.jpeg" height="350" width="400" >  
</div>

# Docker部署 
[**docker项目地址**](https://hub.docker.com/r/capton/brook-web/)

### 运行镜像
``` bash
docker run --net=host -d capton/brook-web:stable-1.0 /bin/bash -c "python brook-web.py 5000"
```
**默认端口5000**
若要修改服务端口，参考：
``` bash
docker run --net=host -d capton/brook-web:stable-1.0 /bin/bash -c "python brook-web.py 8080"
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

> ##  http://123.123.123.123:5000 

### 初始用户信息
#### 初始账号 admin 

#### 初始密码 admin


# 开启[caddy](https://github.com/mholt/caddy) 反向代理https 
[参考教程一](https://doub.io/jzzy-2/)

[参考教程二](https://my.oschina.net/diamondfsd/blog/897301)

[caddy官方文档](https://caddyserver.com/docs)

### caddy安装与卸载

- 一键安装caddy脚本
``` bash
wget -N --no-check-certificate https://raw.githubusercontent.com/ToyoDAdoubi/doubi/master/caddy_install.sh && chmod +x caddy_install.sh && bash caddy_install.sh install http.filemanager
```
- 一键卸载caddy脚本
``` bash
wget -N --no-check-certificate https://raw.githubusercontent.com/ToyoDAdoubi/doubi/master/caddy_install.sh && chmod +x caddy_install.sh && bash caddy_install.sh uninstall
```
### caddy配置本项目反向代理https
**注意: 以下对caddy的操作为覆盖性写入动作，如已经有其他caddy项目，请先备份该配置文件**

示例条件：

> - 域名（请一定要成功解析到你的服务器）为 mydomain.fun, 
> - 邮箱为 mydomain@gmail.com
> - 运行brook-web的主机ip为 123.123.123.123
> - 运行brook-web的端口为 5000

- 默认使用80 端口，443为https端口，即 可通过 http://mydomain.fun 或 https://mydomain.fun 访问
``` bash
echo "mydomain.fun {
 gzip
 tls mydomain@gmail.com
 proxy / http://123.123.123.123:5000
}" > /usr/local/caddy/Caddyfile
```
- 假如使用自定义的https，端口为 5001 ，只能通过 https://mydomain.fun:5001 访问 （不会重定向http到https）
``` bash
echo "mydomain.fun:5001 {
 gzip
 tls mydomain@gmail.com
 proxy / http://123.123.123.123:5000
}" > /usr/local/caddy/Caddyfile
```
**请将以上示例条件，根据你的实际情况进行替换**
### 操作caddy服务
**开启caddy服务**
``` bash
service caddy start
```
**关闭caddy服务**
``` bash
service caddy stop
```
**重启caddy服务**
``` bash
service caddy restart
```
**查看caddy服务状态**
``` bash
service caddy start
```
**查看caddy日志**
``` bash
tail -f /tmp/caddy.log
```



