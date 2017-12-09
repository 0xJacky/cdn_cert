#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime
import os
import collections
import hashlib
import json
import settings
from database import DB
from mail import Mail
from aliyunsdkcore import client
from aliyunsdkcdn.request.v20141111 import SetDomainServerCertificateRequest

db = DB()
mail = Mail()

class Process:
    def __init__(self):
        pass

    # 执行操作
    def do(self, force=False):
        self.push(force=force)

    # 获取证书 md5
    # 返回: 字符串
    def cert_md5(self, domain):
        privkey = os.path.join(settings.LiveCert, domain, 'privkey.pem')
        return hashlib.md5(privkey).hexdigest()

    # 处理推送
    def push(self, force):
        msg = {}
        for d in db.fetchall():
            store_md5 = db.fetchone(d)[1]
            currect_md5 = self.cert_md5(d)
            if not currect_md5 == store_md5 or force is True:
                try:
                    self.Client = client.AcsClient(settings.AccessKeyId, settings.AccessKeySecret, 'cn-hangzhou')
                    self.request = SetDomainServerCertificateRequest.SetDomainServerCertificateRequest()
                    self.request.set_accept_format('json')
                    CertName = d + '_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") # 证书名称，默认域名+日期时间
                    ServerCertificate_path = os.path.join(settings.LiveCert, d, 'fullchain.pem') # 安全证书路径
                    PrivateKey_path = os.path.join(settings.LiveCert, d, 'privkey.pem') # 私钥路径
                    self.request.set_DomainName(d)
                    self.request.set_CertName(CertName)
                    self.request.set_ServerCertificateStatus('on')
                    ServerCertificate = open(ServerCertificate_path, 'r').read()
                    ServerCertificate = open(ServerCertificate_path, 'r').read()
                    PrivateKey = open(PrivateKey_path, 'r').read()
                    self.request.set_ServerCertificate(ServerCertificate)
                    self.request.set_PrivateKey(PrivateKey)
                    RequestId = json.loads(self.Client.do_action_with_exception(self.request))['RequestId']
                    result = "Push success\nRequestId: "+ RequestId
                    db.update(d, currect_md5)
                except Exception as e:
                    result = e.get_error_code() if hasattr(e, 'get_error_code') else e
                msg[d] = result
        if msg:
            content = ""
            for k,v in msg.iteritems():
                content += 'Domain: ' + k + '\nResult: ' + str(v) + "\n\n"
            print content
            mail.send('[CDN Cert] 证书推送结果', content)
        else:
            print "Already up-to-date."
