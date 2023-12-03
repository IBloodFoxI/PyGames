import os
import json
import csv
import random
import sys
import time

locations = {
    "Начало": "Вы находитесь у входа в мрачный лабиринт.",
    "Комната1": "Вы попали засаду гоблинов",
    "Комната2": "По пути вы нашли пару зелий",
    "Комната3": "Вы оказались в комнате с сундуком",
    "Комната4": "Вы заходите в очень тёмную комнату",
    "Комната5": "Вы попадаете в заброшенную библиотеку",
    "выход": "Вы нашли выход из лабиринта! Поздравляю!",
}

actions = {
    "Начало": ["Идти налево", "Идти направо","Посмотреть характеристики"],
    "Комната1": ["Попытаться отбиться", "Попытаться убежать", "Попытаться договориться","Посмотреть характеристики"],
    "Комната2": ["Взять и выпить зелье","Посмотреть характеристики"],
    "Комната3": ["Открыть сундук", "Пройти мимо","Посмотреть характеристики"],
    "Комната4": ["Осмотреться","Посмотреть характеристики"],
    "Комната5": ["Прочитать пару книг", "Пройти мимо","Посмотреть характеристики"],
    "выход": ["Выйти из игры"]
}

HP = 20
chance = 0.5
INT = 0
Luck = chance+(INT/10)
goblin_chance = 0.8
chest_chance = 0.5
leave_chance = 0.05


def describe_location(location):
    print(locations[location])


def make_choice(locations):
    print("Выберите действие:")
    for i, action in enumerate(actions[locations]):
        print(f"{i + 1}. {action}")

    while True:
        try:
            choice = int(input("Введите номер выбранного действия: ")) - 1
            if -1 <= choice < len(actions[locations]):
                return choice
            else:
                print("Некорректный ввод. Пожалуйста, введите номер из списка.")
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите число.")

def save_game(player_name):
    game_state = {
        "Name": player_name,
        "HP": HP,
        "INT": INT,
        "Luck": Luck,
    }

    with open(f"{player_name}_game_state.json", "w") as file:
        json.dump(game_state, file)
    print("Игра сохранена.")

def load_game(player_name):
    global HP, INT, Luck, chance, goblin_chance, chest_chance
    save_file = f"{player_name}_game_state.json"
    if os.path.exists(save_file):
        with open(save_file, "r") as file:
            game_state = json.load(file)
            HP = game_state["HP"]
            INT = game_state["INT"]
            Luck = game_state["Luck"]
            print("Игра загружена.")
    else:
        print("Сохранение не найдено. Начинаем новую игру.")
        HP = 20
        INT = 0
        Luck = chance+(INT/10)
        chance = 0.5
        goblin_chance = 0.8
        chest_chance = 0.5

def delete_save(player_name):
    save_file = f"{player_name}_game_state.json"
    if os.path.exists(save_file):
        os.remove(save_file)
        print(f"Сохранение игры для {player_name} удалено.")
    else:
        print("Сохранение не найдено.")

