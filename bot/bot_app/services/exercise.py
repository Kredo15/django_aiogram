import random
import copy
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot_app.app import bot
from bot_app.data_fetcher import get_new_word
from bot_app.keyboards import get_buttons_for_choose
from .user import get_actions_depending_user, add_words_after_exercise


async def get_word_for_learning(user_id: int,
                                name_category: str,
                                pk_old: int
                                ) -> tuple[int, str, str]:
    res = await get_new_word(user_id, name_category, pk_old)
    pk_new = res.get('id')
    en_word = res.get('en_word').get('word')
    ru_word = res.get('ru_word').get('word')
    return pk_new, en_word, ru_word


def get_data_after_choice_word(data: dict) -> dict:
    if data.get('new_word'):
        try:
            update_data = {len(data.get('study')): copy.deepcopy(data['new_word'])}
        except TypeError:
            update_data = {0: copy.deepcopy(data['new_word'])}
        try:
            data['study'].update(update_data)
        except KeyError:
            data['study'] = update_data
        data['new_word'] = None
        return data


def get_data_after_skipping(data: dict) -> dict:
    if data.get('new_word'):
        data['new_word'] = None
        return data


async def send_menu(message: Message):
    user_actions = await get_actions_depending_user(message.from_user.id, message.from_user.username)
    await bot.send_message(chat_id=message.chat.id, text='Выбери действие', reply_markup=user_actions())


def make_list_words(data: dict, exclude: str, word: str):
    """Собираем список для составления выбора слов"""
    make_list = []
    for key, value in data.items():
        if key != exclude:
            make_list.append(value[word])
    return random.sample(make_list, k=3)


def get_en_word_with_choose_ru(key: str, data: dict):
    """Отдаем слово на английском для изучения и
    3 перевода на выбор(1 правильное + 2 случайных)"""
    send_word = data[key]['en_word']
    other_words = make_list_words(data, key, 'ru_word')
    button_names = [data[key]['ru_word']] + other_words
    random.shuffle(button_names)
    return send_word, data[key]['ru_word'], button_names


def get_ru_word_with_choose_en(key: str, data: dict):
    """Отдаем слово на русском для изучения и
    3 перевода на выбор(1 правильное + 2 случайных)"""
    send_word = data[key]['ru_word']
    other_words = make_list_words(data, key, 'en_word')
    button_names = [data[key]['en_word']] + other_words
    random.shuffle(button_names)
    return send_word, data[key]['en_word'], button_names


def check_key_exercise(data: dict) -> bool:
    """Проверяем остались ли неотправленные key"""
    check = False
    remove_key = None
    for key in data.keys():
        if len(data[key]) == 0:
            remove_key = key
        else:
            check = True
    if remove_key:
        del data[remove_key]
    return check


def get_random_key_func(data: dict) -> str | None:
    random_key_func = random.choice(list(data.keys()))
    if len(data[random_key_func]) > 0:
        return random_key_func
    else:
        return


async def finished_exercise(message: Message, state: FSMContext,
                            data: dict):
    await bot.send_message(chat_id=message.chat.id,
                           text="Отлично, за тренировку ты прошел 5 слов")
    await state.clear()
    await send_menu(message)
    await add_words_after_exercise(user_id=message.from_user.id,
                                   data=data)


async def send_studied_word(state: FSMContext,
                            message: Message, data: dict = None):
    """Выбираем рандомно какое слово отправить
    (на английское слово с выбором перевода на русском
    либо русское слово с выбором перевода на английском)
    list_keys_word - список keys слов, которые еще не отправляли
    random_word_key - key слово которое будем отправлять (удаляем его из списка,
    чтобы повторно не отправить)
    получаем слово и 3 перевода для выбора
    отправляем сообщение и обновляем state"""
    funcs = {'translate_choose_en': get_en_word_with_choose_ru,
             'translate_choose_ru': get_ru_word_with_choose_en}
    if check_key_exercise(data.get('exercise')):
        random_key_func = get_random_key_func(data.get('exercise'))
        list_keys_word = data.get('exercise').get(random_key_func)
        random_word_key = list_keys_word.pop(random.randrange(len(list_keys_word)))
        word, true_word, buttons_name = funcs[random_key_func](random_word_key,
                                                               data.get('study'))
        send_message = await bot.send_message(chat_id=message.chat.id,
                                              text=word,
                                              reply_markup=get_buttons_for_choose(buttons_name))
        data["message_id"] = send_message.message_id
        data["current_studied_word"] = {
            "true_word": true_word,
            "key": random_word_key,
            "func": random_word_key
        }
        await state.update_data(data)
    else:
        await finished_exercise(message=message, state=state,
                                data=data.get('exercise'))
