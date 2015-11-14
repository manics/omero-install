#!/bin/bash

set -e -u -x

source settings.env

WEBSERVER=apache24

for arg in "$@"; do
	case "$arg" in
	apache24)
		WEBSERVER="$arg"
		;;
	*)
		echo "Unknown option: $arg";
		exit 1
	esac
done

OMERO.server/bin/omero config set omero.web.application_server wsgi
OMERO.server/bin/omero web config $WEBSERVER --http "$OMERO_WEB_PORT" > OMERO.server/apache.conf.tmp
OMERO.server/bin/omero web syncmedia
