from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel
from loguru import logger

from game import Game


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('random_number_game.ui', self)
        logger.debug('UI загружено')

        self.game = Game()

        self.check_result_button: QPushButton = self.findChild(QPushButton, 'CheckResultButton')

        self.set_default_stylesheets()

        self.restart_button: QPushButton = self.findChild(QPushButton, 'RestartButton')
        self.restart_button.close()

        self.add_buttons_events()

    def update_placeholder(self):
        self.input_field.setPlaceholderText(f'Ведите число 0-100. Попытка {self.game.game_stage()}')
        logger.debug('Placeholder обновлен')

    def add_buttons_events(self):
        self.check_result_button.clicked.connect(self.run_game)
        self.restart_button.clicked.connect(self.restart_game)
        logger.debug('События для кнопок определены и привязаны')

    def run_game(self):
        self.restart_button.close()

        if self.check_field():
            input_num = int(self.input_field.text())

            if self.game.game_stage() == 5 and input_num != self.game.random_num:
                self.text_label.setStyleSheet('color: red;')
                self.text_label.setText(f'Вы проиграли! Попытки кончились.\nЗагаданное число {self.game.random_num}')

                self.input_field.clear()
                self.input_field.setPlaceholderText('Начините заново!!!')
                self.input_field.setDisabled(True)

                self.restart_button.show()

                logger.debug('Игра проиграна')
                return

            if input_num == self.game.random_num and self.game.game_stage() <= 5:
                self.text_label.setStyleSheet('color: green;')
                self.text_label.setText('Вы выиграли! Поздравляю')

                self.input_field.setDisabled(True)

                self.restart_button.show()

                logger.debug('Игра выиграна')
                return

            else:
                if input_num < self.game.random_num and self.game.game_stage() <= 5:
                    self.show_text('Неверно. Вы названи число меньше загаданного')
                elif input_num > self.game.random_num and self.game.game_stage() <= 5:
                    self.show_text('Неверно. Вы названи число больше загаданного')
                self.game.stage += 1
                self.update_placeholder()
                self.input_field.clear()

    def restart_game(self):
        self.game.random_num = self.game.generate_random_number(0, 100)
        self.game.stage = 1

        self.restart_button.close()

        self.set_default_stylesheets()

    def set_default_stylesheets(self):
        self.input_field: QLineEdit = self.findChild(QLineEdit, 'InputNumber')
        self.input_field.setDisabled(False)
        self.input_field.clear()
        self.update_placeholder()

        self.text_label: QLabel = self.findChild(QLabel, 'OutputText')
        self.text_label.setStyleSheet('background-color: rgb(119, 118, 123);\ncolor: rgb(246, 245, 244);\nborder-radius: 25px;')
        self.text_label.setText('Компьютер загадал число от 0 до 100, угадай его! У тебя 5\nпопыток')

    def check_field(self) -> bool:
        txt = self.input_field.text().strip()

        logger.debug(f'Получено значение для валидации "{txt}"')

        if txt == '':
            self.show_error('Поле не может быть пустым')
            return False

        elif not txt.isdigit():
            self.show_error('Введите число, букв быть не должно')
            return False

        elif not 0 <= int(txt) <= 100:
            self.show_error('Значение должно быть в интервале [0, 100]')
            return False

        return True

    def show_error(self, error_msg: str):
        self.text_label.setStyleSheet('color: red;')
        self.text_label.setText(error_msg)

        logger.error(f'Сообщение об ошибке "{error_msg}"')

    def show_text(self, msg: str):
        self.text_label.setStyleSheet(
            'background-color: rgb(119, 118, 123);\ncolor: rgb(246, 245, 244);\nborder-radius: 25px;')
        self.text_label.setText(msg)

        logger.debug(f'Сообщение "{msg}"')
