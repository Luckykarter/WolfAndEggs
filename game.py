import time
from enum import Enum
import random
from functools import partial
from threading import Thread


class Location(Enum):
    left_up = 'Слева сверху'
    left_down = 'Слева снизу'
    right_up = 'Справа сверху'
    right_down = 'Справа снизу'


class Wolf:
    def __init__(self):
        self.location = Location.left_up

    def move(self, new_location: Location):
        self.location = new_location
        print(f'Wold moved to: {new_location}')


class Egg:
    def __init__(self, location: Location):
        self.location = location
        self.position = 0

    def move(self):
        self.position += 1


class Game:
    EGG_PATH_LENGTH = 5

    def __init__(self):
        self.sound = False
        self.score = 0
        self.speed = 1.0
        self.is_active = False
        self.health = 3
        self.wolf = Wolf()
        self.eggs = [Egg(x) for x in Location]

    def toggle_sound(self):
        self.sound = not self.sound
        if self.sound:
            print('Звук включен')
        else:
            print("Звук выключен")

    def check_next_level(self):
        if self.score % 10 == 0:
            self.speed += 0.2

    def game_over(self):
        self.is_active = False
        print(f'Game Over. Your score: {self.score}')

    def end_game(self):
        self.health -= 1
        if self.health == 0:
            self.game_over()

    def check_wolf_position(self, current_egg: Egg):
        if current_egg.location != self.wolf.location:
            self.end_game()
        else:
            self.score += 1

    def move_random_egg(self):
        egg = random.choice(self.eggs)
        egg.move()
        print(f'Яйцо {egg.location} в позиции {egg.position}')
        print(f'Количество очков: {self.score}')
        if egg.position > self.EGG_PATH_LENGTH:
            self.check_wolf_position(egg)
            egg.position = 0

    def play(self):
        self.is_active = True
        while self.is_active:
            print(f'Волк находится: {self.wolf.location}')
            self.move_random_egg()
            time.sleep(3 / self.speed)
            self.check_next_level()


class Button:
    def __init__(self, name: str, action: callable):
        self.name = name
        self.action = action

    def press(self):
        self.action()


class GameController:
    def __init__(self):
        self.game = Game()
        self.buttons = [
            Button('И', partial(self.game.wolf.move, Location.left_up)),
            Button('Ы', partial(self.game.wolf.move, Location.left_down)),
            Button('З', partial(self.game.wolf.move, Location.right_up)),
            Button('Д', partial(self.game.wolf.move, Location.right_down)),

            Button('Игра', self.game.play),
            Button('Звук', self.game.toggle_sound)
        ]


def move_wolf_randomly(gc: GameController):
    while True:
        button = random.choice(gc.buttons[0:3])
        button.press()
        time.sleep(1)


if __name__ == 'main':
    gc = GameController()
    t = Thread(target=move_wolf_randomly, args=(gc,))
    t.start()
    gc.buttons[4].press()