all:
	sudo apt install redis-server
	sudo pip3 install redis
	sudo pip3 install tatsu
	sudo python3 setup.py install
	sudo service redis-server stop
	rm -rf RedisJSON
	git clone https://github.com/RedisJSON/RedisJSON.git
	cd RedisJSON && make && redis-server --loadmodule src/rejson.so &

