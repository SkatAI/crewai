FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    gcc \
    curl \
    vim \
    pkg-config \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Upgrade pip
RUN pip3 install --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code into the container in ./src
# RUN mkdir -p /app/src
# COPY src/*.py ./src

# Run the bot when the container launches
# CMD ["python", "main.py"]


RUN echo "alias ll='ls -la'" >> ~/.bashrc && \
    echo "PS1='\[\033[01;32m\]\u@crewai\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> ~/.bashrc

# Set Python to not write .pyc files and to flush stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Default command (optional - docker-compose.yml settings will override this)
CMD ["/bin/bash"]