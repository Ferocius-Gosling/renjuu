class ClickHandler:
    def __init__(self):
        self.click_pos = (0, 0)
        self.click = (0, 0, 0)

    def check_click(self, click_pos, click):
        self.click_pos = click_pos
        self.click = click
        return bool(self.click[0])

    def handle(self):
        if self.click_pos[0] < 150 \
            or self.click_pos[1] < 55 \
            or self.click_pos[0] > 610 \
             or self.click_pos[1] > 510:
            return None
        x_click = (self.click_pos[0] - 150) // 32
        y_click = (self.click_pos[1] - 55) // 32
        x_remainder = (self.click_pos[0] - 150) % 32
        y_remainder = (self.click_pos[1] - 55) % 32
        x = x_click if x_remainder < 16 else x_click + 1
        y = y_click if y_remainder < 16 else y_click + 1
        return x, y