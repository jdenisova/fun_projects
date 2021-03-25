import GameGUI
import random
from abc import ABC, abstractmethod


class Warrior(ABC):
    """Базовый класс для модели солдата"""

    __slots__ = ["display", "x", "y", "color", "size"]

    def __init__(self, display, x, y, color, size):
        self.display = display
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass


class Soldier(Warrior):

    def __init__(self, display, x, y, color, size):
        super().__init__(display, x, y, color, size)

    def update(self):
        pass

    def draw(self):
        GameGUI.Rectangle(self.display, self.x, self.y, self.size, self.size, self.color).draw()


class Partisan(Warrior):

    def __init__(self, display, x, y, color, size):
        super().__init__(display, x, y, color, int(size * 0.5))

    def update(self):
        pass

    def draw(self):
        GameGUI.Circle(self.display, self.x, self.y, self.size, self.color).draw()


class Army:
    """Класс для модели армии"""

    __slots__ = ["display", "name", "position", "soldiery", "color"]

    def __init__(self, display, position, name, soldiery, color):
        self.display = display

        self.name = name
        self.color = color
        self.position = position
        self.soldiery = soldiery

    def update(self):
        x1, x2, y1, y2 = self.position
        for soldier in self.soldiery:
            soldier.x = random.randint(x1, x2)
            soldier.y = random.randint(y1, y2)

    def draw(self):
        if self.number > 100:
            for soldier in self.soldiery[:100]:
                soldier.draw()
        else:
            for soldier in self.soldiery:
                soldier.draw()

    @property
    def number(self):
        return len(self.soldiery)

    @number.setter
    def number(self, value):
        value = value if value > 0 else 0
        self.soldiery = self.soldiery[:value]


class SimpleIterator:
    __slots__ = ["limit", "counter"]

    def __init__(self, limit):
        self.limit = limit
        self.counter = -1

    def __next__(self):
        if self.counter + 1 < self.limit:
            self.counter += 1
            return self.counter
        else:
            raise StopIteration


class FightActionModel(GameGUI.GameObject):
    """Модель боевых действий"""

    __slots__ = ["N1", "N2", "t", "background_color", "iter", "army1", "army2", "information",
                 "parameters", "isPlot", "button"]

    def __init__(self, display, x, y, background_color, parameters, army1, army2, N1, N2, t):
        super().__init__(display, x, y)

        self.N1 = N1
        self.N2 = N2
        self.t = t
        self.background_color = background_color
        self.iter = SimpleIterator(len(self.N1))

        self.army1 = army1
        self.army2 = army2

        self.isPlot = False

        font_size = 35
        step_x = 200
        step_y = 30
        x = self.x + 50
        y = self.y + 10

        label_army1 = GameGUI.Rectangle(self.display, x - 30, y, 20, 20, army1.color)
        label_army2 = GameGUI.Rectangle(self.display, x - 30 + step_x * 2, y, 20, 20, army2.color) \
            if isinstance(army2.soldiery[0], Soldier) \
            else GameGUI.Circle(self.display, x - 30 + step_x * 2, y + 10, 10, army2.color)

        self.information = [
            GameGUI.Text(self.display, x, y, army1.name, **{"font_size": font_size}),
            GameGUI.Text(self.display, x, y + step_y, "N1(t)", **{"font_size": font_size}),
            GameGUI.Text(self.display, x, y + step_y * 2, "alpha1", **{"font_size": font_size}),
            GameGUI.Text(self.display, x, y + step_y * 3, "beta1", **{"font_size": font_size}),
            GameGUI.Text(self.display, x, y + step_y * 4, "gamma1", **{"font_size": font_size}),

            label_army1,

            GameGUI.Text(self.display, x + step_x * 2, y, army2.name, **{"font_size": font_size}),
            GameGUI.Text(self.display, x + step_x * 2, y + step_y, "N1(t)", **{"font_size": font_size}),
            GameGUI.Text(self.display, x + step_x * 2, y + step_y * 2, "alpha1", **{"font_size": font_size}),
            GameGUI.Text(self.display, x + step_x * 2, y + step_y * 3, "beta1", **{"font_size": font_size}),
            GameGUI.Text(self.display, x + step_x * 2, y + step_y * 4, "gamma1", **{"font_size": font_size}),

            label_army2
        ]

        self.parameters = [
            GameGUI.Text(self.display, x + step_x, y + step_y, str(parameters[0]), **{"font_size": font_size}),
            GameGUI.Text(self.display, x + step_x, y + step_y * 2, str(parameters[1]), **{"font_size": font_size}),
            GameGUI.Text(self.display, x + step_x, y + step_y * 3, str(parameters[2]), **{"font_size": font_size}),
            GameGUI.Text(self.display, x + step_x, y + step_y * 4, str(parameters[3]), **{"font_size": font_size}),

            GameGUI.Text(self.display, x + step_x * 3, y + step_y, str(parameters[4]), **{"font_size": font_size}),
            GameGUI.Text(self.display, x + step_x * 3, y + step_y * 2, str(parameters[5]), **{"font_size": font_size}),
            GameGUI.Text(self.display, x + step_x * 3, y + step_y * 3, str(parameters[6]), **{"font_size": font_size}),
            GameGUI.Text(self.display, x + step_x * 3, y + step_y * 4, str(parameters[7]), **{"font_size": font_size})
        ]

        self.button = GameGUI.Button(game.display, x + int(step_x * 3.5), y + step_y * 2, 200, 40,
                                     "Показать графики", self.click_button,
                                     **{"font_size": 36, "active_color": GameGUI.RED, "inactive_color": GameGUI.GREEN})

    def click_button(self):
        self.isPlot = True if not self.isPlot else False

        pygame.time.delay(200)

    def update(self):
        self.army1.update()
        self.army2.update()

    def draw(self):
        GameGUI.set_background(self.display, None, self.background_color)

        for text in self.information:
            text.draw()
        for text in self.parameters:
            text.draw()

        self.button.draw()

        if self.isPlot:
            GameGUI.Plot(self.display, 0, 200, int(game.display_width / 2), game.display_height,
                         list(zip(self.N1, self.N2)),
                         **{"plot_color": [GameGUI.GREEN], "label_x": "N1", "label_y": "N2"})\
                .draw()

            GameGUI.Plot(self.display, int(game.display_width / 2), 200, game.display_width, game.display_height,
                         list(zip(self.t, self.N1)), list(zip(self.t, self.N2)),
                         **{"plot_color": [self.army1.color, self.army2.color], "label_x": "t", "label_y": "N"})\
                .draw()
        else:
            try:
                number = next(self.iter)
                x, y = self.N1[number], self.N2[number]

                while self.parameters[0].message == str(round(x)) and self.parameters[4].message == str(round(y)):
                    number = next(self.iter)
                    x, y = self.N1[number], self.N2[number]

                self.army1.number = round(x)
                self.army2.number = round(y)

                self.parameters[0].message = str(round(x))
                self.parameters[4].message = str(round(y))

                self.army1.draw()
                self.army2.draw()

            except StopIteration:
                self.isPlot = True


