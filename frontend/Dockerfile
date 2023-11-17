FROM node:14

RUN mkdir -p /frontend_app

WORKDIR /frontend_app

COPY package.json .

COPY package-lock.json .

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
