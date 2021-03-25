import pygame
from abc import ABC, abstractmethod


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 102, 204)
RED = (255, 0, 0)
GRAY = (128, 128, 128)


def set_background(display, background_image=None, background_color=None):
    """Устанавливает фоновую картинку при наличии, иначе - просто окрашивает в заданный цвет"""

    if background_image:
        menu_background = pygame.image.load(background_image)
        display.blit(menu_background, (0, 0))
    else:
        display.fill(background_color)


class GameObject(ABC):
    """Базовый класс для объектов, которые будут отображаться на экране"""

    __slots__ = ["display", "x", "y"]

    @abstractmethod
    def __init__(self, display, x, y):
        self.display = display
        self.x = x
        self.y = y

    @abstractmethod
    def update(self):
        """Обновляет значения атрибутов объекта"""

    @abstractmethod
    def draw(self):
        """Отображает данный объект на экране"""


class Text(GameObject):
    """Для отображения текста на экране"""

    __slots__ = ["message", "color", "size", "type", "smoothing"]

    def __init__(self, display, x, y, message, **kwargs):
        super().__init__(display, x, y)

        self.message = message

        self.color = kwargs.get("color", BLACK)
        self.size = kwargs.get("size", 30)
        self.type = pygame.font.Font(kwargs.get("type", None), self.size)
        self.smoothing = kwargs.get("smoothing", True)

    def update(self):
        super().update()

    def draw(self):
        self.display.blit(self.type.render(self.message, self.smoothing, self.color), (self.x, self.y))


class NumberCell(GameObject):
    """Для ввода цифр с клавиатуры"""

    __slots__ = ["width", "height", "number", "title", "inactive_color", "active_color", "font_size", "game"]

    def __init__(self, display, x, y, width, height, title, game, **kwargs):
        super().__init__(display, x, y)

        self.width = width
        self.height = height
        self.game = game

        self.inactive_color = kwargs.get("inactive_color", RED)
        self.active_color = kwargs.get("active_color", GREEN)
        self.font_size = kwargs.get("font_size", 36)

        self.title = Text(display, x + 10, y + 10, title, **{"size": self.font_size}) if title else None
        self.number = Text(display, x + 10, y + 60, "", **{"size": self.font_size})

    def update(self):
        if self.game.inputting_symbol:
            if self.game.inputting_symbol - 48 in range(10):
                self.number.message = self.number.message + str(self.game.inputting_symbol - 48)
            elif self.game.inputting_symbol == pygame.K_BACKSPACE:
                self.number.message = self.number.message[:-1]

        self.game.inputting_symbol = None

    def draw(self):
        if self.title:
            self.title.draw()

        if self.number.message:
            pygame.draw.rect(self.display, self.active_color, (self.x, self.y + 50, self.width, self.height))
            self.number.draw()
        else:
            pygame.draw.rect(self.display, self.inactive_color, (self.x, self.y + 50, self.width, self.height))


class Rectangle(GameObject):
    """Прямоугольник"""

    __slots__ = ["width", "height", "color"]

    def __init__(self, display, x, y, width, height, color):
        super().__init__(display, x, y)

        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pygame.draw.rect(self.display, self.color, (self.x, self.y, self.width, self.height))

    def update(self):
        super().update()


class Circle(GameObject):
    """Круг"""

    __slots__ = ["radius", "color"]

    def __init__(self, display, x, y, radius, color):
        super().__init__(display, x, y)

        self.radius = radius
        self.color = color

    def draw(self):
        pygame.draw.circle(self.display, self.color, (self.x, self.y), self.radius)

    def update(self):
        super().update()


class Button(GameObject):
    """Кнопка"""

    __slots__ = ["width", "height", "action", "message", "font_size", "active_color", "inactive_color", "step"]

    def __init__(self, display, x, y, width, height, message, action=None, **kwargs):
        super().__init__(display, x, y)

        self.width = width
        self.height = height
        self.action = action
        self.message = message

        self.font_size = kwargs.get("font_size", 36)
        self.active_color = kwargs.get("active_color", RED)
        self.inactive_color = kwargs.get("inactive_color", GREEN)
        self.step = kwargs.get("step", 10)

    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            pygame.draw.rect(self.display, self.active_color, (self.x, self.y, self.width, self.height))

            if click[0]:
                if self.action:
                    self.action()
        else:
            pygame.draw.rect(self.display, self.inactive_color, (self.x, self.y, self.width, self.height))

        Text(self.display, self.x + self.step, self.y + 10, self.message, **{"font_size": self.font_size}).draw()

    def update(self):
        super().update()


class Menu(GameObject):
    """"Простое главное меню"""

    __slots__ = ["width", "height", "items", "background_color", "background_image", "interval"]

    def __init__(self, display, x, y, width, height, items, **kwargs):
        super().__init__(display, x, y)

        self.width = width
        self.height = height
        self.items = items

        self.background_image = kwargs.get("background_image", None)
        self.background_color = kwargs.get("background_color", BLUE)
        self.interval = kwargs.get("interval", 6)

    def draw(self):
        set_background(self.display, self.background_image, self.background_color)

        for i, button in enumerate(self.items):
            button.x = int((self.x + self.width - button.width) / 2)
            button.y = self.y + (self.interval + button.height) * i
            button.draw()

    def update(self):
        super().update()