class ModelType(GameGUI.GameObject):
    """Выбор типа модели"""

    __slots__ = ["background_color", "parameters", "button1", "button2"]

    def __init__(self, display, x, y, background_color, *args):
        super().__init__(display, x, y)

        self.background_color = background_color
        self.parameters = args

        self.button1 = GameGUI.Button(game.display, x + 300, y + 200, 370, 40, "Регулярные армии", self.click_button1,
                                      **{"font_size": 36, "active_color": GameGUI.RED,
                                         "inactive_color": GameGUI.GREEN, "step": 100})
        self.button2 = GameGUI.Button(game.display, x + 300, y + 250, 370, 40, "Регулярные и партизанские части",
                                      self.click_button2, **{"font_size": 36, "active_color": GameGUI.RED,
                                                             "inactive_color": GameGUI.GREEN})

    def click_button1(self):
        x, y, t = self.solveODE_1(*self.parameters)
        size = 20
        soldiery1 = [
            Soldier(self.display, random.randint(0, DISPLAY_WIDTH - size), random.randint(200, DISPLAY_HEIGHT - size),
                    GameGUI.BLUE, size) for i in range(self.parameters[0])]
        soldiery2 = [
            Soldier(self.display, random.randint(0, DISPLAY_WIDTH) - size, random.randint(200, DISPLAY_HEIGHT - size),
                    GameGUI.RED, size) for i in range(self.parameters[4])]

        army1 = Army(self.display, (0, DISPLAY_WIDTH - size, 200, DISPLAY_HEIGHT - size),
                     "Регулярная армия", soldiery1, GameGUI.BLUE)
        army2 = Army(self.display, (0, DISPLAY_WIDTH - size, 200, DISPLAY_HEIGHT - size),
                     "Регулярная армия", soldiery2, GameGUI.RED)

        game.objects.pop()

        game.objects.append(
            FightActionModel(self.display, 0, 0, GameGUI.GRAY, self.parameters, army1, army2, x, y, t))

    def click_button2(self):
        x, y, t = self.solveODE_2(*self.parameters)
        size = 20
        soldiery1 = [
            Soldier(self.display, random.randint(0, DISPLAY_WIDTH - size), random.randint(200, DISPLAY_HEIGHT - size),
                    GameGUI.BLUE, size) for i in range(self.parameters[0])]
        soldiery2 = [
            Partisan(self.display, random.randint(0, DISPLAY_WIDTH - size), random.randint(200, DISPLAY_HEIGHT - size),
                     GameGUI.RED, size) for i in range(self.parameters[4])]

        army1 = Army(self.display, (0, DISPLAY_WIDTH - size, 200, DISPLAY_HEIGHT - size),
                     "Регулярная армия", soldiery1, GameGUI.BLUE)
        army2 = Army(self.display, (0, DISPLAY_WIDTH - size, 200, DISPLAY_HEIGHT - size),
                     "Партизанские формирования", soldiery2, GameGUI.RED)

        game.objects.pop()
        game.objects.append(
            FightActionModel(self.display, 0, 0, GameGUI.GRAY, self.parameters, army1, army2, x, y, t))

    def solveODE_1(self, x0, alpha1, beta1, gamma1, y0, alpha2, beta2, gamma2, tau=1e-5):
        """Вычисляет ход боевых действий между регулярными армиями"""

        t, x, y = [0], [x0], [y0]

        while True:
            t.append(t[-1] + tau)

            x.append(x[-1] + (-alpha1 * x[-1] - beta1 * y[-1] + gamma1) * tau)
            y.append(y[-1] + (-alpha2 * y[-1] - beta2 * x[-1] + gamma2) * tau)

            if x[-1] < 1 or y[-1] < 1:
                if x[-1] < 1:
                    x[-1] = 0
                if y[-1] < 1:
                    y[-1] = 0
                return x, y, t

    def solveODE_2(self, x0, alpha1, beta1, gamma1, y0, alpha2, beta2, gamma2, tau=1e-5):
        """Вычисляет ход боевых действий между регулярной армией и партизанским соединением"""

        t, x, y = [0], [x0], [y0]

        while True:
            t.append(t[-1] + tau)

            x.append(x[-1] + (-alpha1 * x[-1] - beta1 * y[-1] + gamma1) * tau)
            y.append(y[-1] + (-alpha2 * y[-1] - beta2 * x[-1] * y[-1] + gamma2) * tau)

            if x[-1] < 1 or y[-1] < 1:
                if x[-1] < 1:
                    x[-1] = 0
                if y[-1] < 1:
                    y[-1] = 0
                return x, y, t

    def update(self):
        super().update()

    def draw(self):
        GameGUI.set_background(self.display, None, self.background_color)

        self.button1.draw()
        self.button2.draw()


