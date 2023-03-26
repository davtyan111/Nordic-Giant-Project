FROM node:alpine

COPY package.json .
 
WORKDIR /app

RUN npm install -g npm@8.13.2

COPY .  . 

 EXPOSE 3000

 CMD [ "npm" , "start" , "build"]
