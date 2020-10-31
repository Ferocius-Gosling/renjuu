import pygame

pygame.init()


class Button:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color
        self.is_pressed = False
        self.X = None
        self.Y = None

    def draw(self, display, x, y, action=None):
        self.X = int(x)
        self.Y = int(y)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        pygame.draw.rect(display, self.color, (x, y, self.width, self.height))
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            if click[0] == 1:
                self.is_pressed = True
                if action is not None:
                    action()
        #print_text(message)
