FROM python:3.12-alpine AS build

WORKDIR /app
COPY build.py .
COPY src/ src/

RUN python3 build.py

FROM nginx:alpine

COPY --from=build --chmod=644 /app/dist/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
