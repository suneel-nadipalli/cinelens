FROM node:20-alpine

WORKDIR /app

EXPOSE 3000

COPY package.json package-lock.json ./

RUN npm install --silent

RUN npm install react-bootstrap bootstrap

RUN npm install -D prettier eslint-config-prettier eslint-plugin-prettier

COPY . ./ 

CMD ["npm", "start"]

