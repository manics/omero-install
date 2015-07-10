# Dockerfile for testing the OMERO Linux installation instructions
# Not intended for production use
FROM ubuntu:14.04
MAINTAINER ome-devel@lists.openmicroscopy.org.uk

RUN update-locale LANG=C.UTF-8

ADD omero-install-test.zip /
RUN apt-get update && apt-get -y install unzip && unzip omero-install-test.zip

RUN cd omero-install-test && bash install.sh ubuntu1404 omero51-merge nginx
ADD run.sh /home/omero/run.sh

EXPOSE 80 4063 4064
CMD ["/bin/bash", "-e", "/home/omero/run.sh"]
