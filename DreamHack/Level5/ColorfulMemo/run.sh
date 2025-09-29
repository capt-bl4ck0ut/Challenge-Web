#!/bin/sh
chsh -s /bin/bash www-data
su -p www-data -c "docker-entrypoint.sh mysqld" &
apache2ctl -D FOREGROUND