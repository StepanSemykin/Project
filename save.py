import json
import logging
import pandas as pd
import os

formatter = '[%(asctime)s: %(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, filename="save.log", filemode="w", format=formatter)


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
    logging.info(f'Start sereailization (save.py)')
    path = get_path(path_json)
    logging.info(f'Path: {path}')
    new_data = process_results(data)
    try: 
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f)
    except Exception as err:
        logging.error(f'{err} (save.py)') 
    logging.info('End serealization(save.py)')      


def deserialize_data(path_json: str) -> list:
    logging.info('Start desereailization (save.py)')
    path = get_path(path_json)
    logging.info(f'Path: {path}')
    try:
        with open(path) as f:
                data = json.load(f)
    except Exception as err:
        logging.error(f'{err} (save.py)')
    logging.info('End desereailization (save.py)')
    return data   


def convert_to_excel(path_json: str, path_excel: str) -> None:
    logging.info('Start convert excel (save.py)')
    path_json = get_path(path_json)
    logging.info(f'Path json: {path_json}')
    logging.info(f'Path excel: {path_excel}')
    try:
        pd.read_json(path_json).to_excel(path_excel)
    except Exception as err:
        logging.error(f'{err} (save.py)')
    logging.info('End convert excel (save.py)')


def get_path(path: str) -> str:
    base_path = os.path.dirname(__file__)
    valid_path = os.path.join(base_path, path)
    dir = os.path.dirname(valid_path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return valid_path    
