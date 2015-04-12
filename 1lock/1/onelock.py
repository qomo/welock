# -*- coding: utf-8 -*-
# import logging
import tornado
import sae.const
import _mysql
from tornado import database
from wechat_sdk.basic import WechatBasic

TOKEN = "qomoliao1lock"
APPID = "wx6fefc0f9ac81ef0d"
APPSECRET = "997000a1d68f3b985c1ac235c5c716bb"

MENU = '''欢迎关注QomoLiao的微信公众号，这是一个自娱自乐的微信项目。回复如下按键则可以获得相应回复:
-----------------------------------
0: 帮助（help）
1: 芝麻开门（unlock）
2: 查看密匙（mykey）
3: 关于微信锁（wechatlock）
9: 关于QomoLiao：http://qomo.sinaapp.com/about-me/
'''



MYSQL_DB = sae.const.MYSQL_DB
MYSQL_USER = sae.const.MYSQL_USER
MYSQL_PASS = sae.const.MYSQL_PASS
MYSQL_HOST_M = sae.const.MYSQL_HOST
MYSQL_HOST_S = sae.const.MYSQL_HOST_S
MYSQL_PORT = sae.const.MYSQL_PORT

wechat = WechatBasic(token=TOKEN, appid=APPID, appsecret=APPSECRET)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # 服务器配置
        # TOKEN = "qomoliao1lock"
        self.signature = self.get_argument('signature')
        self.timestamp = self.get_argument('timestamp')
        self.nonce = self.get_argument('nonce')
        self.echostr = self.get_argument('echostr')

        # wechat = WechatBasic(token=TOKEN)
        if wechat.check_signature(signature=self.signature, timestamp=self.timestamp,nonce=self.nonce):
        	self.write(self.echostr)
        else:
        	self.write("ERROR")

    def post(self):
        # 从request中获取请求文本
        body_text = self.request.body
        # print "DEBUG:", body_text, "\n"
        wechat.parse_data(body_text)
        message = wechat.get_message()

        response = None
        # 根据message类型做相应处理
        if message.type == 'text':
            # 文本型
            if (message.content in [u'0', u'帮助', u'help']):
                response = wechat.response_text(MENU)
            elif (message.content == u'1'):
                lockname = 'wechatlock'
                chekey = message.source
                lock = Lock(lockname=lockname, key=chekey)
                lock.unlock()
                response = wechat.response_text("锁开了")
            elif (message.content in [u'2', u'密匙', u'mykey']):
                response = wechat.response_text(message.source)
            elif (message.content in [u'3', u'微信锁', u'wechatlock']):
                response = wechat.response_news([
                {
                    'title': u'【一个想法】微信门锁',
                    'description': u'回到家门口，点击微信公众号的开门按钮，然后收到服务器发回的随机开锁二维码。将二维码放到摄像头前，门锁打开，该二维码报废。或者60s未使用该二维码，自动报废。',
                    'picurl': u'http://mmbiz.qpic.cn/mmbiz/AMRLGdgw8ZJc9xW8JDMg1uMG50kXu9ugfHv0ibWNibliaodrMfeB6BCXnhAeyKXvNYKxH5pF7xdq2Lm0hnyiaHaGibQ/0?tp=webp',
                    'url': u'http://mp.weixin.qq.com/s?__biz=MjM5NTMwMjUyNA==&mid=207774891&idx=1&sn=c5856d8fe2726115edde9b93ef4ab79f&scene=1&key=e50c042086dc971705246a61f80f1195f3361975e277497b71819205f068b5093abbb14d4705710de53ea062902111aa&ascene=0&uin=ODYyOTU2NjU%3D&devicetype=iMac+MacBookAir6%2C2+OSX+OSX+10.10.1+build(14B25)&version=11020012&pass_ticket=k%2BCul8bwJ1vOPGw0hvShNVT3EFjEATsa7teQqgQYSO0%3D',
                }
                ])
            elif (message.content in [u'9', u'aboutme', u'qomolioa']):
                response = wechat.response_news([
                    {
                        'title': u'About me',
                        'description': u'我的个人信息页',
                        'picurl': u'http://qomo-wordpress.stor.sinaapp.com/uploads/2013/04/IMAG0301.jpg',
                        'url': u'http://qomo.sinaapp.com/about-me/'
                    }
                    ])
            else:
                cmd = message.content.split()
                if cmd[0] == "addlock":
                    # print "ADD LOCK"
                    lockname = cmd[1]
                    adminkey = cmd[2]
                    chekey = message.source
                    rt = addlock(lockname, adminkey, chekey)
                    response = wechat.response_text(rt)
                elif cmd[0] == "dellock":
                    # print "DEL LOCK"
                    lockname = cmd[1]
                    chekey = message.source
                    rt = dellock(lockname, chekey)
                    response = wechat.response_text(rt)
                elif cmd[0] == "addkey":
                    # print "ADD KEY"
                    lockname = cmd[1]
                    key = cmd[2]
                    chekey = message.source
                    lock = Lock(lockname=lockname, key=chekey)
                    rt = lock.addkey(key)
                    response = wechat.response_text(rt)
                elif cmd[0] == "delkey":
                    # print "DEL KEY"
                    lockname = cmd[1]
                    key = cmd[2]
                    chekey = message.source
                    lock = Lock(lockname=lockname, key=chekey)
                    rt = lock.delkey(key)
                    response = wechat.response_text(rt)
                elif cmd[0] == "state":
                    lockname = cmd[1]
                    chekey = message.source
                    lock = Lock(lockname=lockname, key=chekey)
                    if lock.islocked():
                        rt = "门锁着"
                    else:
                        rt = "门开着"
                    response = wechat.response_text(rt)
                elif cmd[0] == "lock":
                    lockname = cmd[1]
                    chekey = message.source
                    lock = Lock(lockname=lockname, key=chekey)
                    lock.lock()
                    response = wechat.response_text("锁上了")
                elif cmd[0] == "unlock":
                    lockname = cmd[1]
                    chekey = message.source
                    lock = Lock(lockname=lockname, key=chekey)
                    lock.unlock()
                    response = wechat.response_text("锁开了")
                else:
                    response = wechat.response_text("test")
        # elif message.type == 'image':
        # 	response = wechat.response_text(u'图片')
        else:
            response = wechat.response_text(MENU)

		# 现在直接将 response 变量内容直接作为 HTTP Response 响应微信服务器即可，此处为了演示返回内容，直接将响应进行输出
        self.write(response)

