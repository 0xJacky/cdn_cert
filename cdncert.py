#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2017-2021 0xJacky <me@jackyu.cn>
#
# ！请先使用 pip3 install -r requirements.txt 安装依赖

import argparse
from core import Core
from database import Database

parser = argparse.ArgumentParser(description='CDN Cert - Automatically push the new certificates to CDN')
parser.add_argument('-f', '--force', action="store_true", help='force update')
parser.add_argument('-o', '--only', action="store", default=None, help='update only, use it after -f/--force')
parser.add_argument('-a', '--add', action="store", choices=['domain', 'user'], help='add [domain/user] to database')
parser.add_argument('-e', '--edit', action="store", choices=['domain', 'user'], help='edit [domain/user] in database')
parser.add_argument('-d', '--delete', action="store", choices=['domain', 'user'], help='delete [domain/user] from '
                                                                                       'database')
parser.add_argument('-ls', '--list', action="store", choices=['domains', 'users'], help='print all [domains/users] '
                                                                                        'from database')
parser.add_argument("-v", "--verbosity", action="store_true", help="increase output verbosity")
args = parser.parse_args()

Core = Core()
db = Database(args.verbosity)

if args.force:
    Core.do(force=True, only=args.only)
elif args.add:
    if args.add == 'user':
        Core.add_user()
    elif args.add == 'domain':
        Core.add_domain()
elif args.edit:
    if args.edit == 'user':
        pass
        Core.update_user()
    elif args.edit == 'domain':
        Core.update_domain()
elif args.delete:
    if args.delete == 'user':
        Core.delete_user()
    elif args.delete == 'domain':
        Core.delete_domain()
elif args.list:
    if args.list == 'users':
        Core.get_all_user()
    elif args.list == 'domains':
        Core.get_all_domain()
else:
    Core.do()
