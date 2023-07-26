#!/bin/bash

<<<<<<< HEAD
=======
set -x  # Enable debug mode to see each command's output

>>>>>>> 51fd4e4c2a8831d38fcf16c9e6e6fb308314d753
# Check if the Docker socket exists
if [ -S "/var/run/docker.sock" ]; then
    # Change the group ownership of the Docker socket
    sudo chgrp $(id -g) /var/run/docker.sock
    # Add write permissions for the group
    sudo chmod 666 /var/run/docker.sock
else
    echo "Docker socket not found."
    exit 1
fi
