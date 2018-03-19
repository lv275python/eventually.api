## Description
In this document are listed configuration files with settings for nginx and uWSGI.

## Technologies
* Nginx (1.10.3)
* uWSGI (2.0.15)

## Basic uWSGI installation and configuration
### Install uWSGI
```
pip install uwsgi
```
### Configuring uWSGI
Create a file called `eventually_uwsgi.ini` in folder `eventually.api/eventually/eventually/`:
```
[uwsgi]

chdir           = /home/adminaccount/eventually.api/eventually
module          = eventually.wsgi
master          = true
processes       = 10
max-requests = 500
--check-static /home/adminaccount/eventually.api/eventually/static
chmod-socket    = 664
clear environment on exit
vacuum          = true
```

Create a file called `uwsgi_params` in folder `eventually.api/eventually/eventually/`:
```
uwsgi_param  QUERY_STRING       $query_string;
uwsgi_param  REQUEST_METHOD     $request_method;
uwsgi_param  CONTENT_TYPE       $content_type;
uwsgi_param  CONTENT_LENGTH     $content_length;
uwsgi_param  REQUEST_URI        $request_uri;
uwsgi_param  PATH_INFO          $document_uri;
uwsgi_param  DOCUMENT_ROOT      $document_root;
uwsgi_param  SERVER_PROTOCOL    $server_protocol;
uwsgi_param  REQUEST_SCHEME     $scheme;
uwsgi_param  HTTPS              $https if_not_empty;
uwsgi_param  REMOTE_ADDR        $remote_addr;
uwsgi_param  REMOTE_PORT        $remote_port;
uwsgi_param  SERVER_PORT        $server_port;
uwsgi_param  SERVER_NAME        $server_name;
```
## Basic Nginx installation and configuration
### Install Nginx
```
sudo apt-get install nginx
sudo service nginx start   # start nginx
```
### Configure Nginx
Create a file called eventually_nginx.conf in the `~/eventually.api/eventually/eventually/` directory, and put this in it:
```
upstream django {
   server 127.0.0.1:8001;  # for a web port socket (we'll use this first)
}

server {
    listen 8000;
    client_max_body_size 75M;
    server_name eventlly.com;
    charset utf-8;
    location /media {
        alias /home/adminaccount/eventually.api/eventually/static/public;
    }
```
Symlink to this file from `/etc/nginx/sites-enabled` so Nginx can see it
```sudo ln -s ~/eventually.api/eventually/eventually/eventually_nginx.conf /etc/nginx/sites-enabled/```

## Editing project configuration
Edit `settings.py` in directory `~/eventually.api/eventually/eventually/` 
```STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/'),]```
Сhange to:
```STATIC_ROOT = os.path.join(BASE_DIR, "static/")```

# Run/stop project
### Start uWSGI processes
```
setsid uwsgi --socket :8001 --ini eventually_uwsgi.ini
```

### Kill uWSGI processes
```
pkill -f uwsgi -9
```