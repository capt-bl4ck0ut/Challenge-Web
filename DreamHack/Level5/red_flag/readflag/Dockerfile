FROM ubuntu:18.04

# Install prereqs
RUN apt update && apt install -y wget git make gcc

# Setup goahead
WORKDIR /goahead
RUN git clone https://github.com/lemonholic/goahead-archive.git
WORKDIR /goahead/goahead-archive
### Todo: Switch to the patched version.
### RUN git checkout v4.1.3.1
RUN git checkout v4.1.3

## Build/install
RUN make ME_GOAHEAD_SSL=0 ME_COM_SSL=0 && make install

# Copy in content files
COPY ./deploy/www /var/www/goahead
COPY ./deploy/goahead /etc/goahead/
WORKDIR /etc/goahead/
COPY ./deploy/start.sh .
CMD ["./start.sh"]
