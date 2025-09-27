FROM ubuntu:22.04

# Blender version
ARG BLENDER_VERSION=4.2.0
ARG BLENDER_TAR=blender-${BLENDER_VERSION}-linux-x64.tar.xz
ARG BLENDER_URL=https://download.blender.org/release/Blender${BLENDER_VERSION%.*}/${BLENDER_TAR}

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    xz-utils \
    python3 \
    python3-pip \
    python3-distutils \
    python3-venv \
    git \
    libgl1 \
    libx11-6 \
    libxi6 \
    libxxf86vm1 \
    libxrender1 \
    libxrandr2 \
    libxcursor1 \
    libxinerama1 \
    libglu1-mesa \
    libegl1 \
    libxkbcommon0 \
    libxkbcommon-x11-0 \
    libxcb-xinerama0 \
    && rm -rf /var/lib/apt/lists/*


# Download and install Blender
RUN wget ${BLENDER_URL} -O /tmp/${BLENDER_TAR} && \
    tar -xJf /tmp/${BLENDER_TAR} -C /opt && \
    ln -s /opt/blender-${BLENDER_VERSION}-linux-x64/blender /usr/local/bin/blender && \
    rm /tmp/${BLENDER_TAR}

# Enable pip + setuptools (distutils replacement) inside Blender’s bundled Python
RUN /opt/blender-${BLENDER_VERSION}-linux-x64/${BLENDER_VERSION%.*}/python/bin/python3.11 -m ensurepip && \
    /opt/blender-${BLENDER_VERSION}-linux-x64/${BLENDER_VERSION%.*}/python/bin/python3.11 -m pip install --upgrade pip setuptools wheel && \
    /opt/blender-${BLENDER_VERSION}-linux-x64/${BLENDER_VERSION%.*}/python/bin/python3.11 -m pip install setuptools

# Example: preinstall external Python packages for addons
RUN /opt/blender-${BLENDER_VERSION}-linux-x64/${BLENDER_VERSION%.*}/python/bin/python3.11 -m pip install requests numpy

# Install dev tools for system Python
RUN pip install setuptools black flake8 pytest

# Workspace for addons
WORKDIR /workspace

CMD ["blender"]
