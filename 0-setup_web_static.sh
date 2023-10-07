#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.

# Define the username as a variable
user="ubuntu"

# Update the package list
sudo apt-get update

# Install Nginx if not already installed
sudo apt-get install -y nginx

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file with the specified message
echo "Devoops is not that easy" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link to the /data/web_static/releases/test/ folder
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership of the /data/ directory and its contents recursively to the defined user
sudo chown -R "$user" /data/
sudo chgrp -R "$user" /data/

# Define the Nginx configuration for serving web_static content
nginx_config="server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"

# Add the Nginx configuration to the default Nginx site configuration
echo "$nginx_config" | sudo tee /etc/nginx/sites-available/default

# Restart Nginx to apply the changes
sudo service nginx restart

# Print a message to indicate the setup is complete
echo "Web server setup for web_static deployment is complete."
