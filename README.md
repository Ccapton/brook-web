# brook-web
brook程序服务端Web后台管理

# 部署
### 1、打开终端，以root用户登录
### 2、使用 cd 命令 进入brook-web文件夹
### 3、进入virtualenv虚拟环境
``` bash
source venv/bin/activate
``` 
### 4、安装虚拟环境所依赖的库、框架
``` bash
pip install -r requirements.txt
```

### 5、下载brook主体程序到brook-web文件夹内
``` bash
python install-brook.py
```

### 6、开启brook-web服务
前台模式
``` bash
python brook-web.py
```
后台模式
``` bash
nohup python brook-web.py &
```

# 说明
**请确保你的服务器（Linux|MacOS）已安装 python3、curl**
- **python3** 

本项目依赖的语言环境
- **curl** 

install-brook.py程序用到的下载程序