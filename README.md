# CDN Cert
自动将 Let's encrypt，或其他网站证书推送到阿里云 CDN

## v2.1 更新日志
更新于 2021 年 8 月 28 日
1. 修复 Python3.9 下邮件发送问题
2. 新增自定义证书路径配置，从上个版本更新的用户请在 `cert.db` 中，
为 `domain` 表添加 `cert_path(VARCHAR(255),is_nullable:YES)` 
和 `private_key_path(VARCHAR(255),is_nullable:YES)`
3. 使用 configparse 管理配置文件，更新时请将 `config-template.ini` 复制一份改名为 `config.ini` 并重新配置
4. 可修改域名证书配置和用户信息
5. 支持 Docker 部署
6. Docker 容器自动配置定时任务，每天 01:00 执行更新，日志自动记录在 cdncert.log

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

## Docker 部署

1. 准备

   ```
   git clone https://github.com/0xJacky/cdn_cert.git
   ```

2. 配置将 `config-template.ini` 复制一份并命名为 `config.ini`

3. 运行 Docker

   ```
   docker run -dit -v ${配置和数据库文件目录}:/app/data \
                   -v ${证书文件夹的绝对路径}:/cert \
                   --name=cdn_cert -e "TZ=Asia/Shanghai" \
                   uozi/cdn_cert /bin/bash
   ```

4. 修改配置后使用 `docker restart cdn_cert` 重启容器。

5. 进入容器配置域名及用户信息

   ```
   docker exec -it <image_id> /bin/bash
   ```

6. 注意映射目录后进入 docker 内配置自定义证书的路径，此路径是容器内的绝对路径。

## 手动配置环境

1. 准备
   ```
   git clone https://github.com/0xJacky/cdn_cert.git
   pip3 install -r requirements.txt
   ```
2. 将 `config-template.ini` 复制一份并命名为 `config.ini`

## config.ini 配置说明

| 配置项                           | 默认值                | 说明                                                         |
| -------------------------------- | --------------------- | ------------------------------------------------------------ |
| database.Path                    | cert.db               | 指定数据库存储的地址，相对路径                               |
| letencrypt.Path                  | /cert                 | Let's encrypt 证书目录，使用 Docker 模式时将证书文件夹的绝对路径映射到 /cert 即可，可以不修改此项 |
| letencrypt.ServerCertificateName | fullchain.cer         | 如果您使用的是 Let's encrypt 官方的 certbot 则无需修改此项   |
| letencrypt.PrivateKeyName        | {{ domain_name }}.key | PrivkeyName 提供变量 {{ domain_name }}<br />例如，使用 acme.sh 管理证书的用户，生成的私钥名称与域名相同，则应该设置为 PrivkeyName = {{ domain_name }}.key |
| mail.Host                        | smtpdm.aliyun.com     | 邮件反馈设置 - 阿里云邮件推送服务                            |
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

4. 编辑用户 `-e user`

5. 编辑域名 `-e domain`

6. 删除用户 `-d user`

    ![image][image-4]

    ![image][image-5]

7. 删除域名 `-d domain`

    ![image][image-6]

8. 列出所有域名/用户 `-ls users/domains`

    ![image][image-7]

    ![image][image-8]

    

9. 开发模式 `-v`

10. 强制更新 `-f`

11. 仅更新单个域名 `-f -o {doamain}`

12. 推送成功的邮件模板

     ![image][image-9]

13. 定时配置（Docker 无需配置）
```
crontab -e
# 每天 3:30 执行
30 3 * * * python3 /path/to/cdncert.py
```

### LICENSE 版权声明
Copyright © 2017 - 2024 0xJacky

The program is distributed under the terms of the GNU Affero General Public License.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see http://www.gnu.org/licenses/.


[image-1]:	screenshots/1.png
[image-2]:	screenshots/2.png
[image-3]:	screenshots/3.png
[image-4]:	screenshots/4.png
[image-5]:	screenshots/5.png
[image-6]:	screenshots/6.png
[image-7]:	screenshots/7.png
[image-8]:	screenshots/8.png
[image-9]:	screenshots/9.png
