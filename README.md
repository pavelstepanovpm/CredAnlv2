# Система аналитики кредитного портфеля

Современная система для анализа кредитного портфеля с возможностью моделирования различных сценариев изменения параметров кредитования.

## 🚀 Основные возможности

- **Консолидация данных** по кредитному портфелю
- **Расчет прогнозных графиков** платежей с использованием Quantlib
- **Сценарное моделирование** денежных потоков
- **Визуализация ключевых метрик** портфеля
- **Управление версиями** расчетов
- **Современный React/TypeScript интерфейс** в стиле трейдинговых терминалов

## 🏗️ Архитектура

### Backend (Python/FastAPI)
- **FastAPI** - современный веб-фреймворк
- **Quantlib** - библиотека финансовых расчетов
- **Pydantic** - валидация данных
- **SQLAlchemy** - ORM для работы с БД

### Frontend (React/TypeScript)
- **React 18** - пользовательский интерфейс
- **TypeScript** - типизация
- **Material-UI** - компоненты интерфейса
- **Recharts** - графики и визуализация
- **Redux Toolkit** - управление состоянием

## 📦 Установка и запуск

### Предварительные требования
- Python 3.8+
- Node.js 16+
- npm или yarn

### 1. Установка зависимостей бэкенда

```bash
# Установка Python зависимостей
pip install -r backend/requirements.txt
```

### 2. Установка зависимостей фронтенда

```bash
# Переход в директорию фронтенда
cd frontend

# Установка зависимостей
npm install
```

### 3. Запуск системы

#### 🚀 Единый запуск (рекомендуется)

**Способ 1: Python скрипт**
```bash
# Из корневой директории проекта
python start_system.py
```

**Способ 2: Bash скрипт**
```bash
# Из корневой директории проекта
./start_system.sh
```

**Способ 3: Быстрый запуск**
```bash
# Автоматически выберет лучший способ
python start.py
```

#### 🔧 Ручной запуск (по компонентам)

**Запуск бэкенда:**
```bash
python run_backend.py
```

**Запуск фронтенда:**
```bash
./run_frontend.sh
# или
cd frontend && npm start
```

#### 🌐 Адреса системы

После запуска система будет доступна по адресам:
- **Фронтенд**: http://localhost:3000
- **Бэкенд API**: http://localhost:8000
- **API документация**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

## 📁 Структура проекта

```
CredAnlv2/
├── backend/                 # Python/FastAPI бэкенд
│   ├── main.py             # Основной файл приложения
│   └── requirements.txt     # Python зависимости
├── frontend/               # React/TypeScript фронтенд
│   ├── src/
│   │   ├── components/     # React компоненты
│   │   ├── pages/         # Страницы приложения
│   │   ├── store/         # Redux store
│   │   ├── services/      # API сервисы
│   │   └── types/         # TypeScript типы
│   ├── package.json       # Node.js зависимости
│   └── tsconfig.json      # TypeScript конфигурация
├── models/                # Модели данных
├── api/                   # API клиенты
├── calculations/         # Движок расчетов
├── portfolio/             # Консолидация портфеля
├── versions/              # Управление версиями
├── visualization/         # Визуализация данных
├── run_backend.py         # Скрипт запуска бэкенда
├── run_frontend.sh        # Скрипт запуска фронтенда
└── README.md              # Документация
```

## 🔧 Конфигурация

### Переменные окружения

Создайте файл `.env` в корневой директории:

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api
TREASURY_API_URL=http://localhost:8001/api
TREASURY_API_KEY=your-api-key-here

# Database (если используется)
DATABASE_URL=sqlite:///./portfolio.db
```

## 📊 Основные компоненты

### Модели данных
- `CreditContract` - кредитные договоры
- `Drawdown` - выборки (транши)
- `Repayment` - погашения
- `CalculationVersion` - версии расчетов
- `PortfolioCashflow` - кэш-флоу портфеля

### API Endpoints
- `GET /api/portfolio/data` - данные портфеля
- `GET /api/portfolio/metrics/{version_id}` - метрики портфеля
- `GET /api/versions` - список версий
- `POST /api/versions` - создание версии
- `POST /api/scenarios` - создание сценария

### React компоненты
- `Dashboard` - главная страница с метриками
- `Portfolio` - управление портфелем
- `Scenarios` - сценарное моделирование
- `Reports` - генерация отчетов
- `Settings` - настройки системы

## 🎨 Особенности интерфейса

- **Темная тема** в стиле трейдинговых терминалов
- **Адаптивный дизайн** для различных устройств
- **Интерактивные графики** с использованием Recharts
- **Реальное время** обновления данных
- **Современная типографика** и иконки

## 🚀 Разработка

### Добавление новых компонентов

1. **Backend**: Добавьте новые модели в `models/`, API endpoints в `backend/main.py`
2. **Frontend**: Создайте компоненты в `frontend/src/components/`, страницы в `frontend/src/pages/`

### Тестирование

```bash
# Backend тесты
python -m pytest backend/tests/

# Frontend тесты
cd frontend
npm test
```

## 📝 Лицензия

Проект разработан для внутреннего использования.
