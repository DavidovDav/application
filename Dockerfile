FROM nginx:1.19

RUN rm /etc/nginx/conf.d/*

COPY nginx.conf /etc/nginx/conf.d/

COPY ./flask/templates/index.html /usr/share/nginx/html/templates/index.html