# Sets up a web server for deployment of web_static

exec {'update server':
  provider => shell,
  command  => 'sudo apt-get update -y'
}

package { 'nginx':
  ensure => installed,
  before => Exec['update server'],
}

file { '/data/':
  ensure => directory,
  group  => 'ubuntu',
  owner  => 'ubuntu'
}

file { '/data/web_static/':
  ensure => directory
}

file { '/data/web_static/releases/':
  ensure => directory
}

file { '/data/web_static/shared/':
  ensure => directory
}

file { '/data/web_static/releases/test/':
  ensure => directory
}

file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => 'Test web_static'
}

exec{ 'remove current':
  provider => shell,
  command  => 'test -L /data/web_static/current && rm -rf /data/web_static/current'
}
file { '/data/web_static/releases/current/':
  ensure => link,
  target => '/data/web_static/releases/test',
  before => Exec['remove current'],
}

exec { 'update nginx configuration':
  provider => shell,
  command  => 'sed -i "53i\ \n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default',
  notify   => Service['nginx'],
}

service { 'nginx':
  ensure => running
}
