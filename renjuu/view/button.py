import pygame
import abc
from renjuu.view import params as p


class AbstractButton(abc.ABC):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.X = None
        self.Y = None

    def draw(self, *args, **kwargs):
        pass

    def hide(self, display, x, y):
        pygame.draw.rect(display, p.menu_color,
                         (x, y, self.width, self.height))


class Button(AbstractButton):
    def __init__(self, width, height, color, info=None):
        super().__init__(width, height)
        self.color = color
        self.info = info
        self.is_pressed = False
        self.X = None
        self.Y = None

    def draw(self, display, x, y, *args, action=None):
        self.X = x
        self.Y = y
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        text_style = pygame.font.Font(None, 26)
        text = text_style.render(self.info, 1, p.black_color)
        pygame.draw.rect(display, self.color, (x, y, self.width, self.height))
        display.blit(text, (x, y))
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            if click[0] == 1:
                self.is_pressed = True
                if action is not None:
                    action(*args)
            if click[0] == 0:
                self.is_pressed = False


class CounterWithLimits:
    def __init__(self, max_player_count: int = 0,
                 min_player_count: int = 0):
        self.max_count = max_player_count
        self.min_count = min_player_count

    def button_value_increment_with_limit(self, button):
        button.info = str(min(self.max_count, int(button.info) + 1))

    def button_value_decrement_with_limit(self, button):
        button.info = str(max(self.min_count, int(button.info) - 1))


class SwitchButton(AbstractButton):
    def __init__(self, width, height, colors: list, info: list, items: list):
        super().__init__(width, height)
        self.colors = colors
        self.info = info
        self.items = items
        self._items_order = iter(items)
        self._color_order = iter(colors)
        self._info_order = iter(info)
        self.current_info = info[0]
        self.current_color = colors[0]
        self.current_item = items[0]

    def switch(self):
        try:
            info_to_switch = next(self._info_order)
            color_to_switch = next(self._color_order)
            item_to_switch = next(self._items_order)
        except StopIteration:
            self._color_order = iter(self.colors)
            self._info_order = iter(self.info)
            self._items_order = iter(self.items)
            info_to_switch = next(self._info_order)
            color_to_switch = next(self._color_order)
            item_to_switch = next(self._items_order)
        self.current_color = color_to_switch
        self.current_info = info_to_switch
        self.current_item = item_to_switch

    def draw(self, display, x, y):
        self.X = x
        self.Y = y
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        text_style = pygame.font.Font(None, 26)
        text = text_style.render(self.current_info, 1, p.black_color)
        pygame.draw.rect(display, self.current_color,
                         (x, y, self.width, self.height))
        display.blit(text, (x, y))
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            if click[0] == 1:
                self.switch()
                pygame.time.wait(150)
