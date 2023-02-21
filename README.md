# API для Yamdb
Проект API для Yamdb является учебным, в рамках курса Яндекс "Python-разработчик"

### Описание проекта API для Yamdb

Проект YaMDb собирает отзывы пользователей на различные произведения.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

В данном проекте реализован REST API для проекта Yamdb, данные передаются в формате JSON.
Аутентификация по JWT-токену. 

#### Стек технологий
Проект написан на Python с использованием веб-фреймворка Django REST Framework.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ElenaL1/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
py -3.9 -m venv env - создание виртуального окружения(Windows)
python3 -m venv venv - создание виртуального окружения(linux, macOS)

```

```
source env/bin/activate - активация виртуального окружения(Windows)
source venv/bin/activate - активация виртуального окружения(linux, macOS)
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip - Обновление менеджера пвкетов PIP(Windows)
python3 -m pip install --upgrade pip - Обновление менеджера пвкетов PIP(linux, macOS)
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate (Windows)
python3 manage.py migrate (linux, macOS)
```

Импортировать базу данных:

```
python manage.py csv_to_bd (Windows)
python3 manage.py csv_to_bd (linux, macOS)
```

Запустить проект:

```
python manage.py runserver - Запуск локального сервера(Windows)
python3 manage.py runserver - Запуск локального сервера(linux, macOS)
```

### Примеры запросов

Ресурсы API YaMDb
- auth: аутентификация.
- users: пользователи.
- titles: произведения, к которым пишут отзывы.
- categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
- genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
- comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.

Более подробно информацию об эндпоинтах и примерах запросов и ответов можно посмотреть в 
```
/api_yamdb/api_yamdb/static/redoc.yaml
```