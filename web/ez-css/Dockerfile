FROM node:14

WORKDIR /app

COPY src/ ./
RUN npm install

EXPOSE 3000
CMD ["node", "index.js"]

ENV FLAG="MOCSCTF{Heavy_CS3_1s_d@ngerous}"