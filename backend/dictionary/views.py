from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_user_data, add_user_data, \
    get_word_for_learn, add_word_for_learn, get_repetition_word, \
    add_word_studied


class DataUser(APIView):
    """Отдаём данные пользователя/
    создаем профиль пользователя"""

    def get(self, user: int = None) -> Response:
        if user:
            return Response(get_user_data(user), status=status.HTTP_200_OK)
        return Response({'message': 'Передайте user'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request) -> Response:
        print(request.data)
        check, data = add_user_data(request.data)
        if check:
            return Response({'message': f'Запись {data} добавлена'}, status=status.HTTP_201_CREATED)
        return Response({'message': f'Ошибка: {data}'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request) -> Response:
        pass


class WordForLearn(APIView):
    """Отдаём слово, которое еще не изучалось/
    добавляем новые слова в словарь"""

    def get(self, user: int = None, name_category: str = None) -> Response:
        if user and name_category:
            return Response(get_word_for_learn(user, name_category).data, status=status.HTTP_200_OK)
        return Response({'message': 'Передайте user и название категории'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request) -> Response:
        check, data = add_word_for_learn(request.data)
        if check:
            return Response({'message': f'Запись {data} добавлена'}, status=status.HTTP_201_CREATED)
        return Response({'message': f'Ошибка: {data}'}, status=status.HTTP_400_BAD_REQUEST)


class RepetitionWord(APIView):
    """Отдаем изученное наполовину слово или для повторения/
     добавляем изученное наполовину слово"""

    def get(self, user: int = None, is_learn: bool = False):
        if user:
            return Response(get_repetition_word(user, is_learn), status=status.HTTP_200_OK)
        return Response({'message': 'Передайте user'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request) -> Response:
        check, data = add_word_studied(request.data)
        if check:
            return Response({'message': f'Запись {data} добавлена'}, status=status.HTTP_201_CREATED)
        return Response({'message': f'Ошибка: {data}'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request) -> Response:
        pass
