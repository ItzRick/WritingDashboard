FROM nginx:1.23
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY  ./build .

COPY ./default.conf /etc/nginx/conf.d/configfile.template
EXPOSE 8080
EXPOSE 443
CMD sh -c "envsubst '\$PORT' < /etc/nginx/conf.d/configfile.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"
