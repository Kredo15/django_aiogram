from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, KeyboardButton
from .button_signature import STUDY_NEW_WORD, HALF_LEARNED_WORD, KNOW, \
    STUDY, STOP_STUDY, START, MENU, LEARNED_WORD, RATING, HELP


def get_inline_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=MENU, callback_data="menu")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_actions_all() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=STUDY_NEW_WORD, switch_inline_query_current_chat="categories")],
        [InlineKeyboardButton(text=HALF_LEARNED_WORD, callback_data="half_learned_word")],
        [InlineKeyboardButton(text=LEARNED_WORD, callback_data="learned_word")],
        [InlineKeyboardButton(text=RATING, callback_data="ratings")],
        [InlineKeyboardButton(text=HELP, callback_data="help")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_actions_for_learned() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=STUDY_NEW_WORD, switch_inline_query_current_chat="categories")],
        [InlineKeyboardButton(text=LEARNED_WORD, callback_data="learned_word")],
        [InlineKeyboardButton(text=RATING, callback_data="ratings")],
        [InlineKeyboardButton(text=HELP, callback_data="help")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_actions_for_half_learned() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=STUDY_NEW_WORD, switch_inline_query_current_chat="categories")],
        [InlineKeyboardButton(text=HALF_LEARNED_WORD, callback_data="half_learned_word")],
        [InlineKeyboardButton(text=RATING, callback_data="ratings")],
        [InlineKeyboardButton(text=HELP, callback_data="help")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_actions_new_word() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=STUDY_NEW_WORD, switch_inline_query_current_chat="categories")],
        [InlineKeyboardButton(text=RATING, callback_data="ratings")],
        [InlineKeyboardButton(text=HELP, callback_data="help")]
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
            KeyboardButton(text=STOP_STUDY)
        ],
    ]

    button_keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return button_keyboard


def get_buttons_for_choose(buttons_name: list) -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text=name) for i, name in enumerate(buttons_name) if i % 2 == 0],
          [KeyboardButton(text=name) for i, name in enumerate(buttons_name) if i % 2 != 0]]
    kb += [[KeyboardButton(text=STOP_STUDY)]]
    button_keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return button_keyboard
