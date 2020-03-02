all:
	sudo apt install redis-server
	sudo pip3 install redis
	sudo pip3 install tatsu
	sudo python3 setup.py install
	sudo service redis-server stop
	sudo apt install screen
	rm -rf RedisJSON
	git clone https://github.com/RedisJSON/RedisJSON.git
	cd RedisJSON && make 
	pwd
	cd RedisJSON && screen -d -m -S redis_server redis-server --loadmodule src/rejson.so &
	pwd
	cd example && /bin/bash start_app.sh
