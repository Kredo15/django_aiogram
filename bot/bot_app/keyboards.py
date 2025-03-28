from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
                    ReplyKeyboardMarkup, KeyboardButton


def get_menu_inline():
    buttons = [
        [InlineKeyboardButton(text="Изучать новые слова", callback_data="new_word")],
        [InlineKeyboardButton(text="Слова выученные наполовину", callback_data="word_repetition")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_button_keyboard():
    button_know = KeyboardButton('Знаю')
    button_dont_know = KeyboardButton('Не знаю')
    button_stop = KeyboardButton('Закончить')

    button_keyboard = ReplyKeyboardMarkup()
    button_keyboard.add(button_know)
    button_keyboard.add(button_dont_know)
    button_keyboard.add(button_stop)
    return button_keyboard
