FROM nginx:1.23
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY  ./build .
COPY ./default.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
