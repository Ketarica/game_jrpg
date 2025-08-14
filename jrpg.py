def hp_bar(current, maximum, length=20, symbol="█"):
    filled = int(length * current / maximum)
    empty = length - filled
    return f"[{symbol * filled}{' ' * empty}] {current}/{maximum}"

class Character:
    def __init__(self, health, mana, name):
        self.max_health = health
        self.max_mana = mana
        self.health = health
        self.mana = mana
        self.name = name

    def damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        print(f"{self.name} получает {damage} урона, у него осталось {self.health} здоровья.")

    def display(self):
        # print(f"{self.name} имеет ещё {self.health} здоровья")
        # print(f"{self.name} имеет ещё {self.mana} маны")
        print(f"  Здоровье: {hp_bar(self.health, self.max_health)}")
        print(f"  Мана:     {hp_bar(self.mana, self.max_mana)}")

    def spellsList(self):
        spell_select = input("Выберите 1 заклинание: fire, water:\n").strip().lower()
        # spell_check = True
        if spell_select == "fire":
            spell_dmg = 10
            return spell_dmg, spell_select
        elif spell_select == "water":
            spell_dmg = 5
            return spell_dmg, spell_select
        else:
            print("Такого заклинания нет в списке")
            return None, None

    def attack(self, target, damage):
        print(f"{self.name} атакует {target.name}")
        target.damage(damage)







class Enemy(Character):
    def attack(self, target, damage):
        print(f"{self.name} атакует {target.name}")
        target.damage(damage)


class CharMaker:
    def __init__(self, role):
        self.role = role

    def create(self):
        print(f"Создание {self.role}:")
        name = input("Введите имя: ")
        while True:
            try:
                health = int(input("Введите здоровье: "))
                mana = int(input("Введите ману: "))
                break
            except ValueError:
                print("Пожалуйста, введите корректное число.")

        if self.role.lower() == "враг":
            return Enemy(health, mana, name)
        else:
            return Character(health, mana, name)


hero_creator = CharMaker("герой")
hero = hero_creator.create()

enemy_creator = CharMaker("враг")
enemy = enemy_creator.create()


def cycle(hero, enemy):
    caster = False
    spell_select = []
    spell_dmg = 0
    spell_check = False
    while hero.health > 0:
        print("\nДоступные команды: status, attack, spell, cast, quit")
        command = input("Введите команду: ").strip().lower()

        if command == "status":
            hero.display()
            continue

        elif command == "spell" and not spell_check:
            caster = True
            spell_dmg, spell_select = hero.spellsList()
            if spell_dmg is not None:
                spell_check = True
                print(f"Вы выбрали заклинание {spell_select} на {spell_dmg} единиц урона")
            else:
                caster = False
            continue


        elif command == "attack":
                    damage = int(input("Введите урон, который враг нанесёт герою: "))
                    enemy.attack(hero, damage)
                    if hero.health <= 0:
                        print("Персонаж мертв")
                        print("Желаете создать нового персонажа?")
                        ans = input("Введите команду yes или no: ").strip().lower()
                        if ans == "yes":
                            hero.health = 0
                            hero.name =""
                            hero.damage = 0
                            newHero = hero_creator.create()
                            hero = newHero
                            cycle(hero, enemy)
                        else:
                            print("Выход из игры")
                            break



        elif command == "cast":
            if hero.mana <= 0:
                print("Недостаточно маны")
                continue
            if caster:
                    spell_name = (input(f"Введите название заклинания. У вас доступны: {spell_select} на {spell_dmg} единиц урона:\n"))
                    if spell_name == spell_select:
                        hero.attack(enemy, spell_dmg)
                        hero.mana = hero.mana - 10
                        spell_check = False
                        caster = False
                    else:
                        print("У вас нету этого заклинания")
            else: print("Выбор заклинания не сделан")

            if hero.health <= 0:
                print("Персонаж мертв")
                print("Желаете создать нового персонажа?")
                ans = input("Введите команду yes или no: ").strip().lower()
                if ans == "yes":
                    hero.health = 0
                    hero.name = ""
                    hero.damage = 0
                    newHero = hero_creator.create()
                    hero = newHero
                    cycle(hero, enemy)
                else:
                        print("Выход из игры")
                continue
        elif command == "quit":
            print("Выход из игры.")
            break
    else:
        print("Неизвестная команда.")

cycle(hero,enemy)