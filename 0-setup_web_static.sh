#!/usr/bin/env bash
# Sets up web servers for the dployment of web_static

[[ -z "$(which nginx)" ]] && {
	sudo apt-get update -yqq
	sudo apt-get install nginx -y
}

sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

echo "Test web_static" | sudo tee /data/web_static/releases/test/index.html > /dev/null

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -hR ubuntu:ubuntu /data/

sudo sed -i "53i\ \n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default

sudo service nginx restart
