##out base image
FROM ubuntu

# Install JAVA
RUN apt-get update && apt-get -y install openjdk-8-jdk openjdk-8-jre

COPY partizan /usr/src/app/
WORKDIR /usr/src/app/bin/
RUN ./server.sh

# tell the port number the container should expose
EXPOSE 8089
