import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QLabel, QComboBox,
                             QMainWindow, QPushButton,
                             QWidget, QLineEdit)


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
        self.sort_input.addItems(['По популярности', 'По рейтингу', 'По возрастанию цены',
                                 'По убыванию цены', 'По новинкам', 'Сначала выгодные'])

        self.start_parser = QPushButton('НАЧАТЬ', self.central_widget)
        self.start_parser.setToolTip('Начинает загрузку товаров с сайта')
        self.start_parser.setGeometry(175, 350, 100, 30)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GraphicalInterface()
    w.show()
    sys.exit(app.exec_())
