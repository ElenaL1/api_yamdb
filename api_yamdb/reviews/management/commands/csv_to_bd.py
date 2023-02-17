# Файл вызывается командой python manage.py csv_to_bd
from django.core.management.base import BaseCommand

import pandas as pd
import os
from sqlalchemy import create_engine

from api_yamdb.settings import CSV_FILES_DIR
from reviews.models import (Category, Comment, Genre,
                            GenreTitle, Title, Review, User)

FILES_MODELS = {
    'category.csv': Category,
    'comments.csv': Comment,
    'genre_title.csv': GenreTitle,
    'genre.csv': Genre,
    'review.csv': Review,
    'titles.csv': Title,
    'users.csv': User,
}


class Command(BaseCommand):
    help = 'Загрузка данных в базу из csv-файлов'

    def handle(self, *args, **options):
        for csv_file, model in FILES_MODELS.items():
            csv_path = os.path.join(CSV_FILES_DIR, csv_file)
            data = pd.read_csv(csv_path)
            engine = create_engine('sqlite:///db.sqlite3')
            data.to_sql(model._meta.db_table, if_exists='replace',
                        con=engine, index=False)
        print('Данные из csv-файлов записаны в базу')
