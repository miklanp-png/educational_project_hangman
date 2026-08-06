import random


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


def words_list(words):
    with open(words, "r", encoding="utf-8") as file:
        words = file.read().split()
    return words


def definition_words(definition_of_words):
    with open(definition_of_words, "r", encoding="utf-8") as file:
        definition = file.read().split(".")
    return definition


def definitions_of_the_secret_word(secret_words):
    answer = input("Дать подсказку в виде определения слова? - напиши: да или нет: ")
    if answer == "да":
        indx = words_list("words.txt").index(secret_words)
        return definition_words("definition_words.txt")[indx].lstrip()
    else:
        return "Играем без подсказки значение слова"


def setting_up_the_display_of_letters_in_advance(secret_words, result, previously_proposed_letter):
    print("Выбери уровень сложности - напиши сколько букв открыть в слове 1 или 2, или напиши нет если не хочешь открыть не одной:")
    numbers_of_letter = input()
    if "1" <= numbers_of_letter <= "2":
        counter = 0
        while int(numbers_of_letter) - counter:
            secret_letter = random.choice(list(secret_words))
            if secret_letter not in previously_proposed_letter:
                counter += 1
                previously_proposed_letter.add(secret_letter)
                for i in range(len(secret_words)):
                    if secret_letter == secret_words[i]:
                        result[i] = secret_letter
        return False
    else:
        return "Все буквы в слове будут закрыты"



def open_secret_letter(secret_words, letter, result):
    for i in range(len(secret_words)):
        if letter == secret_words[i]:
            result[i] = letter
    return result


def demonstration_of_error(letter, previously_proposed_letter, secret_words):
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

    if len(letter) >= 2:
        print("Допустима только одна буква")
        return False

    if "A" <= letter <= "Z":
        print("Допустима только кириллица")
        return False

    if letter not in secret_words:
        print("Не отгадал")
        return True

    return False


def start_stop_game_loop():
    print("Начать новую игру? - напиши: да или нет")
    answer_start_or_stop = input()
    if answer_start_or_stop == "да":
        print("Перед началом игры настрой подсказки")
        return True
    else:
        print("Выход из игры")
        return False


def valid_letter(letter, previously_proposed_letter, secret_words):
    if letter in secret_words and letter not in previously_proposed_letter:
        print("Угадал")
        return True
    return False



def check_win_or_loss(secret_words, result, mistake):
    if mistake >= len(hangman_states) - 1:
        print("Проигрыш,", "загаданное слово:", secret_words)
    elif mistake <= len(hangman_states) and "*" not in result :
        print("Выигрыш")
        print(result)


def start_stop_game_round(mistake, result):
    if mistake >= len(hangman_states) - 1:
        return False
    if "*" not in result:
        return False
    return True


def game_states(mistake):
    print("Ошибок:", mistake)
    print(hangman_states[mistake].lstrip())


def game_loop():
    secret_words = random.choice(words_list("words.txt"))
    result = "*".split() * len(secret_words)
    previously_proposed_letter = set()
    mistake = 0
    print(definitions_of_the_secret_word(secret_words))
    print(setting_up_the_display_of_letters_in_advance(secret_words, result, previously_proposed_letter))


    while start_stop_game_round(mistake, result):
        print(result)
        print("Введите букву")
        letter = input().upper()

        if demonstration_of_error(letter, previously_proposed_letter, secret_words):
            previously_proposed_letter.add(letter)
            mistake += 1

        elif valid_letter(letter, previously_proposed_letter, secret_words):
            open_secret_letter(secret_words, letter, result)
            previously_proposed_letter.add(letter)
        game_states(mistake)
        check_win_or_loss(secret_words, result, mistake)


def hangman_game():
    while start_stop_game_loop():
        game_loop()
hangman_game()





