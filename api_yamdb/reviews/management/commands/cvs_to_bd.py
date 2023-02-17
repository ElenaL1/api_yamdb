# Файл вызывается командой python manage.py cvs_to_bd.py
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Comment, Genre, Title, User
import csv
import pandas as pd

data = pd.read_csv('file.csv', sep=',')
def handle_files(f):
    reader = csv.DictReader(open(f))
    for row in reader:
        id=row['id']
        age=row['age']
        height=row['height']
        my_object = MyObject(id=id, age=age,height=height)
        my_object.save()

with open('names.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['first_name'], row['last_name'])

class Command(BaseCommand):
    
    help = 'Загрузка данных в базу из cvs-файлов'

    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for poll_id in options['poll_ids']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))