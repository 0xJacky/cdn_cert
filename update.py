#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2017 0xJacky <jacky-943572677@qq.com>
#
# ！请先使用 pip install aliyun-python-sdk-cdn 安装 sdk！

import argparse
from process import Process
from database import DB

Process = Process()
db = DB()

parser = argparse.ArgumentParser(description='CDN_Cert - Automatically push the new certificates to CDN')
parser.add_argument('-f', '--force', action="store_true", help='force update')
parser.add_argument('-o', '--only', action="store", default=None, help='update only, use it after -f/-force')
parser.add_argument('-a', '--add', action="store_true", help='add domain name to database')
parser.add_argument('-d', '--delete', action="store_true", help='remove domain name from database')
parser.add_argument('-ls', '--list', action="store_true", help='print all the domain names from database')
args = parser.parse_args()

if args.force:
    Process.do(force=True, only=args.only)
elif args.add:
    db.add()
elif args.delete:
    db.delete()
elif args.list:
    db.domainlist()
else:
    Process.do()
