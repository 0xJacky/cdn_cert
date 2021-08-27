# CDN Cert
自动将 Let's encrypt，或其他网站证书推送到阿里云 CDN

## v2.1 Beta 更新日志
更新于 2021 年 8 月 27 日
1. 修复 Python3.9 下邮件发送问题
2. 新增自定义证书路径配置，从上个版本更新的用户请在 `cert.db` 中，
为 `domain` 表添加 `cert_path(VARCHAR(255),is_nullable:YES)` 
和 `private_key_path(VARCHAR(255),is_nullable:YES)`
3. 使用 configparse 管理配置文件，更新时请将 `config-template.ini` 复制一份改名为 `config.ini` 并重新配置
4. 支持 Docker 部署 (TODO)

## v2 更新日志
更新于 2019 年 7 月 8 日

1. 支持多 RAM 账号。

    即当您有多个网站存在于同一个服务器上，且多个网站部署CDN时使用的不是同一阿里云账号时，
    CDN Cert 可以向多个阿里云账号推送续签后的证书。

2. **完全迁移至 Python 3.7**

### 工作原理
定期[1]对比存储在本机的证书与上一次推送成功的证书的 MD5

如有差异则将新证书推送到 CDN

使用 SQLite3 做为数据库，并支持阿里云邮件推送服务，如有更新可以将推送结果发送到您的邮箱。

## 手动配置环境
1. 准备
```
git clone https://github.com/0xJacky/cdn_cert.git
pip3 install -r requirements.txt
```
2. 配置

将 `config-template.ini` 复制一份并命名为 `config-template.ini`

#### config.ini 配置说明

| 配置项                           | 默认值                | 说明                                                         |
| -------------------------------- | --------------------- | ------------------------------------------------------------ |
| database.Path                    | cert.db               | 指定数据库存储的地址，相对路径                               |
| letencrypt.Path                  | /cert/ssl             | Let's encrypt 证书目录                                       |
| letencrypt.ServerCertificateName | fullchain.cer         | 如果您使用的是 Let's encrypt 官方的 certbot 则无需修改此项   |
| letencrypt.PrivateKeyName        | {{ domain_name }}.key | PrivkeyName 提供变量 {{ domain_name }}<br />例如，使用 acme.sh 管理证书的用户，生成的私钥名称与域名相同，则应该设置为 PrivkeyName = {{ domain_name }}.key |
| mail.Host                        | smtpdm.aliyun.com     | # 邮件反馈设置 - 阿里云邮件推送服务                          |
| mail.Port                        | 465                   | 发信端口，除 80 端口外默认使用 SSL                           |
| mail.UserName                    | -                     | 发件人地址，通过控制台创建的发件人地址                       |
| mail.PassWord                    | -                     | 发件人密码，通过控制台创建的发件人密码                       |
| mail.From                        | -                     | 发件人昵称                                                   |
| mail.To                          | -                     | 收件人地址，支持多个收件人，最多30个，以 `,` 分割            |



## 使用方法

1. 用法 `-h/ --help`
    ```
   usage: cdncert.py [-h] [-f] [-o ONLY] [-a {domain,user}] [-e {domain,user}] [-d {domain,user}] [-ls {domains,users}] [-v]
   
   CDN Cert - Automatically push the new certificates to CDN
   
   optional arguments:
     -h, --help            show this help message and exit
     -f, --force           force update
     -o ONLY, --only ONLY  update only, use it after -f/--force
     -a {domain,user}, --add {domain,user}
                           add [domain/user] to database
     -e {domain,user}, --edit {domain,user}
                           edit [domain/user] in database
     -d {domain,user}, --delete {domain,user}
                           delete [domain/user] from database
     -ls {domains,users}, --list {domains,users}
                           print all [domains/users] from database
     -v, --verbosity       increase output verbosity
   
   ```
2. 添加用户信息 `-a user`

    ![image][image-1]

    ![image][image-2]

3. 添加域名信息 `-a domain`

    ![image][image-3]

4. 删除用户 `-d user`

    ![image][image-4]

    ![image][image-5]

5. 删除域名 `-d domain`

    ![image][image-6]

6. 列出所有域名/用户 `-ls users/domains`

    ![image][image-7]

    ![image][image-8]

7. 开发模式 `-v`
8. 强制更新 `-f`
9. 仅更新单个域名 `-f -o {doamain}`
10. 推送成功的邮件模板

    ![image][image-9]
    
11. 定时配置（Docker 无需配置）
```
crontab -e
# 每天 3:30 执行
30 3 * * * python3 /home/cdn_cert/cdncert.py
```

### LICENSE 版权声明
Copyright © 2017 - 2019 0xJacky

The program is distributed under the terms of the GNU Affero General Public License.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see http://www.gnu.org/licenses/.


[image-1]:	https://github.com/0xJacky/cdn_cert/raw/master/screenshots/1.png
[image-2]:	https://github.com/0xJacky/cdn_cert/raw/master/screenshots/2.png
[image-3]:	https://github.com/0xJacky/cdn_cert/raw/master/screenshots/3.png
[image-4]:	https://github.com/0xJacky/cdn_cert/raw/master/screenshots/4.png
[image-5]:	https://github.com/0xJacky/cdn_cert/raw/master/screenshots/5.png
[image-6]:	https://github.com/0xJacky/cdn_cert/raw/master/screenshots/6.png
[image-7]:	https://github.com/0xJacky/cdn_cert/raw/master/screenshots/7.png
[image-8]:	https://github.com/0xJacky/cdn_cert/raw/master/screenshots/8.png
[image-9]:	https://github.com/0xJacky/cdn_cert/raw/master/screenshots/9.png
