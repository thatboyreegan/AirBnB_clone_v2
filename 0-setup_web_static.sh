#!/usr/bin/env bash
# Sets up web servers for the dployment of web_static

[[ -z "$(which nginx)" ]] && {
	sudo apt-get update -yqq
	sudo apt-get install nginx -y
}

[[ ! -d /data/ ]] && {
	mkdir /data/
}

[[ ! -d /data/web_static ]] && {
	mkdir /data/web_static/
}

[[ ! -d /data/web_static/releases ]] && {
	mkdir /data/web_static/releases/
}

[[ ! -d /data/web_static/shared ]] && {
	mkdir /data/web_static/shared/
}

[[ ! -d /data/web_static/releases/test ]] && {
	mkdir /data/web_static/releases/test/
}

echo "Test web_static" > /data/web_static/releases/test/index.html

[[ -L /data/web_static/current ]] && rm -r /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sed -i "53i\ \n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default

sudo service nginx restart
