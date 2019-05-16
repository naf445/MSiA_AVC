#!/bin/bash
user=$1
password=$2
host=$3
export MYSQL_USER=$user
export MYSQL_PASSWORD=$password
export MYSQL_HOST=$host
export MYSQL_PORT=3306
