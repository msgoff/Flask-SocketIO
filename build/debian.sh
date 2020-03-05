# https://docs.docker.com/engine/reference/builder/#from
# https://github.com/phusion/baseimage-docker


# https://docs.docker.com/engine/reference/builder/#run
sudo apt-get update && \
    apt-get install -y \
    redis-server \
    gcc \
    git \ 
    make \
    graphviz \
    python3-dev \
    python-dev \
    python3-pip 

cd /opt/
sudo service redis-server stop
sudo cd /opt/
sudo git clone https://github.com/RedisJSON/RedisJSON.git
sudo cd /opt/RedisJSON && make
sudo cd /opt/
sudo git clone https://github.com/msgoff/Flask-Socketio
sudo cd Flask-Socketio
sudo pip3 install redis
sudo pip3 install tatsu
cd /opt/Flask-Socketio/example/
sudo pip3 install -r requirements.txt
sudo pip3 install gevent
cd /opt/Flask-Socketio/example
/bin/bash start.sh