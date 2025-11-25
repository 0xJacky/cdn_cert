#!/bin/bash

docker build -t cdn_cert .

docker run -dit -v .:/app \
                -v ./cert:/cert \
                --name=cdn_cert -e "TZ=Asia/Shanghai" \
                cdn_cert /bin/bash
