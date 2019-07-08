#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime
import os
import hashlib
import json
import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcdn.request.v20180510.SetDomainServerCertificateRequest import SetDomainServerCertificateRequest
from prettytable import PrettyTable
from database import Database
from mail import Mail

db = Database()
mail = Mail()


class Core:
    def __init__(self):
        pass

    # 执行操作
    def do(self, force=False, only=''):
        queue = ()
        if only:
            if db.has_domain(only):
                queue = (only,)
            else:
                exit('\033[1;31mNo record of this domain.\nPlease add this domain before the operation.\033[0m')

        else:
            domains = db.get_all_domain()
            for domain in domains:
                queue = (domain.domain, )
        self.push(force=force, queue=queue)

    # 获取文件 md5
    # 返回: 字符串
    @staticmethod
    def md5sum(path):
        file = open(path, 'rb')
        return hashlib.md5(file.read()).hexdigest()

    def add_user(self):
        name = input('Please input the user name\n')

        if db.has_user(name):
            exit('\033[1;31mUser %s already exists.\033[0m' % name)

        access_key_id = input('Please input the Access Key ID\n')
        access_key_secret = input('Please input the Access Key Secret\n')
        db.add_user(name, access_key_id, access_key_secret)

    def add_domain(self):
        domain = input('Please input your domain here\n')

        if db.has_domain(domain):
            exit('\033[1;31mDomain %s already exists\033[0m' % domain)

        self.get_all_user()
        user = input('Please input a user name from the table above.\n')

        if db.has_user(user) is not True:
            exit('\033[1;31mNo record of %s.\033[0m' % user)

        db.add_domain(domain, user)

    @staticmethod
    def get_all_domain():
        print('--------------------------------')
        print('Here are your domains list')
        domains = db.get_all_domain()
        table = PrettyTable(['Domain', 'User'])
        for domain in domains:
            table.add_row([domain.domain, domain.user])
        print(table)
        print('--------------------------------')

    @staticmethod
    def get_all_user():
        print('--------------------------------')
        print('Here are your users list')
        users = db.get_all_user()
        table = PrettyTable(['User', 'Access Key ID'])
        for user in users:
            table.add_row([user.name, user.access_key_id])
        print(table)
        print('--------------------------------')

    def update_domain(self):
        self.get_all_domain()
        domain = input('Please input a domain from the table above.\n')

        if db.has_domain(domain) is not True:
            exit('\033[1;31mNo record of this domain.\033[0m')

        self.get_all_user()
        user = input('Please input a user name from the table above.\n')

        if db.has_user(user) is not True:
            exit('\033[1;31mNo record of this user.\033[0m')

        db.update_domain(domain, user=user)

    def delete_domain(self):
        self.get_all_domain()
        domain = input('Please input a domain to delete from the table above.\n')

        if db.has_domain(domain) is not True:
            exit('\033[1;31mNo record of this domain.\033[0m')

        sure = input('Are you sure to delete this domain: [y/n]')

        if sure == 'y':
            db.delete_domain(domain)

    def delete_user(self):
        self.get_all_user()
        user = input('Please input a user to delete from the table above.\n')

        if db.has_user(user) is not True:
            exit('\033[1;31mNo record of this user.\033[0m')

        sure = input('Are you sure to delete this user: [y/n]')
        if sure == 'y':
            db.delete_user(user)

    # 处理推送
    def push(self, force, queue=()):
        msg = {}
        for domain in queue:
            PrivateKeyPath = os.path.join(settings.LiveCert, domain,
                                          settings.PrivkeyName.replace('{{ domain_name }}', domain))  # 私钥路径
            info = db.get_domain(domain)
            user = db.get_user(info.user)
            store_md5 = info.md5
            currect_md5 = self.md5sum(PrivateKeyPath)
            if not currect_md5 == store_md5 or force is True:
                try:
                    client = AcsClient(user.access_key_id, user.access_key_secret, 'cn-hangzhou')
                    ServerCertificatePath = os.path.join(settings.LiveCert, domain,
                                                         settings.ServerCertificateName)  # 安全证书路径
                    ServerCertificate = open(ServerCertificatePath, 'r').read()
                    PrivateKey = open(PrivateKeyPath, 'r').read()
                    CertName = domain + '_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # 证书名称

                    request = SetDomainServerCertificateRequest()
                    request.set_accept_format('json')
                    request.set_DomainName(domain)
                    request.set_ServerCertificateStatus("on")
                    request.set_CertName(CertName)
                    request.set_ServerCertificate(ServerCertificate)
                    request.set_PrivateKey(PrivateKey)
                    request.set_CertType("upload")  # 上传证书
                    request.set_ForceSet("1")  # 忽略证书同名检测
                    response = client.do_action_with_exception(request)
                    RequestId = json.loads(response.decode('utf-8'))['RequestId']
                    result = "Push successfully\nRequestId: " + str(RequestId)

                    db.update_domain(domain, currect_md5)
                except Exception as e:
                    result = e.get_error_code() if hasattr(e, 'get_error_code') else e
                msg[domain] = result
        if msg:
            content = ""
            for k, v in msg.items():
                content += 'Domain: ' + k + '\nResult: ' + str(v) + "\n\n"
            print(content)
            mail.send('[CDN Cert] 证书推送结果', content)
        else:
            print("Already up-to-date.")
