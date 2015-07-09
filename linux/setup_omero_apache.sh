#!/bin/bash

set -e -u -x

source settings.env

OMERO.server/bin/omero config set omero.web.application_server wsgi
OMERO.server/bin/omero web config apache-wsgi > OMERO.server/apache.conf.tmp
OMERO.server/bin/omero web syncmedia
