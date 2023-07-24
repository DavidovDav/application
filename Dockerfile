FROM nginx:1.19

EXPOSE 80

RUN rm /etc/nginx/conf.d/*

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY ./flask/templates/index.html /usr/share/nginx/html/templates/index.html
