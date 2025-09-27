# Use Blender LTS 4.5.3
FROM blender:4.5.3

# Install Python dev tools and common utilities
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        git \
        curl \
        vim \
    && rm -rf /var/lib/apt/lists/*

# Upgrade Blender's Python pip, setuptools, wheel
RUN blender --background --python-expr "import ensurepip; ensurepip.bootstrap(); import pip; pip.main(['install', '--upgrade', 'pip', 'setuptools', 'wheel'])"

# Set working directory for your project/addons
WORKDIR /workspace
