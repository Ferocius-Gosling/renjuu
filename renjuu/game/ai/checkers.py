from renjuu.game.ai.attack import Attack
from renjuu.game.const import Color, directions
from renjuu.game.params import PLAYER_COUNT


class LineChecker:
    def __init__(self):
        self.sub_color = Color.black
        self.attacks = []
        self.current_attack = Attack()
        self.iteration = 1
        self.check_edge = False
        self.attack_place = 1

    def get_attacks(self, game, vector, color, direction):
        self.change_color(color)
        temp = vector
        for i in range(game.board.length_to_win):
            vector += direction
            if self.check_point(game, vector):
                break
        self.turn_to_begin()
        for i in range(game.board.length_to_win):
            temp -= direction
            if self.check_point(game, temp):
                break
        return self.attacks

    def check_point(self, game, vec):
        color = game.board[vec] if not game.board.get_condition(vec) else None
        if self.iteration == 4 and self.sub_color == color:
            self.check_edge = True
        elif self.iteration == 5:
            if self.check_edge:
                if color == self.sub_color or color == Color.non:
                    self.current_attack.potential += 1
                self.attacks.append(self.current_attack)
            return 0
        self.iteration += 1
        if color != Color.non and color is not None:
            if color != self.sub_color:
                self.attacks.append(self.current_attack)
                return color
            else:
                self.current_attack.capability += 1
                self.attack_place += 1
        elif color is None:
            self.attacks.append(self.current_attack)
            return True
        else:
            if self.current_attack.capability:
                self.current_attack.potential += 1
                self.attacks.append(self.current_attack)
                self.current_attack = Attack()
                self.current_attack.potential += 1
            self.current_attack.divider += 1
            self.attack_place += 1

    def turn_to_begin(self):
        self.iteration = 1
        self.check_edge = False
        self.current_attack = self.attacks[0]
        self.attacks.pop(0)

    def change_color(self, color):
        self.sub_color = color
        self.current_attack.capability += 1


def get_all_attacks(game, vector):
    if game.board[vector] != Color.non:
        return False
    attacks = {}
    for i in range(PLAYER_COUNT):
        attacks[Color(i + 1)] = {}
        for direction in directions:
            attacks[Color(i + 1)][direction] = \
                get_attack_lines(game, vector, Color(i + 1), direction)
    return attacks


def get_attack_lines(game, vector, sub_color, direction):
    checker = LineChecker()
    checker.get_attacks(game, vector, sub_color, direction)
    return filter_lines(checker)


def filter_lines(checker: LineChecker):
    result = []
    if checker.attack_place >= 5:
        for attack in checker.attacks:
            if attack.capability and attack.potential or attack.capability >= 5:
                result.append(attack)
    checker.attacks = result
    return result


def is_break_point(line: list):
    if not line or not len(line):
        return False
    center_attack = Attack()
    for attack in line:
        if attack.divider == 1:
            center_attack = attack
    if center_attack.capability >= 4:
        return True
    if center_attack.potential == 2 and center_attack.capability >= 3:
        return True
    result = False
    for attack in line:
        score = center_attack.capability
        if attack.divider == 2:
            if center_attack.potential == 2 and attack.potential == 2:
                score += 1
            if score + attack.capability >= 4:
                result = True
    return result


def count_weight(game, vector):
    attacks = get_all_attacks(game, vector)
    if not attacks:
        return
    amount = 0
    for i in range(PLAYER_COUNT):
        amount += count(game, attacks[Color(i + 1)], Color(i + 1))
    return amount


def count(game, attacks, color):
    weight = 0
    breakpoints = 0
    for key in attacks:
        if is_break_point(attacks[key]):
            if breakpoints + 1 == 2:
                breakpoints += 1
                weight += 100
                break
        for attack in attacks[key]:
            if attack.capability > 5:
                attack.capability = 5
            if attack.capability == 5 and color == game.current_player.color:
                weight += 100
            weight += attack.count_weight()
    return weight
