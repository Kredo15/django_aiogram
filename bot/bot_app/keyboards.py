from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, KeyboardButton
from .button_signature import STUDY_NEW_WORD, HALF_LEARNED_WORD, KNOW, \
    STUDY, STOP_STUDY, START, MENU


def get_inline_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=MENU, callback_data="menu")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_inline_actions() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=STUDY_NEW_WORD, switch_inline_query_current_chat="categories")],
        [InlineKeyboardButton(text=HALF_LEARNED_WORD, callback_data="repetition_word")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_button_new_word() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text=KNOW)
        ],
        [
            KeyboardButton(text=STUDY)
        ],
        [
            KeyboardButton(text=STOP_STUDY)
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
            KeyboardButton(text=START)
        ],
        [
            KeyboardButton(text=STOP_EXERCISE)
        ],
    ]

    button_keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return button_keyboard
