
class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        events = []
        self.hp -= amount

        if self.hp <= 0:
            events.append({ 'dead' : self.owner })

        return events

    def attack(self, target):
        events = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            events.append({ 'message' : '{0} attacks {1} for {2} hp.'.format(self.owner.name.capitalize(),
                                                                              target.name, str(damage))})
            events.extend(target.fighter.take_damage(damage))
        else:
            events.append({ 'message' : '{0} attacks {1} but does no damage'.format(self.owner.name.capitalize(),
                                                                                     target.name)})

        return events

