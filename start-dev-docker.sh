#!/bin/bash

docker build -t cdn_cert .

docker run -dit -v /Users/Jacky/Documents/Projects/cdn_cert:/app \
                -v /Users/Jacky/Documents/Projects/cdn_cert/cert:/cert \
                --name=cdn_cert \
                cdn_cert /bin/bash
