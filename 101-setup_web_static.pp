# Sets up a web server for deployment of web_static

exec {'update server':
  provider => shell,
  command  => 'sudo apt-get update -y'
}

package { 'nginx':
  ensure => installed,
  before => Exec['update server'],
}

exec { 'create /data/':
  provider => shell,
  command  => 'mkdir -p /data/web_static/releases/test/ /data/web_static/shared/'
}

exec { 'change owner':
  provider => shell,
  command  => 'sudo chown -hR ubuntu:ubuntu /data/'
}

file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => 'Test web_static'
}

exec { 'create current symlink':
  provider => shell,
  command  => 'ln -fs /data/web_static/releases/test/ /data/web_static/current'
}

exec { 'update nginx configuration':
  provider => shell,
  command  => 'sed -i "53i\ \n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default',
  notify   => Service['nginx'],
}

service { 'nginx':
  ensure => running
}