class InputtingParameters(GameGUI.GameObject):
    __slots__ = ["background_color", "iter", "input_cell_titles", "input_cell", "button", "parameters"]

    def __init__(self, display, x, y, background_color, *args):
        super().__init__(display, x, y)

        self.background_color = background_color
        self.iter = SimpleIterator(len(args) - 1)
        self.input_cell_titles = args[1:]
        self.input_cell = GameGUI.NumberCell(game.display, x, y, 110, 40, args[0], game,
                                             **{"active_color": GameGUI.GREEN, "inactive_color": GameGUI.RED,
                                                "font_size": 30})

        self.button = GameGUI.Button(game.display, x-40, y + 105, 185, 45, "Ввести параметр", self.input_parameters,
                                     **{"font_size": 36, "active_color": GameGUI.RED,
                                        "inactive_color": GameGUI.GREEN})
        self.parameters = []

    def input_parameters(self):
        if self.input_cell.number.message:
            self.parameters.append(int(self.input_cell.number.message))
            self.input_cell.number.message = ""

            try:
                self.input_cell.title.message = self.input_cell_titles[next(self.iter)]

            except StopIteration:
                game.objects.pop()

                game.objects.append(ModelType(game.display, 0, 0, GameGUI.BLUE, *self.parameters))

                pygame.time.delay(1000)

    def update(self):
        self.input_cell.update()

    def draw(self):
        GameGUI.set_background(self.display, None, self.background_color)

        self.input_cell.draw()
        self.button.draw()


def new_model():
    game.objects.append(InputtingParameters(
        game.display, int((game.display_width - 110) / 2),
        int(game.display_height / 2) - 120, GameGUI.BLUE,
        *["N1(0)", "alpha1", "beta1", "gamma1", "N2(0)", "alpha2", "beta2", "gamma2"])
    )


if __name__ == "__main__":
    DISPLAY_WIDTH = 1000
    DISPLAY_HEIGHT = 600

    game = GameGUI.Game("Боевые действия двух армий", DISPLAY_WIDTH, DISPLAY_HEIGHT)

    menu = GameGUI.Menu(game.display, 0, 200, DISPLAY_WIDTH, DISPLAY_HEIGHT,
                        (
                            GameGUI.Button(game.display, 0, 0, 210, 40, "Ввести параметры", new_model,
                                           **{"font_size": 36, "active_color": GameGUI.RED,
                                              "inactive_color": GameGUI.GREEN}),
                            GameGUI.Button(game.display, 0, 0, 210, 40, "Выйти", quit,
                                           **{"font_size": 36, "active_color": GameGUI.RED,
                                              "inactive_color": GameGUI.GREEN, "step": 70})
                        ),
                        **{"interval": 10, "background_color": GameGUI.BLUE})

    game.objects.append(menu)
    game.run()
