FROM node:22
ENV NEXT_TELEMETRY_DISABLED=1
RUN mkdir /app
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
CMD [ "npm", "run", "dev" ]
