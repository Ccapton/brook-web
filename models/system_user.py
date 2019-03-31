#coding=utf-8
#。—————————————————————————————————————————— 
#。                                           
#。  system_user.py                               
#。                                           
#。 @Time    : 2019-03-31 07:53                
#。 @Author  : capton                        
#。 @Software: PyCharm                
#。 @Blog    : http://ccapton.cn              
#。 @Github  : https://github.com/ccapton     
#。 @Email   : chenweibin1125@foxmail.com     
#。__________________________________________

from . import db
from sqlalchemy import text, func


class SystemUser(db.Model):

    __tablename__ = 'sys_user'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), nullable=False, server_default=None)

    password = db.Column(db.String(128), nullable=False, server_default=None)

    is_locked = db.Column(db.Integer, server_default=text("0"))

    create_time = db.Column(db.DateTime, server_default=func.now())

    update_time = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    email = db.Column(db.String(128), server_default=None)