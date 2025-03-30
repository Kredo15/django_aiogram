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
    kb = [
        [
            KeyboardButton(text='Знаю')
            ],
        [
            KeyboardButton(text='Не знаю')
            ],
        [
            KeyboardButton(text='Закончить')
            ],
        ]

    button_keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return button_keyboard
