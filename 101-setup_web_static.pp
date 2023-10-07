# Define variables
$nginx_config = @(EOL)
server {
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
}
EOL

# Update package list
package { 'nginx':
  ensure => 'installed',
}

# Create necessary directories
file { ['/data/web_static/releases/test/', '/data/web_static/shared/']:
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create a fake HTML file with the specified message
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => 'Devoops is not that easy',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

# Create a symbolic link to the /data/web_static/releases/test/ folder
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Manage Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => $nginx_config,
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
}

# Enable the Nginx site configuration
exec { 'enable_nginx_site':
  command => 'ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/',
  unless  => 'test -e /etc/nginx/sites-enabled/default',
  path    => ['/bin', '/usr/bin'],
}

# Restart Nginx to apply the changes
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}

