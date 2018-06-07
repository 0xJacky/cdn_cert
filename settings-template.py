#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
## 配置开始
# 访问 https://ak-console.aliyun.com/index#/accesskey 获取
AccessKeyId = ''
AccessKeySecret = ''

# Let's encrypt 证书目录，一般情况下无需修改
# LetsencryptPath = os.path.join('/usr/local/nginx/conf')
# LiveCert = os.path.join(LetsencryptPath, 'ssl')
LetsencryptPath = os.path.join('/etc/letsencrypt')
LiveCert = os.path.join(LetsencryptPath, 'live')

# 安全证书与私钥名称设置
# 警告：如果您使用的是 Let's encrypt 官方的 certbot 则无需修改此项目
ServerCertificateName = 'fullchain.pem'
PrivkeyName = 'privkey.pem'
# PrivkeyName 提供变量 {{ domain_name }}
# 例如，使用 acme.sh 管理证书的用户，生成的私钥名称与域名相同，则应该设置为 PrivkeyName = '{{ domain_name }}.key'
# ServerCertificateName = 'fullchain.cer'
# PrivkeyName = '{{ domain_name }}.key'

# 数据存储地址
ABS_PATH = os.path.split(os.path.realpath(__file__))[0]
DB_PATH = os.path.join(ABS_PATH, 'cert.db')

# 邮件反馈设置 - 阿里云邮件推送服务
Host = 'smtpdm.aliyun.com'
Port = '465'
# 发件人地址，通过控制台创建的发件人地址
UserName = ''
# 发件人密码，通过控制台创建的发件人密码
PassWord = ''
# 发件人昵称
From = ''
# 收件人地址或是地址列表，支持多个收件人，最多30个
#To = ['***', '***']
To = ''
