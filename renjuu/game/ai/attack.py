import dataclasses
from renjuu.game.ai.const import ATTACK_WEIGHTS


@dataclasses.dataclass()
class Attack:
    capability: int = dataclasses.field(default=0)
    potential: int = dataclasses.field(default=0)
    divider: int = dataclasses.field(default=1)

    def count_weight(self):
        return ATTACK_WEIGHTS[self.capability][self.potential] / self.divider
