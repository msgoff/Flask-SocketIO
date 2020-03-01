all:
	sudo apt install redis-server
	#virtualenv venv -p python3.7
	sudo pip3 install redis
	sudo pip3 install tatsu
	sudo python3 setup.py install
	sudo service redis-server stop
	git clone https://github.com/RedisJSON/RedisJSON.git
	cd RedisJSON
	make
	redis-server --loadmodule src/rejson.so &



