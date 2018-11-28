# Raider Bot Container
FROM python:3.7.1-slim-stretch

# Enable non-free debian
RUN sed -i 's/stretch\ main/stretch\ main\ non-free/g' /etc/apt/sources.list
# Update and install packages
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y \
        nmap \
        tor \
        nikto \
        git \
        build-essential \
    && apt-get clean && apt-get autoremove

# Install proxychains-ng
RUN cd /tmp && git clone https://github.com/rofl0r/proxychains-ng.git && cd proxychains-ng \
    && ./configure --prefix=/usr --sysconfdir=/etc \
    && make && make install && make install-config \
    && rm -rf /tmp/proxychains-ng && ln -s /usr/bin/proxychains4 /usr/bin/proxychains

# save precious space
RUN apt-get remove -y build-essential git

# don't run as root
RUN groupadd --gid 1001 app
RUN useradd --uid 1001 --gid app --home /app app
RUN pip install pipenv --no-cache-dir

# make app dir
RUN mkdir /app && \
    chown app.app /app
USER app
WORKDIR /app

# set up reqs
COPY --chown=app:app requirements.txt /app/requirements.txt
RUN pip install --user -r /app/requirements.txt && .local/bin/errbot --init
COPY plugins/* /app/plugins/

COPY config/* /app/
# Setup extra fun stuff
# RUN git clone git@github.com:vulnersCom/nmap-vulners.git

#Set the Entrypoint
COPY docker/* /app/docker/
USER root
RUN chmod +x /app/docker/*.sh
USER app
ENTRYPOINT [ "/app/docker/entrypoint.sh" ]
CMD [ ".local/bin/errbot", "--config", "/app/config.py" ]
