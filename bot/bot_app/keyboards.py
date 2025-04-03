from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
                    ReplyKeyboardMarkup, KeyboardButton


def get_menu_inline():
    buttons = [
        [InlineKeyboardButton(text="Изучать новые слова", switch_inline_query_current_chat="categories")],
        [InlineKeyboardButton(text="Слова выученные наполовину", callback_data="repetition_word")]
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
