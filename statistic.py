import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from save import deserialize_data

DEFAULT_PATH = '.\\Files\\result.json'


def draw_graphs() -> None:
    data = deserialize_data(DEFAULT_PATH)
    df = pd.DataFrame(data)

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    high, bin_edges, intervals = axes[0, 0].hist(df['Текущая цена'], edgecolor='black', color='green', alpha=0.8)
    plt.subplot(2, 2, 1)
    plt.xticks(bin_edges)
    plt.gca().xaxis.set_major_formatter('{:.0f}'.format)
    plt.xlabel('Цена')
    plt.ylabel('Количество товаров')
    plt.title('Гистограмма цен на товары')

    mean_price = int(np.mean(df['Текущая цена']))
    min = np.min(df['Текущая цена'])
    max = np.max(df['Текущая цена'])
    r = max - min
    s = int(np.sqrt(np.var(df['Текущая цена'], ddof=2)))
    size = df['Текущая цена'].size
    plt.subplot(2, 2, 2)
    plt.text(0.3, 0.5, f'Количество товаров: {size}\nМинимальная цена: {min}\nМаксимальная цена: {max} \
             \nСредняя цена: {mean_price}\nРазмах: {r}\nСтандартное отклонение: {s}', 
             style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

    params = axes[1, 0].boxplot(df['Текущая цена'], vert=False)
    medians = [median.get_xdata()[0] for median in params['medians']]
    whiskers = [whiscer.get_xdata() for whiscer in params['whiskers']]
    arr = np.array(whiskers[0])
    arr = np.append(arr, whiskers[1])
    arr = np.append(arr, medians)
    plt.subplot(2, 2, 3)
    plt.xticks(ticks=arr)
    plt.gca().xaxis.set_major_formatter('{:.0f}'.format)
    plt.xlabel('Цена')
    plt.title('Боксплот цен на товары')

    mean_price = np.mean(df['Текущая цена'])
    min = np.min(df['Текущая цена'])
    max = np.max(df['Текущая цена'])
    plt.subplot(2, 2, 2)

    axes[1, 1].scatter(df['Рейтинг'], df['Текущая цена'])
    plt.subplot(2, 2, 4)
    plt.xlabel('Рейтинг')
    plt.ylabel('Цена')
    plt.title('Зависимость рейтинга товара от его цены')

    plt.show()


if __name__ == '__main__':
    draw_graphs()