# Use official Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update apt cache and install required packages:
#   - git: for cloning repositories
#   - lynx: terminal-based web browser for verification
#   - python3: interpreter to run our Hello World program
RUN apt-get update && apt-get install -y \
    git \
    lynx \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Set a working directory inside the container
WORKDIR /workspace

# Clone the MIT xv6 public OS repository
RUN git clone https://github.com/mit-pdos/xv6-public.git

# Copy our Hello World Python script into the container
COPY hello.py .

# When the container starts, run the Hello World program
CMD ["python3", "hello.py"]
