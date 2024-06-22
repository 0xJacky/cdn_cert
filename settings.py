#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import configparser
dataDir = 'data'
if not os.path.isfile(dataDir):
  os.path.isfile(dataDir)
if not os.path.isfile(dataDir + '/config.ini'):
  os.system('cp config-template.ini ' + dataDir + '/config.ini')
config = configparser.ConfigParser()
config.read(dataDir + '/config.ini')
# 数据存储地址
ABS_PATH = os.path.split(os.path.realpath(__file__))[0]
DB_PATH = os.path.join(ABS_PATH, config['database']['Path'])

# 配置开始
# Let's encrypt 证书目录，一般情况下无需修改
LiveCert = os.path.join(config['letencrypt']['Path'])

# 安全证书与私钥名称设置
# 警告：如果您使用的是 Let's encrypt 官方的 certbot 则无需修改此项
ServerCertificateName = config['letencrypt']['ServerCertificateName']
# PrivateKeyName 提供变量 {{ domain_name }}
# 例如，使用 acme.sh 管理证书的用户，生成的私钥名称与域名相同，则应该设置为 PrivateKeyName = '{{ domain_name }}.key'
PrivateKeyName = config['letencrypt']['PrivateKeyName']

mail = config['mail']
# 邮件反馈设置 - 阿里云邮件推送服务
Host = mail['Host']
Port = mail['Port']
# 发件人地址，通过控制台创建的发件人地址
UserName = mail['UserName']
# 发件人密码，通过控制台创建的发件人密码
PassWord = mail['Password']
# 发件人昵称
From = mail['From']
# 收件人地址或是地址列表，支持多个收件人，最多30个
To = mail['To'].split(',')
