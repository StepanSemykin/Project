import pandas as pd
import matplotlib.pyplot as plt
from save import deserialize_data

DEFAULT_PATH = '.\\Files\\result.json'


def draw_hist():
    data = deserialize_data(DEFAULT_PATH)
    df = pd.DataFrame(data)
    high, bin_edges, intervals = plt.hist(df['Текущая цена'], edgecolor='black', color="green", alpha=0.8)

    plt.xlabel("Цена")
    plt.ylabel("Количество товаров")
    plt.title('Гистограмма цен на товары')
    plt.show()


if __name__ == '__main__':\
    draw_hist()