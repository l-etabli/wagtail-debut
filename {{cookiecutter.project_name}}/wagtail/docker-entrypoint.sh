#!/bin/bash
# $0 is a script name, $1, $2, $3 etc are passed arguments
# $1 is our command
# Credits: https://rock-it.pl/how-to-write-excellent-dockerfiles/
CMD=$1

wait_for_db () {
    # Wait until postgres is ready
    until nc -z $DATABASE_HOST 5432; do
        echo "$(date) - waiting for postgres... ($DATABASE_HOST:5432)"
        sleep 3
    done
}

setup_django () {
    echo Running migrations
    python manage.py migrate --noinput

    echo Create dummy user if none exists
    python manage.py create_superuser_if_none_exists --user=admin --password=admin

    echo Replace possible default site root page
    python manage.py wagtail_replace_default_site_root_page

    echo Collecting static-files
    python manage.py collectstatic --noinput

    echo Create cache table
    python manage.py createcachetable
}

case "$CMD" in
    "runserver" )
        wait_for_db
        setup_django

        echo Starting using manage.py runserver
        exec python manage.py runserver 0.0.0.0:8000
        ;;

    "uwsgi" )
        wait_for_db
        setup_django

		pip install uwsgi

        echo Starting using uwsgi
        exec uwsgi --ini uwsgi.ini
        ;;

    "test" )
        wait_for_db

        echo Running tests
        exec pytest --ds=pipit.settings.test
        ;;

    "typecheck" )
        echo Running typecheck
        exec mypy .
        ;;

    * )
        # Run custom command. Thanks to this line we can still use
        # "docker run our_container /bin/bash" and it will work
        exec $CMD ${@:2}
        ;;
esac
