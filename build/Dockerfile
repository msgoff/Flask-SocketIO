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
    wget \
    graphviz \
    python3-dev \
    python-dev \
    python3-pip 

WORKDIR /opt/
RUN service redis-server stop
RUN cd /opt/
RUN git clone https://github.com/RedisJSON/RedisJSON.git
RUN cd /opt/RedisJSON && make
RUN cd /opt/
RUN git clone https://github.com/msgoff/Flask-Socketio
RUN cd Flask-Socketio
RUN pip3 install redis
RUN pip3 install tatsu
WORKDIR /opt/Flask-Socketio/example/
RUN pip3 install -r requirements.txt
RUN pip3 install gevent
WORKDIR /opt/Flask-Socketio/example
RUN mkdir static
RUN /bin/bash get_static_assets.sh
# An ENTRYPOINT allows you to configure a container that will run as an executable.
ENTRYPOINT ["/bin/bash"]

# There can only be one CMD instruction in a Dockerfile
# The CMD instruction should be used to run the software contained by your image, along with any arguments. 
CMD ["start.sh"]