class Lock():
    """每一个锁都需要一个key来使用"""
    def __init__(self, key, lockname="wechatlock"):
        self.mdb = database.Connection("%s:%s"%(MYSQL_HOST_M,str(MYSQL_PORT)), MYSQL_DB,MYSQL_USER, MYSQL_PASS)
        self.__lockname = lockname
        self.__key = key        # 使用锁需要一个key，根据key的权限不同，可以使用不同的操作，管理者key可以进行所以操作，普通key只能进行普通操作
        self.__adminkey = self.get_admin_key()  # 该锁的管理者key
        self.__state = self.islocked()


    def __del__(self):
        self.mdb.close()


    def islocked(self):
        return bool(self.mdb.get("SELECT `state` FROM `lock` WHERE `lockname` = %s", self.__lockname)['state'])


    def unlock(self):
        if self.check_key():
            self.mdb.execute("UPDATE `lock` SET `state` = %s WHERE `lockname` = %s", False, self.__lockname)
            return True
        else:
            return False

    def lock(self):
        if self.check_key():
            self.mdb.execute("UPDATE `lock` SET `state` = %s WHERE `lockname` = %s", True, self.__lockname)
            return True
        else:
            return False

    def check_key(self, key = ""):
        if key=="":
            # 检查调用者self.__key是否在钥匙列表里
            key = self.__key
        # 检查key是否在名为self.__lockname的钥匙列表里
        # print "CHECK KEY:"+key
        if self.mdb.get("SELECT `lockname` FROM `lockkeypair` WHERE `lockname` = %s AND `key` = %s", self.__lockname, key):
            return True
        else:
            return False

    def addkey(self, addedkey):
        # 需要锁调用者self.__key是管理者key
        if self.__adminkey == self.__key:
            # 如果chekey是该锁的管理者，执行添加操作
            self.mdb._ensure_connected()
            if self.check_key(addedkey):
                return u'他本来就能够开这个锁'
            else:
                query = "INSERT INTO `lockkeypair` (`lockname`, `key`) values(%s,%s)"
                self.mdb._ensure_connected()
                self.mdb.execute(query, self.__lockname, addedkey)
                return u'成功将该钥匙添加到该锁的钥匙列表'
        else:
            return u'你不是该锁的管理者'

    def delkey(self, delkey):
        # 需要锁调用者self.__key是管理者key
        if self.__adminkey == self.__key:
            # 如果chekey是该锁的管理者，执行删除操作
            self.mdb._ensure_connected()
            if self.check_key(delkey):
                self.mdb.execute("DELETE FROM `lockkeypair` WHERE `lockname` = %s AND `key` = %s", self.__lockname, delkey)
                return u'删除成功'
            else:
                return u'要删除的密匙本来就没有开锁权限'
        else:
            return u'你不是该锁的管理者'

    def get_admin_key(self):
        return (self.mdb.get("SELECT `admin` FROM `lock` WHERE `lockname` = %s", self.__lockname))['admin']



