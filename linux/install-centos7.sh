#!/bin/bash

set -e -u -x

WEBSERVER=nginx
OMEROVER=omero

for arg in "$@"; do
	case "$arg" in
	nginx|apache)
		WEBSERVER="$arg"
		;;
	omero|omerodev|omerodevmerge)
		OMEROVER="$arg"
		;;
	*)
		echo "Unknown option: $arg";
		exit 1
	esac
done

source settings.env

bash -eux dependencies-centos7.sh

bash -eux system_setup.sh
bash -eux setup_postgres.sh

cp settings.env setup_$OMEROVER.sh ~omero
if [ $WEBSERVER = apache ]; then
	cp setup_omero_apache.sh ~omero
fi
if [ $OMEROVER = omerodev ]; then
	yum -y install python-virtualenv
	yum clean all
	su - omero -c "bash -eux setup_$OMEROVER.sh"
elif [ $OMEROVER = omerodevmerge ]; then
	yum -y install python-virtualenv
	yum clean all
	su - omero -c "bash -eux setup_$OMEROVER.sh merge"
fi 


if [ $WEBSERVER = nginx ]; then
	bash -eux setup_nginx_centos7.sh
else
	su - omero -c "bash -eux setup_omero_apache.sh"
	bash -eux setup_apache_centos7.sh
fi

#If you don't want to use the systemd scripts you can start OMERO manually:
#su - omero -c "OMERO.server/bin/omero admin start"
#su - omero -c "OMERO.server/bin/omero web start"

bash -eux setup_omero_daemon_centos7.sh

systemctl start omero.service
systemctl start omero-web.service
