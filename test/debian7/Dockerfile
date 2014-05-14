# Dockerfile for testing the OMERO Linux installation instructions
# Not intended for production use
FROM debian
MAINTAINER ome-devel@lists.openmicroscopy.org.uk

ADD https://github.com/manics/omero-install/archive/master.zip /
RUN apt-get update && apt-get install unzip && unzip master.zip

RUN cd omero-install-master && bash install-debian7-ubuntu1404.sh
ADD run.sh /home/omero/run.sh

EXPOSE 80 4063 4064
CMD ["/bin/bash", "-e", "/home/omero/run.sh"]
