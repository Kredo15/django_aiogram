from bot_app.data_fetcher import get_user_data, add_user, add_studied_word, get_auth_user
from bot_app.keyboards import get_actions_new_word, get_actions_all, \
    get_actions_for_learned, get_actions_for_half_learned


async def init_user(user_id: int, username: str) -> dict | None:
    token_user = await get_auth_user(user_id)
    if token_user.get("refresh"):
        user_data = await get_user_data(user_id)
        return user_data
    await add_user(user_id, username)
    await get_auth_user(user_id)
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


async def add_studied_word_in_user_dict(user_id: int, data: dict) -> None:
    json_for_send = {
        "user": user_id,
        "word": data['pk'],
        "translate_choose_ru": True,
        "translate_choose_en": True,
        "translate_write_ru": True,
        "translate_write_en": True,
        "write_word_using_audio": True
    }
    await add_studied_word([json_for_send])


async def add_words_after_exercise(user_id: int, data: dict) -> None:
    json_for_send = []
    for value in data.values():
        tmp_json = {
            "user": user_id,
            "word": value['pk'],
            "translate_choose_ru": value['translate_choose_ru'],
            "translate_choose_en": value['translate_choose_en']
        }
        json_for_send.append(tmp_json)
    await add_studied_word(json_for_send)
