FROM node:latest as build-step

RUN mkdir app
WORKDIR /app

COPY package*.json ./
COPY tsconfig.json ./

RUN npm install

ADD . ./
ENV TZ="America/New_York"
CMD ["npm", "run", "start"]




