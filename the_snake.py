
from random import choice

import pygame as pg

# Константы размеров игрового поля и сетки.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Допустимые изменения направления.
DIRECTIONS = {
    (pg.K_UP, RIGHT): UP,
    (pg.K_UP, LEFT): UP,
    (pg.K_UP, UP): UP,

    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_DOWN, DOWN): DOWN,

    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_LEFT, LEFT): LEFT,

    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT,
    (pg.K_RIGHT, RIGHT): RIGHT,
}

# Цвета игровых объектов.
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки.
SPEED = 20

screen = pg.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32
)
pg.display.set_caption('Змейка')

clock = pg.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=None, body_color=None):
        if position is None:
            position = (
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2
            )

        self.position = position
        self.body_color = body_color

    def draw(self):
        """Подготовить метод отрисовки."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс яблока, которое появляется на игровом поле."""

    def __init__(self):
        """Создать яблоко и задать его цвет."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self, occupied_positions=None):
        """Разместить яблоко в свободной клетке."""
        if occupied_positions is None:
            occupied_positions = []

        free_positions = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x * GRID_SIZE, y * GRID_SIZE) not in occupied_positions
        ]

        if free_positions:
            self.position = choice(free_positions)
        else:
            self.position = None

    def draw(self):
        """Отрисовать яблоко на игровом поле."""
        rect = pg.Rect(
            self.position,
            (GRID_SIZE, GRID_SIZE)
        )

        pg.draw.rect(
            screen, self.body_color, rect
        )
        pg.draw.rect(
            screen, BORDER_COLOR, rect, 1
        )


class Snake(GameObject):
    """Класс змейки, управляющий движением и ростом."""

    def __init__(self):
        """Создать змейку в центре игрового поля."""
        super().__init__(body_color=SNAKE_COLOR)

        self.reset()
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def reset(self):
        """Сбросить состояние змейки после столкновения."""
        self.length = 1
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
        self.positions = [self.position]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновить направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Переместить змейку на одну клетку."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        new_head = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)
        self.position = new_head

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовать все сегменты змейки."""
        for position in self.positions[:-1]:
            rect = pg.Rect(
                position,
                (GRID_SIZE, GRID_SIZE)
            )

            pg.draw.rect(
                screen, self.body_color, rect
            )
            pg.draw.rect(
                screen, BORDER_COLOR, rect, 1
            )

        head_rect = pg.Rect(
            self.positions[0],
            (GRID_SIZE, GRID_SIZE)
        )

        pg.draw.rect(
            screen, self.body_color, head_rect
        )
        pg.draw.rect(
            screen, BORDER_COLOR, head_rect, 1
        )

        if self.last:
            last_rect = pg.Rect(
                self.last,
                (GRID_SIZE, GRID_SIZE)
            )

            pg.draw.rect(
                screen,
                BOARD_BACKGROUND_COLOR,
                last_rect
            )


def handle_keys(game_object):
    """Обработать нажатия клавиш управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

        if event.type == pg.KEYDOWN:
            game_object.next_direction = DIRECTIONS.get(
                (event.key, game_object.direction)
            )


def main():
    """Запустить основной игровой цикл."""
    pg.init()

    snake = Snake()
    apple = Apple()

    while apple.position in snake.positions:
        apple.randomize_position(snake.positions)

    while True:

        clock.tick(SPEED)

        handle_keys(snake)

        snake.update_direction()

        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

            while apple.position in snake.positions:
                apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
