from enum import Enum
from random import randint

from loguru import logger


class Game:
    def __init__(self):
        self.random_num = self.generate_random_number(0, 100)

        self.stage = 1

    def generate_random_number(self, a: int, b: int) -> int:
        number = randint(a, b)
        logger.info(f'Сгенерировано случайное число - {number}')
        return number

    def game_stage(self) -> int:
        logger.debug(f'Запрос значения игровой попытки. Попытка №{self.stage}')
        return self.stage
