#################
##### BUILD #####
#################
FROM debian:bookworm as builder

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive
ENV VIRTUAL_ENV=/opt/venv

# Install base tools
RUN \
apt-get update && apt-get install -y git --no-install-recommends
RUN apt-get install -y python3-full python3-pip python3-venv

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY . .

#RUN python3 -m pip install .

ENTRYPOINT python3 entrypoint.py