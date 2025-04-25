from aiogram.fsm.context import FSMContext
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from .app import bot
from .keyboards import get_button_new_word, get_actions_all, \
    get_actions_for_learned, get_actions_for_half_learned, \
    get_actions_new_word, get_button_start_study, get_buttons_for_choose
from .data_fetcher import get_new_word, get_categories, add_studied_word, \
    get_user_data, add_user
import copy
import random


async def init_user(user_id: int, username: str) -> dict | None:
    user_data = await get_user_data(user_id)
    if user_data:
        return user_data
    await add_user(user_id, username)
    return


async def get_actions_depending_user(user_id: int, username: str):
    user = await init_user(user_id, username)
    if not user:
        return get_actions_new_word
    if user.get("number_words_studied") > 0 and user.get("number_half_learned_words") > 0:
        return get_actions_all
    elif user.get("number_words_studied") > 0:
        return get_actions_for_learned
    elif user.get("number_half_learned_words") > 0:
        return get_actions_for_half_learned
    else:
        return get_actions_new_word


async def get_inline_with_categories() -> list[InlineQueryResultArticle]:
    categories = await get_categories()
    results = []
    for value in categories:
        results.append(InlineQueryResultArticle(
            id=value['name'],
            title=value['name'],
            input_message_content=InputTextMessageContent(
                disable_web_page_preview=True,
                message_text=f"learning words from the category {value['name']}"
            )
        ))
    return results


async def get_word_for_learning(user_id: int,
                                name_category: str,
                                pk_old: int
                                ) -> tuple[int, str, str]:
    res = await get_new_word(user_id, name_category, pk_old)
    pk_new = res.get('id')
    en_word = res.get('en_word').get('word')
    ru_word = res.get('ru_word').get('word')
    return pk_new, en_word, ru_word


async def add_studied_word_in_user_dict(user_id: int, data: dict) -> None:
    data_for_send = {
        "user": user_id,
        "word": data['pk'],
        "translate_choose_ru": True,
        "translate_choose_en": True,
        "translate_write_ru": True,
        "translate_write_en": True,
        "write_word_using_audio": True
    }
    await add_studied_word(data_for_send)


async def bot_send_message_new_word(state: FSMContext,
                                    user_id: int = None,
                                    name_category: str = None,
                                    pk_old: int = 0
                                    ) -> None:
    pk_new, en_word, ru_word = await get_word_for_learning(user_id=user_id,
                                                           name_category=name_category,
                                                           pk_old=pk_old)
    message = await bot.send_message(chat_id=user_id,
                                     text=f'{en_word}<span class="tg-spoiler"> - {ru_word}</span>',
                                     parse_mode='html',
                                     reply_markup=get_button_new_word())
    await state.update_data(pk=pk_new,
                            message_id=message.message_id,
                            new_word=dict(en_word=en_word, ru_word=ru_word))


def get_data_after_study(data: dict) -> dict:
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


def get_final_message_for_study(data: dict) -> str:
    result = ""
    for value in data.values():
        result += f"{value['en_word']} - {value['ru_word']}\n"
    return f"Отлично! Готов изучить слова 📚?\n\n{result}"


async def send_final_message_for_study(state: FSMContext,
                                       user_id: int = None,
                                       data_study: dict = None):
    data = await state.get_data()
    message = await bot.send_message(chat_id=user_id,
                                     text=get_final_message_for_study(data_study),
                                     reply_markup=get_button_start_study())
    data["message_id"] = message.message_id
    await state.update_data(data)


def make_list_words(data: dict, exclude: int, word: str):
    """Собираем список для составления выбора слов"""
    make_list = []
    for key, value in data.items():
        if key != exclude:
            make_list.append(value[word])
    return random.choices(make_list, k=2)


def get_en_word_with_choose_ru(key: int, data: dict):
    """Отдаем слово на английском для изучения и
    3 перевода на выбор(1 правильное + 2 случайных)"""
    send_word = data[key]['en_word']
    other_words = make_list_words(data, key, 'ru_word')
    return send_word, random.shuffle([data[key]['ru_word'] + other_words])


def get_ru_word_with_choose_en(key: int, data: dict):
    """Отдаем слово на русском для изучения и
    3 перевода на выбор(1 правильное + 2 случайных)"""
    send_word = data[key]['ru_word']
    other_words = make_list_words(data, key, 'en_word')
    return send_word, random.shuffle([data[key]['en_word'] + other_words])


def get_random_func(data: dict) -> str | None:
    random_key_func = random.choice(list(data.keys()))
    if len(data[random_key_func]) > 0:
        return random_key_func
    else:
        del data[random_key_func]
        try:
            return list(data.keys())[0]
        except IndexError:
            return


async def send_studied_word(state: FSMContext,
                            chat_id: int, data: dict = None):
    """Выбираем рандомно какое слово отправить
    (на английское слово с выбором перевода на русском
    либо русское слово с выбором перевода на английском)
    list_keys_word - список keys слов, которые еще не отправляли
    random_word_key - key слово которое будем отправлять (удаляем его из списка,
    чтобы повторно не отправить)
    получаем слово и 3 перевода для выбора
    отправляем сообщение и обновляем state"""
    funcs = {'choose_en': get_en_word_with_choose_ru,
             'choose_ru': get_ru_word_with_choose_en}
    random_key_func = get_random_func(data.get('start_study'))
    if not data['start_study']:
        bot.send_message(chat_id=chat_id,
                         text="Отлично, ты изучил 5 слов")
        await state.clear()
    elif random_key_func:
        list_keys_word = data.get('start_study').get(random_key_func)
        random_word_key = list_keys_word.pop(random.randrange(len(list_keys_word)))
        word, buttons_name = funcs[random_key_func](random_word_key,
                                                    data.get('study'))
        message = bot.send_message(chat_id=chat_id,
                                   text=word,
                                   reply_markup=get_buttons_for_choose(buttons_name))
        data["message_id"] = message.message_id
        await state.update_data(data)