def update_csv(player_name):
    player_data = []
    csv_file = "player_data.csv"

    if os.path.exists(csv_file):
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            player_data = list(reader)

    updated_player = {
        "Name": player_name,
        "HP": HP,
        "INT": INT,
        "Luck": Luck,
     }

    player_exists = False
    for player in player_data:
        if player["Name"] == player_name:
            player.update(updated_player)
            player_exists = True
            break

    if not player_exists:
        player_data.append(updated_player)

    with open(csv_file, "w", newline="") as file:
        fieldnames = ["Name", "HP", "INT", "Alive"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(player_data)
    print("Данные игроков обновлены в CSV файле.")

print("Добро пожаловать в лабиринт!")
time.sleep(3)
print("Изначально у вас есть 20 хп, если оно опуститься до 0 игра закончится!")
time.sleep(1)
print("Ваша задача выбраться из лабиринта любым способом... Даже можете сбежать из него, вас никто не держит")
print('Напишите "0", что бы сохраниться!!!')
time.sleep(2)
def handle_location(current_location):
    global HP
    global INT
    global chance
    global Luck
    global goblin_chance
    global chest_chance
    global leave_chance

    while True:
        describe_location(current_location)
        choice = make_choice(current_location)

        if choice == -1:
            action = input("Введите 'сохранить', 'загрузить', 'удалить' или 'выйти': ")
            if action.lower() == "сохранить":
                player_name = input("Введите ваше имя: ")
                save_game(player_name)
            elif action.lower() == "загрузить":
                player_name = input("Введите ваше имя: ")
                load_game(player_name)
            elif action.lower() == "удалить":
                player_name = input("Введите ваше имя: ")
                delete_save(player_name)
            elif action.lower() == "выйти":
                update_csv("Player") 
                sys.exit()
    
        match current_location:
            case "Начало":
                if choice == 0:
                    current_location = random.choice(["Комната1", "Комната2", "Комната3", "Комната4", "Комната5",]) 
                elif choice == 1:
                    current_location = random.choice(["Комната1", "Комната2", "Комната3", "Комната4", "Комната5",]) 
                elif choice == 2:
                    print("Характеристики:")
                    print(f"HP: {HP}")
                    print(f"INT: {INT}")
                    print(f"Luck: {Luck * 10}")
                    time.sleep(2)
                    current_location = "Начало"
                    time.sleep(1)
            case "Комната1":
                if choice == 0:
                    print ('Вы попытались напасть на группу гоблинов')
                    if random.random() > chance:
                        HP-=2
                        print ('Вас избили гоблины (-2 хп)')
                        if random.random() > leave_chance:
                            time.sleep(2)
                            current_location = random.choice(["Комната2", "Комната3", "Комната4", "Комната5",])
                        else:
                            current_location = "выход"
                            time.sleep(2)
                    else:
                        print('Вы испугали гоблинов и они разбежались')
                        if random.random() > leave_chance:
                            time.sleep(2)
                            current_location = random.choice(["Комната2", "Комната3", "Комната4", "Комната5",])
                        else:
                            current_location = "выход"
                            time.sleep(2)
                if choice == 1:
                    if random.random() < goblin_chance:
                        print ('Вы так быстро бежали от гоблинов, что выбежали из лабиринта')
                    else:
                        print ('Вы убежали и попали в самое начало')
                        time.sleep(2)
                        current_location = "Начало"
                if choice == 2:
                    if INT >= 20:
                        print ('Вы рассказали гоблинам анекдот, они ничего не поняли, но было интересно. Благодаря вашим умственным способностям они решили показать вам выход! Крутые парни')
                        print ('Конец!')
                        sys.exit()
                    else:
                        print ('Вы рассказали гоблинам анекдот, но они не оценили юмора (-2 хп)')
                        if random.random() > leave_chance:
                            time.sleep(2)
                            current_location = random.choice(["Комната2", "Комната3", "Комната4", "Комната5",])
                        else:
                            current_location = "выход"
                            time.sleep(2)
                if choice == 3:
                    print("Характеристики:")
                    print(f"HP: {HP}")
                    print(f"INT: {INT}")
                    print(f"Luck: {Luck * 10}")
                    time.sleep(2)
                    current_location = "Комната1"
                    time.sleep(1)
            case "Комната2":
                if choice == 0:
                    if random.random() < chance:
                        time.sleep(2)
                        print ('Вы поднимаете зелье и выпиваете его')
                        print ('Вы чувствуете себя так будто выпили аква минерале (+2 хп)')
                        HP+=2
                        if random.random() > leave_chance:
                            time.sleep(2)
                            current_location = random.choice(["Комната1","Комната3", "Комната4", "Комната5",])
                        else:
                            current_location = "выход"
                            time.sleep(2)
                    else:
                        print ('Вы поднимаете зелье и выпиваете его')
                        print ('Вы чувствуете себя так будто выпили горький коффе (-1 хп),(+1 к умственным способностям)')
                        HP-=1
                        INT+=1
                        if random.random() > leave_chance:
                            time.sleep(2)
                            current_location = random.choice(["Комната1","Комната3", "Комната4", "Комната5",])
                        else:
                            current_location = "выход"
                            time.sleep(2)
                if choice == 1:
                    print("Характеристики:")
                    print(f"HP: {HP}")
                    print(f"INT: {INT}")
                    print(f"Luck: {Luck * 10}")
                    time.sleep(2)
                    current_location = "Комната2"
                    time.sleep(1)
            case "Комната3":
                if choice == 0:
                    if random.random() > chance:
                        print ('Вы открываете сундук и вашу руку начинает есть мимик (-1 хп)')
                        HP-=1
                        print ('Неприятно однако')
                        if random.random() > leave_chance:
                            time.sleep(2)
                            current_location = random.choice(["Комната1", "Комната2", "Комната4", "Комната5",])
                        else:
                            current_location = "выход"
                            time.sleep(2)
                    else:
                        print ('Вы открываете сундук, а там....')
                        time.sleep(2)
                        if random.random() < chest_chance:
                            print ('лежит несколько пара зелий лечения, кульно однако (+3 хп)')
                            HP+=3
                            if random.random() > leave_chance:
                                time.sleep(2)
                                current_location = random.choice(["Комната1", "Комната2", "Комната4", "Комната5",])
                            else:
                                current_location = "выход"
                                time.sleep(2)
                        else:
                            print ('лежит пара интересных книг, абуга читать не люблю, придётся (+2 к умственным способностям)')
                            INT+=2
                            if random.random() > leave_chance:
                                time.sleep(2)
                                current_location = random.choice(["Комната1", "Комната2", "Комната4", "Комната5",])
                            else:
                                current_location = "выход"
                                time.sleep(2)
                if choice == 1:
                    print ('Вы решили, что богатства вам ни к чему и прошли мимо сундука')
                    if random.random() > leave_chance:
                        time.sleep(2)
                        current_location = random.choice(["Комната1", "Комната2", "Комната4", "Комната5",])
                    else:
                        current_location = "выход"
                        time.sleep(2)
                if choice == 2:
                    print("Характеристики:")
                    print(f"HP: {HP}")
                    print(f"INT: {INT}")
                    print(f"Luck: {Luck * 10}")
                    time.sleep(2)
                    current_location = "Комната3"
                    time.sleep(1)
            case "Комната4":
                if choice == 0:
                    print ('Комната оказалась ловушкой')
                    if random.random() > Luck:
                        print ('Вам неповезло, вы угодили в ловушку и серьёзно поранились (-5 хп) ')
                        HP-=5
                        if random.random() > leave_chance:
                            time.sleep(2)
                            current_location = random.choice(["Комната1", "Комната2", "Комната3", "Комната5",])
                        else:
                                current_location = "выход"
                                time.sleep(2)
                    else:
                        print ('Вы довольно удачливый и глазастый, поэтому увидели ловушку раньше чем попали в неё')
                        if random.random() > leave_chance:
                            time.sleep(2)
                            current_location = random.choice(["Комната1", "Комната2", "Комната3", "Комната5",])
                        else:
                                current_location = "выход"
                                time.sleep(2)
                if choice == 1:
                    print("Характеристики:")
                    print(f"HP: {HP}")
                    print(f"INT: {INT}")
                    print(f"Luck: {Luck * 10}")
                    time.sleep(2)
                    current_location = "Комната4"
                    time.sleep(1)
            case "Комната5":
                if choice == 0:
                    print ('Вам стало интересно, что за чтиво есть в этой библеотеке.')
                    if random.random() < Luck:
                        print ('Вы нашли пару книг по питону, вы чувствуете как становитесь умнее (+4 к умственным способностям)')
                        INT+=4
                        if random.random() > leave_chance:
                            time.sleep(2)
                            current_location = random.choice(["Комната1", "Комната2", "Комната3", "Комната4",])
                        else:
                                current_location = "выход"
                                time.sleep(2)
                    else:
                        print ('Вы нашли пару книг Говарда Лафкрафта, чтиво интересное, но от него ваше воображение разыгралось... Может за вами кто то следит? (-1 хп (психологический урон) (-1 к умственным способностям)) ')
                        HP-=1
                        INT-=1
                        if random.random() > leave_chance:
                            time.sleep(2)
                            current_location = random.choice(["Комната1", "Комната2", "Комната3", "Комната4",])
                        else:
                                current_location = "выход"
                                time.sleep(2)
                if choice == 1:
                    print ('Вы решили, что быть угабугой самое то и прошли мимо библиотеки')
                    if random.random() > leave_chance:
                        time.sleep(2)
                        current_location = random.choice(["Комната1", "Комната2", "Комната3", "Комната4",])
                    else:
                        current_location = "выход"
                        time.sleep(2)
                if choice == 2:
                    print("Характеристики:")
                    print(f"HP: {HP}")
                    print(f"INT: {INT}")
                    print(f"Luck: {Luck * 10}")
                    time.sleep(2)
                    current_location = "Комната5"
                    time.sleep(1)
            case "выход":
                print('Конец!')
                time.sleep(1)
                print("Вы нашли выход из лабиринта! Поздравляю!")
                if choice == 0:
                    sys.exit()
        
        if HP <= 0:
            print("Ваши хп опустились до нуля. Вы умерли.")
            sys.exit()
        elif HP > 0:
            continue

starting_location = "Начало"
load_game("Player")
handle_location(starting_location)