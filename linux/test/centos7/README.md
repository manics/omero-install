Centos 7 testing
================

1. Create a test image containing the installation scripts
2. Start the container (this requires special options for systemd which may depend on your host system, see the [parent README](https://github.com/ome/ome-docker/blob/master/omero-ssh-systemd/README.md) for more details.)
3. ssh in
4. Change into the `/omero-install-test` directory
5. Run the scripts
6. Optionally set a system password for the `omero` user to allow ssh

        ./docker-build.sh centos7
        CID=$(docker run -d ... -v /sys/fs/cgroup:/sys/fs/cgroup:ro omero_install_test_centos7)
        #CID=$(docker run -d ... --privileged omero_install_test_centos7)
        ssh -o UserKnownHostsFile=/dev/null root@<address of container> # Password: omero
        cd /omero-install-test
        bash install-centos7.sh
        #echo omero:omero | chpasswd