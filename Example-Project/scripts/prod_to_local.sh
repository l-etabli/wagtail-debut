#!/bin/bash
set -e

# Arguments
local_domain=${1-example.com.dev:8099}
ssh_host=${2-user@prod-server}

ROOTDIR=$(git rev-parse --show-toplevel)
DOCKERDIR=$(cd ${ROOTDIR}/docker/; pwd)


echo "Creating database dump from prod..."
ssh $ssh_host "export PGUSER=<remote_db_user> && pg_dump <remote_db> --no-owner > /tmp/db-dump.sql"

echo "Downloading database dump..."
scp $ssh_host:/tmp/db-dump.sql $DOCKERDIR/files/db-dumps/db-dump.sql
ssh $ssh_host "rm /tmp/db-dump.sql"

cd $ROOTDIR
echo "Rebuilding docker containers."

docker-compose stop
docker-compose rm -f
docker-compose up -d

echo "Waiting for postgres (60 seconds)..."
sleep 60

echo "Adjusting database..."

docker-compose exec web python manage.py change_site_domain --site_id=1 --new_site_domain=$local_domain

docker-compose exec web python manage.py change_user_password --user=admin --password=admin

echo "---"
echo "Done!"
echo "The application is ready at: $local_domain"
echo "Username/Password is admin/admin"