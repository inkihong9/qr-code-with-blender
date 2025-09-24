# Use Ubuntu 22.04 (glibc >= 2.28)
FROM ubuntu:22.04

# Prevent interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install Blender, Python, pip, and utilities
RUN apt-get update && apt-get install -y \
    blender \
    python3 \
    python3-pip \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Make "python" command point to python3
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Set default working directory
WORKDIR /workspace
