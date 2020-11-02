from flask import Flask,render_template,request,make_response,redirect,url_for,Response
import pymysql
import os
import platform
import datetime
import json

f = open('config.ini', 'r')
config_text = f.read()
f.close()
config_json = json.loads(config_text)
isdebug = config_json['app_debug']
'''
用于调试，在debug模式中会输出
但在运营中不会输出

'''
def log(s):
    if isdebug == 1:
        print(s)