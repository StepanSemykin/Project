import json


def to_int(string: str) -> int:
    return int(''.join(filter(str.isdigit, string)))


def process_results(data: list) -> list:
    new_data = []
    for i in data:
        name = i[0].replace('\n', ' ') if i[0] is not None else None
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


if __name__ == "__main__":
    a = [['S20FE\nСмартфон Samsung Galaxy S20 FE Resale', '158616144', '4.3', '6 оценок', '33 000 ?', '29 106 ?'], ['Samsung\nЗадняя крышка Samsung A107F (Galaxy A10S) Черная', '87251353', '1', '1 оценка', '1 200 ?', '478 ?'], 
     ['S20FE\nСмартфон Samsung Galaxy S20 FE Resale', '158616146', '4.3', '6 оценок', '33 000 ?', '27 621 ?'], ['Samsung\nЗащитное стекло на Samsung Galaxy A52 A51 самсунг А51 А52', '108747547', '4.6', '836 оценок', '245 ?', '154 ?'], 
     [None, 4], [None, 5], ['Samsung\nАккумулятор Samsung IA-BH125C / BH-125C / BH125C', '113384144', 'Нет оценок', '', '1 913 ?', '946 ?'], ['Samsung\nЗащитное стекло на samsung а51/а52', '50722198', '5', '2 843 оценки', '331 ?', '139 ?'], 
     ['Samsung\nСмартфон Samsung Galaxy A14 4/128GB', '178853188', '5', '55 оценок', '18 440 ?', '14 106 ?'], ['Samsung\nАдаптер тайпси, оригинал самсунг 45W', '97330930', '4', '213 оценок', '1 490 ?', '566 ?'], [None, 10], 
     ['S20FE\nСмартфон Samsung Galaxy S20 FE Resale', '158616145', '4.3', '6 оценок', '33 000 ?', '29 700 ?'], ['Samsung\nСмартфон Galaxy A14 4/64GB', '189802451', '4.7', '55 оценок', '17 002 ?', '13 006 ?'], 
     ['Samsung\nСмартфон Galaxy A14 4/64GB', '189802456', '4.7', '55 оценок', '16 594 ?', '12 694 ?'], ['Samsung\nЧехол на Samsung Galaxy S20 FE с принтом', '195996998', 'Нет оценок', '', '999 ?', '349 ?'], 
     ['Samsung\nЧехол на Samsung Galaxy S20 FE с принтом', '195997003', 'Нет оценок', '', '999 ?', '349 ?'], [None, 16], [None, 17], ['Samsung\nЧехол на Samsung Galaxy S20 FE с принтом', '195996994', 'Нет оценок', '', '999 ?', '349 ?'], 
     ['Samsung\nЧехол на Samsung Galaxy S20 с принтом', '196003433', 'Нет оценок', '', '999 ?', '339 ?']]
    path = 'Files\\result.json'
    serialize_data(a, path)
    b = deserialize_data(path)
    print(b)