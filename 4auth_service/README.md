## Быстрый старт

### Запуск сервиса
```bash
# Клонирование проекта (если еще не клонирован)
git clone <repository-url>
cd auth_service

# Запуск с помощью Docker одной командой
docker-compose up --build -d
```

### Проверка состояния запуска
```bash
# Проверка состояния сервисов
docker-compose ps

# Просмотр логов приложения
docker-compose logs app --tail=50

# Проверка работоспособности (health check)
curl http://localhost:8000/health
```

## Документация API
После запуска сервиса перейдите по следующему адресу, чтобы ознакомиться с полной документацией API:  
http://localhost:8000/docs


## Административные команды

### Остановка сервиса
```bash
docker-compose down
```

### Перезапуск сервиса
```bash
docker-compose restart
```

### Просмотр логов
```bash
# Просмотр логов всех сервисов
docker-compose logs

# Просмотр логов приложения в реальном времени
docker-compose logs app -f

# Просмотр логов базы данных
docker-compose logs db

# Просмотр логов Redis
docker-compose logs redis
```

### Сброс сервиса (удаление всех данных)
```bash
docker-compose down -v
docker-compose up --build -d
```