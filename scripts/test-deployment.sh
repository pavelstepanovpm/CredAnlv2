#!/bin/bash

# Скрипт для тестирования автоматического развертывания
# Использование: ./scripts/test-deployment.sh

set -e

# Конфигурация
REPO_OWNER="pavelstepanovpm"
REPO_NAME="CredAnlv2"
SERVER_HOST="87.228.88.77"

# Цвета
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Проверка GitHub CLI
check_gh_cli() {
    log_info "Проверка GitHub CLI..."
    
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI не установлен"
        log_info "Установите GitHub CLI:"
        log_info "  brew install gh"
        log_info "  gh auth login"
        exit 1
    fi
    
    if ! gh auth status &> /dev/null; then
        log_error "GitHub CLI не аутентифицирован"
        log_info "Выполните: gh auth login"
        exit 1
    fi
    
    log_success "GitHub CLI настроен"
}

# Проверка работоспособности сервисов
check_services() {
    log_info "Проверка работоспособности сервисов..."
    
    # Проверка Frontend
    log_info "Проверка Frontend (http://$SERVER_HOST:3002)..."
    if curl -f -s "http://$SERVER_HOST:3002" > /dev/null; then
        log_success "Frontend работает"
    else
        log_error "Frontend недоступен"
        return 1
    fi
    
    # Проверка Backend
    log_info "Проверка Backend (http://$SERVER_HOST:8001/docs)..."
    if curl -f -s "http://$SERVER_HOST:8001/docs" > /dev/null; then
        log_success "Backend работает"
    else
        log_error "Backend недоступен"
        return 1
    fi
    
    # Проверка API health
    log_info "Проверка API health..."
    if curl -f -s "http://$SERVER_HOST:8001/health" > /dev/null; then
        log_success "API health check прошел"
    else
        log_warning "API health check недоступен (это нормально, если endpoint не реализован)"
    fi
}

# Создание тестового коммита
create_test_commit() {
    log_info "Создание тестового коммита..."
    
    # Создать файл с информацией о тесте
    cat > DEPLOYMENT_TEST.md << EOF
# 🧪 Тест автоматического развертывания

- **Дата**: $(date '+%Y-%m-%d %H:%M:%S')
- **Коммит**: $(git rev-parse --short HEAD)
- **Ветка**: $(git branch --show-current)
- **Пользователь**: $(git config user.name)
- **Email**: $(git config user.email)

## 🎯 Цель теста
Проверить работу автоматического развертывания через GitHub Actions.

## 📊 Результат
Тест будет считаться успешным, если:
- ✅ GitHub Actions workflow выполнится без ошибок
- ✅ Frontend будет доступен по адресу: http://$SERVER_HOST:3002
- ✅ Backend API будет доступен по адресу: http://$SERVER_HOST:8001/docs
- ✅ Все контейнеры будут запущены и работать

---
*Тест создан автоматически скриптом test-deployment.sh*
EOF
    
    # Добавить файл в git
    git add DEPLOYMENT_TEST.md
    
    # Создать коммит
    git commit -m "test: автоматическое развертывание $(date '+%Y-%m-%d %H:%M:%S')"
    
    log_success "Тестовый коммит создан"
}

# Отправка коммита
push_commit() {
    log_info "Отправка коммита в репозиторий..."
    
    git push origin main
    
    log_success "Коммит отправлен"
}

# Мониторинг развертывания
monitor_deployment() {
    log_info "Мониторинг развертывания..."
    
    # Получить URL для Actions
    ACTIONS_URL="https://github.com/$REPO_OWNER/$REPO_NAME/actions"
    
    log_info "Откройте в браузере: $ACTIONS_URL"
    log_info "Ожидание завершения развертывания..."
    
    # Ожидание с индикатором прогресса
    for i in {1..30}; do
        echo -n "."
        sleep 10
    done
    echo ""
    
    log_info "Проверка результата развертывания..."
    check_services
}

# Показать информацию о развертывании
show_deployment_info() {
    echo ""
    log_success "🎉 Тест развертывания завершен!"
    echo ""
    echo "📊 Информация о развертывании:"
    echo "   🌐 Frontend: http://$SERVER_HOST:3002"
    echo "   🔧 Backend: http://$SERVER_HOST:8001/docs"
    echo "   📋 Actions: https://github.com/$REPO_OWNER/$REPO_NAME/actions"
    echo ""
    echo "🔧 Управление на сервере:"
    echo "   ssh -i ~/.ssh/DSkey_project root@$SERVER_HOST"
    echo "   cd /opt/credit-analytics"
    echo "   docker-compose ps"
    echo "   docker-compose logs -f"
    echo ""
}

# Основная функция
main() {
    echo "🧪 Тестирование автоматического развертывания"
    echo "=============================================="
    echo "Репозиторий: $REPO_OWNER/$REPO_NAME"
    echo "Сервер: $SERVER_HOST"
    echo "=============================================="
    
    # Проверка текущего состояния
    log_info "Проверка текущего состояния сервисов..."
    if check_services; then
        log_success "Все сервисы работают"
    else
        log_warning "Некоторые сервисы недоступны"
    fi
    
    # Проверка GitHub CLI
    check_gh_cli
    
    # Создание тестового коммита
    create_test_commit
    
    # Отправка коммита
    push_commit
    
    # Мониторинг развертывания
    monitor_deployment
    
    # Показать информацию
    show_deployment_info
}

# Обработка аргументов
while [[ $# -gt 0 ]]; do
    case $1 in
        --check-only)
            log_info "Проверка только текущего состояния..."
            check_services
            exit 0
            ;;
        --help)
            echo "Использование: $0 [опции]"
            echo ""
            echo "Опции:"
            echo "  --check-only    Проверить только текущее состояние сервисов"
            echo "  --help          Показать эту справку"
            exit 0
            ;;
        *)
            log_error "Неизвестная опция: $1"
            echo "Используйте --help для справки"
            exit 1
            ;;
    esac
done

# Запуск основной функции
main
