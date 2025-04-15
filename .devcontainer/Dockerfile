FROM mcr.microsoft.com/devcontainers/python:0-3.11

RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc && \
    curl https://packages.microsoft.com/config/debian/11/prod.list | sudo tee /etc/apt/sources.list.d/msprod.list && \
    sudo apt-get update && \
    sudo ACCEPT_EULA=y apt-get install -y mssql-tools18