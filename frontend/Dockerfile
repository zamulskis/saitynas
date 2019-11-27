FROM node:12.9.1

WORKDIR /frontend

COPY package*.json ./

RUN npm ci -qy

COPY . /frontend

EXPOSE 3000

CMD ["npm", "start"]