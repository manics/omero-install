# Dockerfile for testing the OMERO Linux installation instructions
# Not intended for production use
FROM centos:centos6
MAINTAINER ome-devel@lists.openmicroscopy.org.uk

# Needed for postgres init.d
RUN touch /etc/sysconfig/network

# Get cron working http://stackoverflow.com/a/21928878
RUN yum -y install cronie && \
	sed -i -re s'/(session\s+required\s+pam_loginuid.so)/#\1/' \
	/etc/pam.d/crond

ADD omero-install-test.zip /
RUN yum -y install unzip && unzip omero-install-test.zip

RUN cd omero-install-test && bash install.sh centos6 omero51-merge apache
ADD run.sh /home/omero/run.sh

EXPOSE 80 4063 4064
CMD ["/bin/bash", "-e", "/home/omero/run.sh"]
