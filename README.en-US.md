# CDN Cert
Automatically push Let's Encrypt or other website certificates to Aliyun CDN.

## v2.1 Changelog
Updated on August 28, 2021
1. Fixed email sending issues under Python 3.9.
2. Added custom certificate path configuration. Users updating from previous versions, please add `cert_path(VARCHAR(255),is_nullable:YES)` and `private_key_path(VARCHAR(255),is_nullable:YES)` to the `domain` table in `cert.db`.
3. Now using `configparse` to manage configuration files. When updating, please copy `config-template.ini` to `config.ini` and reconfigure.
4. Ability to modify domain certificate configuration and user information.
5. Support for Docker deployment.
6. Docker containers automatically configure cron jobs to execute updates daily at 01:00, with logs automatically recorded in `cdncert.log`.

## v2 Changelog
Updated on July 8, 2019

1. Support for multiple RAM accounts.

    This means if you have multiple websites on the same server and they use different Aliyun accounts for CDN deployment, CDN Cert can push renewed certificates to multiple Aliyun accounts.

2. **Completely migrated to Python 3.7**

### How it Works
Periodically[1] compares the MD5 hash of the "Certificate + Private Key" combination with the digest from the last successful push.

If there is a difference, the new certificate will be pushed to the CDN.

SQLite3 is used as the database. It also supports Aliyun's email push service to send update results to your mailbox.

## Docker Deployment

1. Preparation

   ```
   git clone https://github.com/0xJacky/cdn_cert.git
   ```

2. Configuration: Copy `config-template.ini` and name it `config.ini`.

3. Run Docker

   ```
   docker run -dit -v ${config_and_db_directory}:/app/data \
                   -v ${absolute_path_to_cert_folder}:/cert \
                   --name=cdn_cert -e "TZ=Asia/Shanghai" \
                   uozi/cdn_cert /bin/bash
   ```

4. After modifying the configuration, use `docker restart cdn_cert` to restart the container.

5. Enter the container to configure domains and user information:

   ```
   docker exec -it <image_id> /bin/bash
   ```

6. Note: After mapping the directory, enter the docker container to configure the custom certificate path; this path must be the absolute path within the container.

## Manual Environment Setup

1. Preparation
   ```
   git clone https://github.com/0xJacky/cdn_cert.git
   pip3 install -r requirements.txt
   ```
2. Copy `config-template.ini` and name it `config.ini`.

## config.ini Configuration Details

| Configuration Item           | Default Value         | Description                                                                 |
| ---------------------------- | --------------------- | --------------------------------------------------------------------------- |
| database.Path               | cert.db               | Path to store the database, relative path                                   |
| letencrypt.Path             | /cert                 | Let's Encrypt certificate directory. In Docker mode, map the absolute path of the cert folder to /cert; this can be left unchanged. |
| letencrypt.ServerCertificateName | fullchain.cer         | No need to change if you are using the official Let's Encrypt certbot.     |
| letencrypt.PrivateKeyName    | {{ domain_name }}.key | `PrivkeyName` provides a variable `{{ domain_name }}`.<br />For example, if you use acme.sh and the private key name is the same as the domain, set it to `PrivkeyName = {{ domain_name }}.key` |
| mail.Host                   | smtpdm.aliyun.com     | Email feedback settings - Aliyun Email Push Service                          |
| mail.Port                   | 465                   | Sending port; SSL is used by default except for port 80.                    |
| mail.UserName               | -                     | Sender address created via the console.                                       |
| mail.PassWord               | -                     | Sender password created via the console.                                     |
| mail.From                   | -                     | Sender nickname                                                             |
| mail.To                     | -                     | Recipient addresses, supports up to 30 recipients, separated by `,`            |

## Usage

1. Usage `-h/ --help`
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
   
2. Add user information `-a user`

    ![image][image-1]

    ![image][image-2]

3. Add domain information `-a domain`

    ![image][image-3]

4. Edit user `-e user`

5. Edit domain `-e domain`

6. Delete user `-d user`

    ![image][image-4]

    ![image][image-5]

7. Delete domain `-d domain`

    ![image][image-6]

8. List all domains/users `-ls users/domains`

    ![image][image-7]

    ![image][image-8]

9. Development mode `-v`

10. Force update `-f`

11. Update a single domain only `-f -o {domain}`

12. Email template for successful push

     ![image][image-9]

13. Scheduled Task (No configuration needed for Docker)
```
crontab -e
# Execute daily at 3:30
30 3 * * * python3 /path/to/cdncert.py
```

### LICENSE Copyright Notice
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
