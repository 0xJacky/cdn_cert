#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2017 0xJacky <jacky-943572677@qq.com>
#
# ！请先使用 pip install aliyun-python-sdk-cdn 安装 sdk！

from process import Process
main = Process()

main.insert_domain_list()
main.push()
