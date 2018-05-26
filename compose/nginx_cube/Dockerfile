FROM nginx

COPY compose/nginx_cube/nginx.conf /etc/nginx/nginx.conf
COPY compose/nginx_cube/static_production /static
COPY compose/nginx_cube/uwsgi_params /uwsgi_params
COPY compose/nginx_cube/static_root_data /static_root_data
COPY compose/nginx_cube/ssl /ssl
RUN mkdir -p /tmp/cache
RUN chmod -R 777 /tmp
EXPOSE 80
EXPOSE 8282
