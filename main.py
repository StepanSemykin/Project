import os
import sys
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QLabel, QComboBox,
                             QMainWindow, QPushButton, QFileDialog,
                             QWidget, QLineEdit, QMessageBox)
from WBparser import extract_data
from save import serialize_data, convert_to_excel
from statistic import draw_graphs

SORT_METHODS = {0: 'popular', 1: 'rate', 2: 'priceup',
                3: 'pricedown', 4: 'newly', 5: 'benefit'}
DEFAULT_PATH = '.\\Files\\result.json'


class GraphicalInterface(QMainWindow):
    def __init__(self) -> None:
        """Initializates of the application window.
        """
        super(GraphicalInterface, self).__init__()
        self.setWindowTitle('WB Parser')
        self.setFixedSize(450, 420)
        self.move(800, 200)
        self.setFont(QFont('Arial', 14))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.intro = QLabel('Вас приветствует система для автоматизированного \
                            сбора данных о товарах с маркетплейса Wildberries',
                            self.central_widget)
        self.intro.setGeometry(50, -90, 350, 300)
        self.intro.setWordWrap(True)
        self.intro.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.name_label = QLabel(
            'Наименование товара:', self.central_widget)
        self.name_label.setGeometry(10, 130, 170, 45)
        self.name_label.setWordWrap(True)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_input = QLineEdit(self.central_widget)
        self.name_input.setGeometry(190, 130, 250, 45)

        self.quantity_label = QLabel(
            'Количество товаров:', self.central_widget)
        self.quantity_label.setGeometry(10, 200, 170, 45)
        self.quantity_label.setWordWrap(True)
        self.quantity_label.setAlignment(Qt.AlignCenter)
        self.quantity_input = QLineEdit(self.central_widget)
        self.quantity_input.setGeometry(190, 200, 250, 45)

        self.sort_label = QLabel('Способ сортировки:', self.central_widget)
        self.sort_label.setGeometry(10, 270, 170, 45)
        self.sort_label.setWordWrap(True)
        self.sort_label.setAlignment(Qt.AlignCenter)
        self.sort_input = QComboBox(self.central_widget)
        self.sort_input.setGeometry(190, 270, 250, 45)
        self.sort_input.addItems(['По популярности', 'По рейтингу',
                                  'По возрастанию цены', 'По убыванию цены',
                                  'По новинкам', 'Сначала выгодные'])

        self.start_parser = QPushButton('НАЧАТЬ', self.central_widget)
        self.start_parser.setToolTip('Начинает загрузку товаров с сайта')
        self.start_parser.setGeometry(175, 350, 100, 40)
        self.start_parser.clicked.connect(self.start_program)

        self.workerThread = None

    def is_fill(self, name: str, quantity: str) -> bool:
        return True if name and quantity else False

    def start_program(self) -> None:
        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()
        sort = self.sort_input.currentIndex()
        if self.is_fill(name, quantity):
            self.data = extract_data(name,  sort, int(quantity))
            serialize_data(self.data, DEFAULT_PATH)

            # self.data = [['S20FE\nСмартфон Samsung Galaxy S20 FE Resale', '158616144', '4.3', '6 оценок', '33 000 ?', '29 106 ?'], ['Samsung\nЗадняя крышка Samsung A107F (Galaxy A10S) Черная', '87251353', '1', '1 оценка', '1 200 ?', '478 ?'],
            #              ['S20FE\nСмартфон Samsung Galaxy S20 FE Resale', '158616146', '4.3', '6 оценок', '33 000 ?', '27 621 ?'], [
            #                  'Samsung\nЗащитное стекло на Samsung Galaxy A52 A51 самсунг А51 А52', '108747547', '4.6', '836 оценок', '245 ?', '154 ?'],
            #              [None, 4], [None, 5], ['Samsung\nАккумулятор Samsung IA-BH125C / BH-125C / BH125C', '113384144', 'Нет оценок', '',
            #                                     '1 913 ?', '946 ?'], ['Samsung\nЗащитное стекло на samsung а51/а52', '50722198', '5', '2 843 оценки', '331 ?', '139 ?'],
            #              ['Samsung\nСмартфон Samsung Galaxy A14 4/128GB', '178853188', '5', '55 оценок', '18 440 ?', '14 106 ?'], [
            #     'Samsung\nАдаптер тайпси, оригинал самсунг 45W', '97330930', '4', '213 оценок', '1 490 ?', '566 ?'], [None, 10],
            #     ['S20FE\nСмартфон Samsung Galaxy S20 FE Resale', '158616145', '4.3', '6 оценок', '33 000 ?', '29 700 ?'], [
            #         'Samsung\nСмартфон Galaxy A14 4/64GB', '189802451', '4.7', '55 оценок', '17 002 ?', '13 006 ?'],
            #     ['Samsung\nСмартфон Galaxy A14 4/64GB', '189802456', '4.7', '55 оценок', '16 594 ?', '12 694 ?'], [
            #         'Samsung\nЧехол на Samsung Galaxy S20 FE с принтом', '195996998', 'Нет оценок', '', '999 ?', '349 ?'],
            #     ['Samsung\nЧехол на Samsung Galaxy S20 FE с принтом', '195997003', 'Нет оценок', '', '999 ?', '349 ?'], [None, 16], [
            #         None, 17], ['Samsung\nЧехол на Samsung Galaxy S20 FE с принтом', '195996994', 'Нет оценок', '', '999 ?', '349 ?'],
            #     ['Samsung\nЧехол на Samsung Galaxy S20 с принтом', '196003433', 'Нет оценок', '', '999 ?', '339 ?']]

            self.workerThread = FileWritingThread(self.data, DEFAULT_PATH)
            self.workerThread.start()
            self.save_data_to_excel()
            self.output_statistic()
        else:
            QMessageBox.warning(self, 'Warning',
                                'Пожалуйста, заполните все поля')

    def save_data_to_excel(self) -> None:
        try:
            self.file_name, self.filter = QFileDialog.getSaveFileName(
                self, 'Сохранить файл', '', 'All Files (*); Excel Files (*.xlsx)')
            convert_to_excel(DEFAULT_PATH, self.file_name)
            QMessageBox.information(
                self, 'Information', 'Данные успешно сохранены')
        except OSError as err:
            self.file_name = os.path.join(DEFAULT_PATH, 'result.xlsx')
            convert_to_excel(DEFAULT_PATH, self.file_name)
            QMessageBox.warning(
                self, 'Warning', 'Директория не выбрана. \
                Данные сохранены в директорию по умолчанию')

    def output_graphs_question(self) -> bool:
        reply = QMessageBox.question(self, 'Confirmation',
                                     'Вывести график со статистикой?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        return reply == QMessageBox.Yes

    def output_statistic(self) -> None:
        if self.output_graphs_question():
            draw_graphs()
                    

class FileWritingThread(QThread):
    finished = pyqtSignal()

    def __init__(self, data: list, path: str) -> None:
        super().__init__()
        self.data = data
        self.path = path

    def run(self) -> None:
        serialize_data(self.data, self.path)
        self.finished.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GraphicalInterface()
    w.show()
    sys.exit(app.exec_())
