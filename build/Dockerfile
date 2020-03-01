# https://docs.docker.com/engine/reference/builder/#from
# https://github.com/phusion/baseimage-docker
FROM phusion/baseimage:0.11

# https://docs.docker.com/engine/reference/builder/#run
RUN apt-get update && \
    apt-get install -y \
    redis-server \
    gcc \
    git \ 
    make \
    graphviz \
    python3-dev \
    python-dev \
    python3-pip 

WORKDIR /opt/
RUN service redis-server stop
RUN cd /opt/
RUN git clone https://github.com/RedisJSON/RedisJSON.git
RUN cd /opt/RedisJSON && make
RUN redis-server --loadmodule src/rejson.so &
RUN cd /opt/
RUN git clone https://github.com/msgoff/Flask-Socketio
RUN cd Flask-Socketio
RUN pip3 install redis
RUN pip3 install tatsu

