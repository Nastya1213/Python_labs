import random

class Hero:
    def __init__(self, name, level=1, health=100, power=10):
        self.name = name
        self.level = level
        self.health = health
        self.power = power

    
    def go_on_scouting(self):
        # Случайная встреча с противником
        enemy_level = random.randint(1, 5)
        print(f"{self.name} встретил противника уровня {enemy_level} во время разведки.")
        
        # Выбор действия: сражаться или избегать боя
        choice = input("Вы хотите сразиться или убежать? (fight/run): ").lower()
        if choice == "fight":
            return enemy_level
        else:
            print(f"{self.name} избегает боя и возвращается в королевство.")
            return None

class Warrior(Hero):
    def __init__(self, name, level=1, health=120, power=15):
        super().__init__(name, level, health, power)

    def attack(self, enemy_level):
        if self.level >= enemy_level:
            print(f"Воин {self.name} побеждает врага уровня {enemy_level}.")
            return "victory"
        else:
            print(f"Воин {self.name} проиграл врагу уровня {enemy_level}.")
            return "defeat"

class Mage(Hero):
    def __init__(self, name, level=1, health=80, power=10, mana=50):
        super().__init__(name, level, health, power)
        self.mana = mana

    def cast_spell(self, enemy_level):
        if self.mana >= 10 and self.level >= enemy_level:
            self.mana -= 10
            print(f"Маг {self.name} использует заклинание и побеждает врага уровня {enemy_level}.")
            return "victory"
        else:
            print(f"Маг {self.name} проиграл врагу уровня {enemy_level}.")
            return "defeat"

class Kingdom:
    def __init__(self):
        self.food = 9
        self.live = True
        self.territory = 50
        self.heroes = []

    def add_hero(self, hero):
        self.heroes.append(hero)
        print(f"Герой {hero.name} добавлен в королевство.")

    def feed_people(self):
        # Расход еды для населения
        if self.food > 10:
            self.food -= 10
            print(f"Королевство накормило народ. Осталось {self.food} еды.")
        else:
            print("В королевстве нет еды! Население начинает бунтовать.")
            self.trigger_rebellion()

    def manage_resources(self, success):
        if success == 'victory':
            self.territory += 5
            print(f"Королевство расширилось! Новая территория: {self.territory}.")
        elif success == 'defeat':
            if self.territory >= 5:
                self.territory -= 5
                print(f"Королевство потеряло часть территории. Осталось: {self.territory}.")
            else: self.live = False
            
        else:
            print("Нет изменений в ресурсах королевства.")

    def trigger_rebellion(self):
        print("Бунт! Королевство в опасности из-за нехватки ресурсов.")
        self.live = False



# Создаем королевство и героев
kingdom = Kingdom()
warrior = Warrior("Артур")
mage = Mage("Мерлин")

# Добавляем героев в королевство
kingdom.add_hero(warrior)
kingdom.add_hero(mage)

while kingdom.live:
    # Цикл разведки и управления ресурсами
    for hero in kingdom.heroes:
        enemy_level = hero.go_on_scouting()
        if enemy_level:
            if isinstance(hero, Warrior):
                result = hero.attack(enemy_level)
            elif isinstance(hero, Mage):
                result = hero.cast_spell(enemy_level)
            kingdom.manage_resources(result)
    # Королевство кормит народ
    kingdom.feed_people()
print("Королевство умерло :(")
