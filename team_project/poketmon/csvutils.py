import csv
import pandas as pd
from poketmon.models import monster


def read_csv(file_path):
    data = []
    with open(file_path, 'r', encoding='cp949') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def save_to_model(data):
    for item in data:
        monster.objects.create(
            name=item['name'],
            type=item['type'],
            height=item['height'],
            classify=item['classify'],
            gender=item['gender'],
            weight=item['weight'],
            ability=item['ability'],
            description=item['description'],
            evolution=item['evolution'],
            img=item['img'],
        )
