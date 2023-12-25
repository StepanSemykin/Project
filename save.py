import json
import pandas as pd


def to_int(string: str) -> int:
    return int(''.join(filter(str.isdigit, string)))


def process_results(data: list) -> list:
    new_data = []
    for i in data:
        if i[0] is None: 
            continue
        else: 
            name = i[0].replace('\n', ' ')  
        id = i[1]
        rating = 0 if i[2] == 'Нет оценок' else float(i[2])
        number_ratings = 0 if i[3] == '' else to_int(i[3])
        old_price = to_int(i[4])
        current_price = to_int(i[5])
        product = {'Наименование': name, 'Артикул': id, 'Рейтинг': rating, 
                   'Количество отзывов': number_ratings, 'Старая цена': old_price, 
                   'Текущая цена': current_price}
        new_data.append(product)
    return new_data


def serialize_data(data: list, path_json: str) -> None: 
    new_data = process_results(data)
    try: 
        with open(path_json, 'w', encoding='utf-8') as f:
            json.dump(new_data, f)
    except Exception as err:
        print(err)   


def deserialize_data(path_json: str) -> list:
    try:
        with open(path_json) as f:
                data = json.load(f)
    except Exception as err:
        print(err)
    return data   


def convert_to_excel(path_json: str, path_excel: str) -> None:
    pd.read_json(path_json).to_excel(path_excel)