def addlock(lockname, adminkey, bosskey):
    # 只有qomoliao有权添加锁
    if check_boss(bosskey):
        mdb = database.Connection("%s:%s"%(MYSQL_HOST_M,str(MYSQL_PORT)), MYSQL_DB,MYSQL_USER, MYSQL_PASS)
        mdb._ensure_connected()
        if mdb.get("SELECT `lockname` FROM `lock` WHERE `lockname` = %s", lockname):
            rt = u'这个锁名已被使用'
        else:
            query = "INSERT INTO `lock` (`lockname`,`admin`,`state`) values(%s,%s,%s)"
            mdb._ensure_connected()
            mdb.execute(query, lockname, adminkey, True)
            # 将管理员密匙添加到锁密匙列表
            lock = Lock(lockname)
            lock.addkey(adminkey, adminkey)
            rt = u'成功添加锁和管理员'
        mdb.close()
        return rt
    else:
        return u'你不是我的大boss，我不能接受这个指令'


def dellock(lockname, bosskey):
    if check_boss(bosskey):
        mdb = database.Connection("%s:%s"%(MYSQL_HOST_M,str(MYSQL_PORT)), MYSQL_DB,MYSQL_USER, MYSQL_PASS)
        mdb._ensure_connected()
        if mdb.get("SELECT `lockname` FROM `lock` WHERE `lockname` = %s", lockname):
            # 如果锁存在，删除锁关联的密匙；再删除锁
            mdb._ensure_connected()
            mdb.execute("DELETE FROM `lockkeypair` WHERE `lockname` = %s", lockname)
            mdb.execute("DELETE FROM `lock` WHERE `lockname` = %s LIMIT 1", lockname)
            rt = u'成功删除锁'
        else:
            rt = u'不存在这个锁'
        mdb.close()
        return rt
    else:
        return u'你不是我的大boss，我不能接受这个指令'


def check_boss(bosskey):
    return bosskey=="ofGrFjt2u8N0V2oHVm7zPF90ECx4"

class Qrcode(tornado.web.RequestHandler):
    """生成二维码ticket"""
    def get(self):
        # 打开生成页面
        self.render("qrcode.html")

    def post(self):
        # 生成二维码需要用post方法
        pass
        


urls = [(r"/", MainHandler),
        # (r"/qrcode", Qrcode),
        ]



