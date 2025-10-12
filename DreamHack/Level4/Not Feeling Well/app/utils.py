from base64 import b64encode
from sql import manager
import re

def file_loader(path):
    try:
        f = open(path, 'rb').read()
        return b64encode(f).decode()

    except FileNotFoundError:
        f = open("/app/static/images/simple.png", "rb").read()
        return b64encode(f).decode()

def info(form) -> dict:

    userinfo = {
        'username':'',
        'profile':'',
        'status_message':''
    }

    for key, value in form.items():
        if key in ['username', 'profile', 'status_message']:
            userinfo[key] = value

    return userinfo

def waf(data, mode):
    if mode == 'path':
        blacklist = ['..', '../']
    
    elif mode == 'sqli':
        blacklist = ['*', ')', ')', "'", '"', '0x']

    for i in blacklist:
        if data.find(i) != -1:
            return True

    return False

def escape(data):
    return data.replace("'", "\\'").replace('"', '\\"')

def reset():
    conn = manager()    
    conn.cursor()

    conn.execute(f"""
        DELETE FROM `users`;
    """)
    conn.execute(f"""
        INSERT INTO `users` VALUES ('guest','guest','/app/static/images/simple.png','not feeling well..'),('male','male','/app/static/images/male.png','My gender is male!'),('female','female','/app//static/images/female.png','My gender is female!');
    """)

    conn.commit()
    conn.close()

def db_integrity(info) -> True or False:
    
    conn = manager()
    conn.cursor()

    conn.execute(f"""
        SELECT `username`, `profile`, `status_message` FROM `users` WHERE `username` = '{info['username']}'
    """)

    res = conn.fetch_all()
    conn.close()
    if res:
        if res[0] != info:
            reset()

            return False
    
    else:
        return True
