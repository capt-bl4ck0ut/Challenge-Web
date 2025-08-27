#!/bin/bash

export FLAG=$(cat /tmp/flag.txt)
export ADMIN_PASSWORD=$(cat /tmp/admin_password.txt)
rm -f /tmp/flag.txt /tmp/admin_password.txt

python3 /home/server/chall/admin.py &
python3 /home/server/chall/run.py
