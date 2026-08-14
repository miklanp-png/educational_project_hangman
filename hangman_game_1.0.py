import random
import json
import os


game_script = os.path.dirname(os.path.abspath(__file__))
words = os.path.join(game_script, "words_1.0.json")


zero = ('''
|========
|       
|
|
|
|''')

one = ('''
|========
|       |
|
|
|
|''')

two = ('''
|========
|       |
|       0
|       
|
|''')

three = ('''
|========
|       |
|       0
|      ( )
|
|''')

four = ('''
|========
|       |
|       0
|   >-<( )>-<
|   
|''')

five = ('''
|========
|       |
|       0
|   >-<( )>-<
|      / \\
|    _/   \\_''')


hangman_states = (zero, one, two, three, four, five)


def get_list_words() -> dict:
    with open("words_1.0.json", "r", encoding="utf-8") as file:
        return json.load(file)


list_words = get_list_words()


def definitions_secret_word(secret_word: str) -> None:
    answer = input("Дать подсказку в виде определения слова? - напиши: да или нет: ")
    if answer == "да":
        print("Определение секретного слова:", list_words[secret_word])

    else:
        print("Играем без подсказки значение слова")


def open_secret_letter(secret_words: str, letter: str, result: list) -> list:
    for i in range(len(secret_words)):
        if letter == secret_words[i]:
            result[i] = letter

    return result


def print_error(letter: str, previously_proposed_letter: set, secret_words: str) -> bool:
    if letter == " ":
        print("Это пробел")
        return False

    if letter == "":
        print("Это пустая строка")
        return False

    if letter in previously_proposed_letter:
        print("Данная буква уже использована")
        return False

    if "0" <= letter <= "9":
        print("Введёна цифра")
        return False

    if 1 < len(letter) <= 3:
        print("Допустима только одна буква или введи всё слова целиком")
        return False

    if len(letter) >= 4:
        print("Ты наверное ввел всё слова целиком, но не отгадал")
        return True

    if "A" <= letter <= "Z":
        print("Допустима только кириллица")
        return False

    if letter in '=-+{}[]!"№;%():?':
        print("Не корректный ввод")
        return False

    if letter not in secret_words:
        print("Не отгадал")
        return True

    return False


def run_game_loop() -> bool:
    print("Начать новую игру? - напиши: да или нет")
    answer_start_or_stop = input().lower()
    if answer_start_or_stop == "да":
        print("Перед началом игры настрой подсказки")
        return True

    else:
        print("Выход из игры")
        return False


def validate_letter(letter: str, previously_proposed_letter: set, secret_word: str) -> bool:
    if letter in secret_word and letter not in previously_proposed_letter:
        print("Угадал")
        return True

    return False


def check_end_game(result: list, mistake: int) -> str:
    if mistake <= len(hangman_states) and "*" not in result:
        return "win"

    elif mistake >= len(hangman_states) - 1:
        return "loss"

    return "game_continue"


def check_game_round(mistake: int, result: list) -> bool:
    if mistake >= len(hangman_states) - 1:
        return False

    if "*" not in result:
        return False

    return True


def print_game_states(mistake: int) -> None:
    print("Ошибок:", mistake)
    print(hangman_states[mistake].lstrip())


def get_number_of_hint_letters() -> bool | str:
    print("Выбери уровень сложности - напиши сколько букв открыть в загаданном слове 1 или 2, или напиши любой другой символ если не хочешь открыть не одной буквы:")
    numbers_of_letter = input()

    if numbers_of_letter in ("1", "2"):
       return numbers_of_letter

    return False


def get_random_letter(secret_word: str, previously_proposed_letter: set) -> str | None:
    while True:
        chosen_letter = random.choice(list(secret_word))
        if chosen_letter not in previously_proposed_letter:
            return chosen_letter

        elif previously_proposed_letter == set(secret_word): #Страховка от бесконечного цикла хотя по факту это условие не выполнится, можно обойтись без него.
            return None


def game_loop() -> None:
    secret_word = random.choice(list(list_words.keys()))
    result = ["*"] * len(secret_word)
    previously_proposed_letter = set()
    mistake = 0
    definitions_secret_word(secret_word)
    letters_to_open_count = get_number_of_hint_letters()

    if letters_to_open_count:
        print("Количество открытых букв в загаданном слове:", letters_to_open_count)
        open_letter_counter = 0
        while int(letters_to_open_count) > open_letter_counter:
            open_letter_counter += 1
            get_random_letter(secret_word, previously_proposed_letter)
            random_letter = get_random_letter(secret_word, previously_proposed_letter)
            open_secret_letter(secret_word, random_letter, result)
            previously_proposed_letter.add(random_letter)

    else:
        print("Все буквы в слове будут закрыты")

    while check_game_round(mistake, result):
        print(result)
        print("Введите букву")
        letter = input().upper()

        if print_error(letter, previously_proposed_letter, secret_word):
            previously_proposed_letter.add(letter)
            mistake += 1

        elif validate_letter(letter, previously_proposed_letter, secret_word):
            open_secret_letter(secret_word, letter, result)
            previously_proposed_letter.add(letter)

        print_game_states(mistake)

        if check_end_game(result, mistake) == "win":
            print("Выйгрыш!, загаданное слово:", secret_word)

        elif check_end_game(result, mistake) == "loss":
            print("Проигрыш, загаданное слово:", secret_word)

        elif letter == secret_word:
            print("Ты отгадал слова целиком!", secret_word)
            break

        else:
            print("Игра продолжается")


def hangman_game() -> None:
    while run_game_loop():
        game_loop()


if __name__ == "__main__":
    hangman_game()
