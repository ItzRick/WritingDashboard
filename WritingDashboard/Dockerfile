FROM node:16-bullseye-slim as build-stage
ENV NODE_ENV=production
WORKDIR /app
COPY ["package.json", "npm-shrinkwrap.json*", "./"]
RUN npm install --production --silent && mv node_modules ../
COPY ./public ./public
COPY ./src ./src
RUN chown -R node /app
USER node
RUN npm run build


FROM nginx:1.23
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build-stage /app/build .
COPY ./nginx.conf /etc/nginx/conf.d/configfile.template
COPY ./${SSL_KEY} /etc/nginx/certs/${SSL_KEY}
COPY ./${SSL_CERT} /etc/nginx/certs/${SSL_CERT}
EXPOSE $PORT
CMD sh -c "envsubst '\$PORT, \$URL, \$PORTHTTP, \$SSL_KEY, \$SSL_CERT, ' < /etc/nginx/conf.d/configfile.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"
