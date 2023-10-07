# web_server_setup.pp

# Install Nginx package
package { 'nginx':
  ensure => 'installed',
}

# Create directories
file { '/data/web_static/releases/test/':
  ensure => 'directory',
}

file { '/data/web_static/shared/':
  ensure => 'directory',
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => 'Devoops is not that easy',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

# Create a symbolic link
file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Define Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => template('path/to/nginx_config.erb'),
  notify  => Service['nginx'],
}

# Notify Nginx to restart when the configuration changes
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
}

# Print a message indicating the setup is complete
notify { 'web_server_setup_message':
  message => 'Web server setup for web_static deployment is complete.',
}

