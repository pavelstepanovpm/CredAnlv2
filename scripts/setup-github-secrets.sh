#!/bin/bash

# Скрипт для настройки GitHub Secrets
# Использование: ./scripts/setup-github-secrets.sh

set -e

# Конфигурация
REPO_OWNER="pavelstepanovpm"
REPO_NAME="CredAnlv2"
SERVER_HOST="87.228.88.77"
SERVER_USER="root"
PROJECT_PATH="/opt/credit-analytics"
SSH_KEY_PATH="~/.ssh/DSkey_project"

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
    
    # Проверка аутентификации
    if ! gh auth status &> /dev/null; then
        log_error "GitHub CLI не аутентифицирован"
        log_info "Выполните: gh auth login"
        exit 1
    fi
    
    log_success "GitHub CLI настроен"
}

# Получение SSH ключа
get_ssh_key() {
    log_info "Получение SSH ключа..."
    
    SSH_KEY_PATH_EXPANDED=$(eval echo $SSH_KEY_PATH)
    
    if [ ! -f "$SSH_KEY_PATH_EXPANDED" ]; then
        log_error "SSH ключ не найден: $SSH_KEY_PATH_EXPANDED"
        exit 1
    fi
    
    SSH_KEY_CONTENT=$(cat "$SSH_KEY_PATH_EXPANDED")
    log_success "SSH ключ получен"
}

# Настройка секретов
setup_secrets() {
    log_info "Настройка GitHub Secrets..."
    
    # SERVER_HOST
    log_info "Добавление SERVER_HOST..."
    echo "$SERVER_HOST" | gh secret set SERVER_HOST --repo "$REPO_OWNER/$REPO_NAME"
    log_success "SERVER_HOST добавлен"
    
    # SERVER_USER
    log_info "Добавление SERVER_USER..."
    echo "$SERVER_USER" | gh secret set SERVER_USER --repo "$REPO_OWNER/$REPO_NAME"
    log_success "SERVER_USER добавлен"
    
    # SERVER_SSH_KEY
    log_info "Добавление SERVER_SSH_KEY..."
    echo "$SSH_KEY_CONTENT" | gh secret set SERVER_SSH_KEY --repo "$REPO_OWNER/$REPO_NAME"
    log_success "SERVER_SSH_KEY добавлен"
    
    # PROJECT_PATH
    log_info "Добавление PROJECT_PATH..."
    echo "$PROJECT_PATH" | gh secret set PROJECT_PATH --repo "$REPO_OWNER/$REPO_NAME"
    log_success "PROJECT_PATH добавлен"
}

# Проверка секретов
verify_secrets() {
    log_info "Проверка настроенных секретов..."
    
    SECRETS=$(gh secret list --repo "$REPO_OWNER/$REPO_NAME")
    
    if echo "$SECRETS" | grep -q "SERVER_HOST"; then
        log_success "SERVER_HOST настроен"
    else
        log_error "SERVER_HOST не найден"
    fi
    
    if echo "$SECRETS" | grep -q "SERVER_USER"; then
        log_success "SERVER_USER настроен"
    else
        log_error "SERVER_USER не найден"
    fi
    
    if echo "$SECRETS" | grep -q "SERVER_SSH_KEY"; then
        log_success "SERVER_SSH_KEY настроен"
    else
        log_error "SERVER_SSH_KEY не найден"
    fi
    
    if echo "$SECRETS" | grep -q "PROJECT_PATH"; then
        log_success "PROJECT_PATH настроен"
    else
        log_error "PROJECT_PATH не найден"
    fi
}

# Тестирование развертывания
test_deployment() {
    log_info "Тестирование автоматического развертывания..."
    
    # Создать тестовый коммит
    echo "# Test deployment - $(date)" >> DEPLOYMENT_TEST.md
    git add DEPLOYMENT_TEST.md
    git commit -m "test: автоматическое развертывание $(date '+%Y-%m-%d %H:%M:%S')"
    
    log_info "Отправка тестового коммита..."
    git push origin main
    
    log_success "Тестовый коммит отправлен"
    log_info "Проверьте Actions в GitHub для мониторинга развертывания"
    log_info "URL: https://github.com/$REPO_OWNER/$REPO_NAME/actions"
}

# Основная функция
main() {
    echo "🔐 Настройка GitHub Secrets для автоматического развертывания"
    echo "=============================================================="
    echo "Репозиторий: $REPO_OWNER/$REPO_NAME"
    echo "Сервер: $SERVER_HOST"
    echo "Пользователь: $SERVER_USER"
    echo "Путь проекта: $PROJECT_PATH"
    echo "=============================================================="
    
    check_gh_cli
    get_ssh_key
    setup_secrets
    verify_secrets
    
    echo ""
    log_success "🎉 GitHub Secrets настроены успешно!"
    echo ""
    echo "📋 Настроенные секреты:"
    echo "   SERVER_HOST = $SERVER_HOST"
    echo "   SERVER_USER = $SERVER_USER"
    echo "   SERVER_SSH_KEY = [приватный ключ]"
    echo "   PROJECT_PATH = $PROJECT_PATH"
    echo ""
    
    read -p "Хотите протестировать автоматическое развертывание? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        test_deployment
    else
        log_info "Тестирование пропущено"
        log_info "Для тестирования выполните:"
        log_info "  git commit --allow-empty -m 'test: автоматическое развертывание'"
        log_info "  git push origin main"
    fi
    
    echo ""
    log_info "🌐 Проверьте Actions:"
    echo "   https://github.com/$REPO_OWNER/$REPO_NAME/actions"
    echo ""
    log_info "🔧 Управление секретами:"
    echo "   gh secret list --repo $REPO_OWNER/$REPO_NAME"
    echo "   gh secret delete SECRET_NAME --repo $REPO_OWNER/$REPO_NAME"
}

# Обработка аргументов командной строки
while [[ $# -gt 0 ]]; do
    case $1 in
        --repo)
            REPO_NAME="$2"
            shift 2
            ;;
        --owner)
            REPO_OWNER="$2"
            shift 2
            ;;
        --server)
            SERVER_HOST="$2"
            shift 2
            ;;
        --user)
            SERVER_USER="$2"
            shift 2
            ;;
        --path)
            PROJECT_PATH="$2"
            shift 2
            ;;
        --ssh-key)
            SSH_KEY_PATH="$2"
            shift 2
            ;;
        --help)
            echo "Использование: $0 [опции]"
            echo ""
            echo "Опции:"
            echo "  --repo REPO      Название репозитория (по умолчанию: CredAnlv2)"
            echo "  --owner OWNER    Владелец репозитория (по умолчанию: pavelstepanovpm)"
            echo "  --server HOST    IP адрес сервера (по умолчанию: 87.228.88.77)"
            echo "  --user USER      Пользователь SSH (по умолчанию: root)"
            echo "  --path PATH      Путь к проекту (по умолчанию: /opt/credit-analytics)"
            echo "  --ssh-key PATH   Путь к SSH ключу (по умолчанию: ~/.ssh/DSkey_project)"
            echo "  --help           Показать эту справку"
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
