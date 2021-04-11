#!/bin/bash

backup_path="$PWD/db/backups/"

mysql_host="db"
mysql_user="root"
mysql_path="$(which mysql)"
check_connection="$($mysql_path -h $mysql_host -u$mysql_user --password=123 -Bse 'show databases')"
#/usr/bin/mysql -h "db" -u"root" --password=123 -Bse 'show databases'

echo "Connected to db, Starting backup"