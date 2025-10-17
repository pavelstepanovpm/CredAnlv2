# Dockerfile для фронтенда системы аналитики кредитного портфеля
FROM node:16-alpine as build

# Установить рабочую директорию
WORKDIR /app

# Копировать package.json и package-lock.json
COPY package*.json ./

# Установить зависимости
RUN npm install --only=production

# Копировать исходный код
COPY . .

# Собрать приложение
RUN npm run build

# Production stage с nginx
FROM nginx:alpine

# Копировать собранное приложение
COPY --from=build /app/build /usr/share/nginx/html

# Копировать конфигурацию nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Открыть порт
EXPOSE 80

# Команда запуска
CMD ["nginx", "-g", "daemon off;"]
