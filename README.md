# CDN Cert
自动将 Let's encrypt 续签后的证书推送到阿里云 CDN

### 工作原理
定期对比存储在本机的证书与上一次推送成功的证书的 MD5

如有差异则将新证书推送到 CDN

使用 SQLite3 做为数据库，并支持阿里云邮件推送服务，如有更新可以将推送结果发送到您的邮箱。

### 使用方法
1. 获取项目
```
git clone https://github.com/0xJacky/cdn_cert.git
```
2. 安装阿里云 CDN SDK
```
pip install aliyun-python-sdk-cdn
```
3. 配置

    将 `cert-template.db` 复制一份并命名为 `cert.db`

    将 `settings-template.py` 复制一份并命名为 `settings.py`

    打开 `settings.py` 进行配置

4. 运行
```
python update.py
```
5. 定时配置
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

