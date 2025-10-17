#!/bin/bash

# Скрипт для получения SSH ключа для GitHub Secrets
# Использование: ./scripts/get-ssh-key.sh

set -e

# Конфигурация
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

# Получение SSH ключа
get_ssh_key() {
    log_info "Получение SSH ключа..."
    
    SSH_KEY_PATH_EXPANDED=$(eval echo $SSH_KEY_PATH)
    
    if [ ! -f "$SSH_KEY_PATH_EXPANDED" ]; then
        log_error "SSH ключ не найден: $SSH_KEY_PATH_EXPANDED"
        log_info "Убедитесь, что ключ существует и путь указан верно"
        exit 1
    fi
    
    SSH_KEY_CONTENT=$(cat "$SSH_KEY_PATH_EXPANDED")
    
    log_success "SSH ключ получен"
    
    echo ""
    log_info "📋 Содержимое SSH ключа для GitHub Secret SERVER_SSH_KEY:"
    echo "================================================================"
    echo "$SSH_KEY_CONTENT"
    echo "================================================================"
    echo ""
    
    log_warning "⚠️  ВАЖНО:"
    echo "1. Скопируйте ВЕСЬ текст выше (включая BEGIN и END строки)"
    echo "2. Вставьте его в GitHub Secret с именем 'SERVER_SSH_KEY'"
    echo "3. НЕ добавляйте лишних пробелов или переносов строк"
    echo ""
    
    # Создать временный файл с ключом
    TEMP_FILE="/tmp/ssh_key_for_github.txt"
    echo "$SSH_KEY_CONTENT" > "$TEMP_FILE"
    
    log_info "💾 SSH ключ также сохранен в: $TEMP_FILE"
    log_info "Вы можете скопировать его оттуда:"
    echo "   cat $TEMP_FILE | pbcopy"
    echo ""
}

# Показать инструкции
show_instructions() {
    log_info "📖 Инструкции по настройке GitHub Secrets:"
    echo ""
    echo "1. Откройте: https://github.com/pavelstepanovpm/CredAnlv2/settings/secrets/actions"
    echo "2. Нажмите 'New repository secret'"
    echo "3. Добавьте следующие секреты:"
    echo ""
    echo "   Name: SERVER_HOST"
    echo "   Secret: 87.228.88.77"
    echo ""
    echo "   Name: SERVER_USER"
    echo "   Secret: root"
    echo ""
    echo "   Name: SERVER_SSH_KEY"
    echo "   Secret: [содержимое SSH ключа выше]"
    echo ""
    echo "   Name: PROJECT_PATH"
    echo "   Secret: /opt/credit-analytics"
    echo ""
    log_info "📚 Подробная инструкция: MANUAL_GITHUB_SECRETS_SETUP.md"
    echo ""
}

# Основная функция
main() {
    echo "🔑 Получение SSH ключа для GitHub Secrets"
    echo "=========================================="
    
    get_ssh_key
    show_instructions
    
    log_success "🎉 SSH ключ готов для использования!"
    echo ""
    log_info "🚀 После настройки секретов протестируйте развертывание:"
    echo "   git commit --allow-empty -m 'test: автоматическое развертывание'"
    echo "   git push origin main"
    echo ""
    log_info "📊 Мониторинг: https://github.com/pavelstepanovpm/CredAnlv2/actions"
}

# Обработка аргументов
while [[ $# -gt 0 ]]; do
    case $1 in
        --key-path)
            SSH_KEY_PATH="$2"
            shift 2
            ;;
        --help)
            echo "Использование: $0 [опции]"
            echo ""
            echo "Опции:"
            echo "  --key-path PATH   Путь к SSH ключу (по умолчанию: ~/.ssh/DSkey_project)"
            echo "  --help            Показать эту справку"
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
