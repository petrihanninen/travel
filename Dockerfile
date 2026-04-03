FROM python:3.12-alpine AS build

WORKDIR /app
COPY build.py .
COPY src/ src/

RUN python3 build.py

FROM nginx:alpine

COPY --from=build /app/dist/ /usr/share/nginx/html/
RUN find /usr/share/nginx/html -type d -exec chmod 755 {} + \
 && find /usr/share/nginx/html -type f -exec chmod 644 {} +

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
