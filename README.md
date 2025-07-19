# BAOTAO on Django,  Shop + Ticketing and Ordering System

##Описание

Это тестовое задание — полноценное Django-приложение с:

- регистрацией пользователей;
- разделением прав через админку;
- созданием заказов и тикетов;
- скрытой логикой связи тикет ↔ товар;
- обновлением статуса тикета через API;
- визуальным и API-интерфейсом.

---

## Стркутура
```
myproject/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── authentification/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── apps.py
│   ├── permissions.py
│   ├── templates/
│   │   ├── authentification/
│   │   │   └── dashboard.html
│   │   │   └── login.html
│   │   │   └── signup.html
│   │   └── auth_about.html
│   └── urls.py
├── shop/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── templates/
│   │   ├── registration/
│   │   │   └── signup.html
│   │   │   └── login.html
│   │   └── catalogue.html
│   └── urls.py
└── README.md
```



## 📦 Функциональность

### Пользователи могут:

- Зарегистрироваться, войти
- Оформлять заказы по номеру телефона
- Просматривать свои заказы и их статус

### Администраторы могут:

- Управлять товарами, заказами и тикетами через админку
- Назначать права пользователям через группы
- Обновлять статусы тикетов вручную или через API

---

## Установка

### 0. В .env напишите свой DJANGO_SECRET_KEY

### 1. Клонировать проект и перейти в директорию

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject

### 2. Создать виртуальное окружение и активировать

```
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```
### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Запуск
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Аутентификация
Страницы:
Регистрация: /signup/
Вход: /auth/login/
Выход: /auth/logout/

## Админка

Через /admin/ можно добавлять пользователей в группы:

Менеджеры — полный доступ

Пользователи — только к своим заказам

В API и UI пользователи видят только свои данные, админы — все.

## Модели

### Order
| Поле          | Описание                         |
| ------------- | -------------------------------- |
| user          | Пользователь                     |
| phone\_number | Телефон                          |
| comment       | Комментарий к заказу             |
| status        | `PENDING`, `IN_PROGRESS`, `DONE` |
| tickets       | Все тикеты, связанные с заказом  |

### Ticket

| Поле           | Описание                                 |
| -------------- | ---------------------------------------- |
| order          | К какому заказу относится                |
| product\_codes | Список кодов товаров (JSON-массив)       |
| status         | Статус: `PENDING`, `IN_PROGRESS`, `DONE` |
| created_at    | Когда создан                             |

## API

Все эндпоинты доступны через /api/
| Эндпоинт                           | Метод | Описание                     |
| ---------------------------------- | ----- | ---------------------------- |
| `/api/products/`                   | GET   | Список всех товаров          |
| `/api/orders/`                     | GET   | Заказы текущего пользователя |
| `/api/orders/`                     | POST  | Создать заказ                |
| `/api/tickets/`                    | GET   | Список тикетов               |
| `/api/tickets/<id>/update_status/` | POST  | Обновить статус тикета       |

## UI
| URL                | Описание                             |
| ------------------ | ------------------------------------ |
| `/`                | Главная страница                     |
| `/catalogue/`      | Каталог товаров с кнопкой покупки    |
| `/orders/`         | Список заказов текущего пользователя |
| `/signup/`         | Регистрация                          |
| `/accounts/login/` | Вход                                 |
| `/admin/`          | Админка                              |
