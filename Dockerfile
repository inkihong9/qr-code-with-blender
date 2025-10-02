FROM python:3.11

# Update system packages to reduce vulnerabilities and remove unnecessary packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y ca-certificates && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip

# Copy the rest of your app
COPY . /app

# Default command to start bash
CMD ["bash"]
