#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
## 配置开始
# 访问 https://ak-console.aliyun.com/index#/accesskey 获取
AccessKeyId = ''
AccessKeySecret = ''

# 指定证书所属加速域名，需属于https加速类型
DomainName = ['',]

# Let's encrypt 证书目录，一般情况下无需修改
LetsencryptPath = os.path.join('/etc/letsencrypt')
LiveCert = os.path.join(LetsencryptPath, 'live')

# 数据存储地址
ABS_PATH = os.path.split(os.path.realpath(__file__))[0]
JSON_PATH = os.path.join(ABS_PATH, 'data.json')

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
