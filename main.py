import logging
import multiprocessing as mp
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QLabel, QComboBox, QDialog,
                             QMainWindow, QPushButton, QFileDialog,
                             QWidget, QLineEdit, QMessageBox, QVBoxLayout)
from check import check_key
from save import serialize_data, convert_to_excel
from statistic import draw_graphs
from WBparser import extract_data

SORT_METHODS = {0: 'popular', 1: 'rate', 2: 'priceup',
                3: 'pricedown', 4: 'newly', 5: 'benefit'}
DEFAULT_PATH = 'Files\\result.json'

formatter = '[%(asctime)s: %(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, filename="main.log",
                    filemode="w", format=formatter)


class KeyInputDialog(QDialog):
    def __init__(self, parent=None):
        super(KeyInputDialog, self).__init__(parent)

        self.setWindowTitle('Введите ключ')
        self.key_label = QLabel('Ключ:', self)
        self.key_input = QLineEdit(self)
        self.confirm_button = QPushButton('Подтвердить', self)
        self.confirm_button.clicked.connect(self.check_key)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.key_label)
        self.layout.addWidget(self.key_input)
        self.layout.addWidget(self.confirm_button)
        self.setLayout(self.layout)

    def check_key(self):
        self.entered_key = self.key_input.text().strip()
        if check_key(self.entered_key):
            self.accept()
        else:
            self.reject()

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

        self.show_key_input_dialog()

    def show_key_input_dialog(self):
        self.key_input_dialog = KeyInputDialog(self)
        self.result = self.key_input_dialog.exec_()
        if self.result != QDialog.Accepted:
            self.close()

    def is_fill(self, name: str, quantity: str) -> bool:
        return True if name and quantity else False

    def start_program(self) -> None:
        logging.info('Start programm (main.py)')
        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()
        sort = self.sort_input.currentIndex()
        if self.is_fill(name, quantity):
            logging.info('Is fill')
            self.data = extract_data(name,  sort, int(quantity))
            serialize_data(self.data, DEFAULT_PATH)
            self.save_data_to_excel()
            self.output_statistic()
            logging.info('End programm (main.py)')
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


if __name__ == "__main__":
    mp.freeze_support()
    app = QApplication(sys.argv)
    w = GraphicalInterface()
    w.show()
    sys.exit(app.exec_())
