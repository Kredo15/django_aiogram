from aiogram.filters.state import State, StatesGroup


class WordsStudy(StatesGroup):
    start = State()
    new_word = State()
    word_repetition = State()
