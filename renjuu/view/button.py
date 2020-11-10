import pygame
from renjuu.view import params as p


class Button:
    def __init__(self, width, height, color, info=None):
        self.width = width
        self.height = height
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

    def hide(self, display, x, y):
        pygame.draw.rect(display, p.menu_color,
                         (x, y, self.width, self.height))


class SwitchButton:
    def __init__(self, width, height, colors: list, info: list, items: list):
        self.width = width
        self.height = height
        self.X = None
        self.Y = None
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


def hide(button, display, x, y):
    pygame.draw.rect(display, p.menu_color,
                     (x, y, button.width, button.height))
