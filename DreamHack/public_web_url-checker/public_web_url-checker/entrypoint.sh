#!/bin/bash
set -euo pipefail

echo "memory_limit = 512M" >> /usr/local/etc/php/php.ini

mkdir -p /run/mysqld
chown mysql:mysql /run/mysqld
mysqld_safe --datadir=/var/lib/mysql --bind-address=127.0.0.1 &
for i in {1..60}; do
  mysqladmin ping -h127.0.0.1 --silent && break
  sleep 1
done

mysql -uroot <<SQL
CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '${DB_USER}'@'127.0.0.1' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'127.0.0.1';
FLUSH PRIVILEGES;
SQL

if [ ! -f /var/www/html/cms/wp-config.php ]; then
  mkdir -p /var/www/html/cms
  cd /var/www/html/cms

  wp core download --version="${WP_VERSION}" --force --allow-root
  wp config create --dbname="${DB_NAME}" --dbuser="${DB_USER}" --dbpass="${DB_PASS}" \
                   --dbhost=127.0.0.1 --dbprefix=wp_ --skip-check --allow-root
  wp core install --url="${WP_URL}" --title="${WP_TITLE}" \
                  --admin_user="${WP_ADMIN_USER}" \
                  --admin_password="${WP_ADMIN_PASS}" \
                  --admin_email="${WP_ADMIN_EMAIL}" --allow-root

  wp plugin install /tmp/web-directory-free.zip --force --activate --allow-root

  wp option add ctf_flag 'cybercon{REDACTED}' --allow-root || true
fi

chown -R www-data:www-data /var/www/html
exec apache2-foreground