class ListOfGameObjects:
    """Для группировки объектов"""

    __slots__ = ["game_objects"]

    def __init__(self, *game_objects):
        self.game_objects = list(game_objects)

    def draw(self):
        for game_object in self.game_objects:
            game_object.update()
            game_object.draw()

    def update(self):
        pass


class Plot(GameObject):
    """Выводит графики на экран"""

    __slots__ = ["center", "width", "height", "axes_color", "plot_color", "scale_x", "scale_y",
                 "thickness", "label_x", "label_y", "plots"]

    def __init__(self, display, x, y, width, height, *plots, **kwargs):
        super().__init__(display, x+20, y+20)

        self.width = width - 20
        self.height = height - 40
        self.center = self.x + 20, self.height

        self.axes_color = kwargs.get("axes_color", BLACK)
        self.plot_color = kwargs.get("plot_color", WHITE)
        self.thickness = kwargs.get("thickness", 3)
        self.label_x = kwargs.get("label_x", None)
        self.label_y = kwargs.get("label_y", None)

        self.plots = self.convert_coordinates_of_points(plots)

    def draw_axes(self):
        """Рисует оси координат"""

        pygame.draw.line(self.display, self.axes_color, (self.x, self.center[1]), (self.width, self.center[1]))
        pygame.draw.line(self.display, self.axes_color, (self.center[0], self.y), (self.center[0], self.height))

        Text(self.display, self.width-20, self.height + 15, self.label_x, **{"color": self.axes_color, "size":25}).draw()

        Text(self.display, self.x+15, self.y-20, self.label_y, **{"color": self.axes_color, "size":25}).draw()

        size_bar = 10
        axes_scale = 50

        for x in range(self.center[0], self.width, axes_scale):
            pygame.draw.line(self.display, self.axes_color, (x, self.center[1] - size_bar),
                             (x, self.center[1] + size_bar))

        for x in range(self.center[0], self.x, -axes_scale):
            pygame.draw.line(self.display, self.axes_color, (x, self.center[1] - size_bar),
                             (x, self.center[1] + size_bar))

        for y in range(self.center[1], self.height, axes_scale):
            pygame.draw.line(self.display, self.axes_color, (self.center[0] - size_bar, y),
                             (self.center[0] + size_bar, y))

        for y in range(self.center[1], self.y, -axes_scale):
            pygame.draw.line(self.display, self.axes_color, (self.center[0] - size_bar, y),
                             (self.center[0] + size_bar, y))

    def legend(self):
        pass

    def convert_coordinates_of_points(self, plots):
        """Пересчитывает реальные координаты в координаты на дисплее"""

        scale_x = 0
        scale_y = 0

        for plot in plots:
            temp1 = max(list(map(lambda t: t[0], plot)))
            temp2 = max(list(map(lambda t: t[1], plot)))

            if temp1 > scale_x:
                scale_x = temp1

            if temp2 > scale_y:
                scale_y = temp2

        scale_x /= (self.width-self.center[0])
        scale_y /= (self.height-self.y)

        return [[(int(self.center[0] + x / scale_x), int(self.center[1] - y / scale_y))
                 for x, y in plot]
                for plot in plots]

    def draw_points(self):
        """Рисует графики"""

        while len(self.plots) != len(self.plot_color):
            self.plot_color.append(self.plot_color[0])

        for plot, color in zip(self.plots, self.plot_color):
            pygame.draw.lines(self.display, color, False, plot, self.thickness)

    def draw(self):
        self.draw_axes()
        self.draw_points()

    def update(self):
        super().update()


class Game:
    """Создает новую 'игру'"""

    __slots__ = ["objects", "game_over", "game_pause", "display", "clock", "display_width", "display_height",
                 "inputting_symbol"]

    def __init__(self, capital, display_width, display_height):
        self.objects = []
        pygame.init()
        self.display = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption(capital)
        self.clock = pygame.time.Clock()
        self.display_width = display_width
        self.display_height = display_height

        self.inputting_symbol = None

        self.game_over = False
        self.game_pause = False

    def update(self):
        """Обновление объектов"""

        for o in self.objects:
            o.update()

    def draw(self):
        """Отображение объектов на экране"""

        if self.game_pause:
            self.display.fill(BLACK)

        if self.objects:
            self.objects[-1].draw()

    def handle_event(self):
        """Обработка нажатий на клавиши"""

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if len(self.objects) > 1:
                        self.objects.pop()

                if event.key == pygame.K_SPACE:
                    self.game_pause = True

                self.inputting_symbol = event.key

    def run(self):
        """Цикл работы игры"""

        while not self.game_over:
            self.handle_event()

            self.update()
            self.draw()

            pygame.display.update()
            pygame.time.delay(100)
