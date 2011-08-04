server {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay off;

    listen 80;
    server_name {{ server_name }} www.{{ server_name }};
    access_log /var/log/nginx/{{ server_name }}-access.log;

    charset utf-8;
    keepalive_timeout 5;
    client_max_body_size 8m;

    gzip_types text/plain text/xml text/css application/javascript application/x-javascript application/json;

    location / {
        proxy_pass http://localhost:{{ gunicorn_port }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_redirect off;
    }

    location /static {
        root {{ django_path }};
        autoindex off;
        expires 1M;
    }

    location /static/admin {
        alias {{ env_path }}/lib/python2.6/site-packages/django/contrib/admin/media;
        autoindex off;
        expires 10m;
    }

    error_page  500 502 503 504  /50x.html;
    location = /50x.html {
        root {{ django_path }}/templates;
    }

    error_page  404  /404.html;

    location = /robots.txt {
        alias {{ django_path }}/static/robots.txt;
    }
}
