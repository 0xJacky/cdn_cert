# CDN Cert
自动将 Let's encrypt 续签后的证书推送到阿里云 CDN

### 工作原理
定期对比存储在本机的证书与上一次推送成功的证书的 MD5

如有差异则将新证书推送到 CDN

使用 SQLite3 做为数据库，并支持阿里云邮件推送服务，如有更新可以将推送结果发送到您的邮箱。

### 使用方法
1. 准备
```
git clone https://github.com/0xJacky/cdn_cert.git
pip install aliyun-python-sdk-cdn
```
2. 配置
	将 `settings-template.py` 复制一份并命名为 `settings.py`

	打开 `settings.py` 进行配置

	运行 `python update.py -a` 添加需要自动续期的域名到数据库

3.  参数
	
	$python update.py -h
	usage: update.py [-h] [-f] [-a] [-d] [-ls]
	
	CDN_Cert - Automatically push the new certificates to CDN
	
	optional arguments:
	  -h, --help    show this help message and exit
	  -f, --force   force update
	  -a, --add     add domain name to database
	  -d, --delete  remove domain name from database
	  -l, --list   print all the domain names from database
	
	e.g.
	$python update.py
	Domain: jackyu.cn
	Result: Push success
	RequestId: D40F6BC4-6418-43B1-8E31-8BBB548AB3E2
	
	Domain: beta.uozi.org
	Result: Push success
	RequestId: 9BF6A271-38CC-45F4-8DA0-48022DB742A3
	
	
	邮件发送成功！
	$python update.py -f (force update)
	Domain: jackyu.cn
	Result: Push success
	RequestId: D40F6BC4-6418-43B1-8E31-8BBB548AB3E2
	
	Domain: beta.uozi.org
	Result: Push success
	RequestId: 9BF6A271-38CC-45F4-8DA0-48022DB742A3
	
	
	邮件发送成功！
	
	$python update.py -l
	CDN Cert -- Domain List
	-----------------------
	beta.uozi.org
	jackyu.cn
	-----------------------
	
	$python update.py -a
	Plase input the domain name, use ',' to split.
	ojbk.me
	Execute successfully.
	
	$python update.py -d
	Plase input a domain name to delete.
	beta.uozi.org
	Execute successfully.
	
4. 定时配置
```
crontab -e
# 每天 3:30 执行
30 3 * * * python /home/cdn_cert/update.py
```

### LICENSE 版权声明
Copyright © 2017 0xJacky

The program is distributed under the terms of the GNU Affero General Public License.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see http://www.gnu.org/licenses/.