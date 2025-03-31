from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
                    ReplyKeyboardMarkup, KeyboardButton

category = ["popular_word", "animals_word", "colloquial_phrases"]


def get_menu_inline():
    buttons = [
        [InlineKeyboardButton(text="Изучать новые слова", callback_data="new_word")],
        [InlineKeyboardButton(text="Слова выученные наполовину", callback_data="repetition_word")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_category_inline():
    buttons = [
        [InlineKeyboardButton(text="Популярные слова", callback_data="popular_word")],
        [InlineKeyboardButton(text="Животные", callback_data="animals_word")],
        [InlineKeyboardButton(text="Разговорные фразы", callback_data="colloquial_phrases")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_button_keyboard():
    kb = [
        [
            KeyboardButton(text='Знаю')
            ],
        [
            KeyboardButton(text='Изучать')
            ],
        [
            KeyboardButton(text='Закончить упражнение')
            ],
        ]

    button_keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return button_keyboard
