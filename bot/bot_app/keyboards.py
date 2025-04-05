from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
                    ReplyKeyboardMarkup, KeyboardButton


def get_menu_inline() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Изучать новые слова", switch_inline_query_current_chat="categories")],
        [InlineKeyboardButton(text="Слова выученные наполовину", callback_data="repetition_word")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_button_new_word() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text='😎 Знаю')
            ],
        [
            KeyboardButton(text='🤷‍♀️ Изучать')
            ],
        [
            KeyboardButton(text='✋ Закончить упражнение')
            ],
        ]

    button_keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return button_keyboard


def get_button_start_study() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text='🚀 Поехали')
        ],
        [
            KeyboardButton(text='✋ Закончить упражнение')
        ],
    ]

    button_keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return button_keyboard
