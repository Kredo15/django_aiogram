from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_user_data, add_user_data, \
    get_word_for_study, add_word_for_study, get_studied_word, \
    add_word_studied, get_all_categories, add_category, update_user_data, \
    update_word_studied, get_all_ratings, add_ratings


class RatingsData(APIView):
    """Отдаём название рейтингов/
    создаем название рейтингов"""

    def get(self, request):
        return Response(get_all_ratings(), status=status.HTTP_200_OK)

    def post(self, request):
        check, data = add_ratings(request.data)
        if check:
            return Response({'message': f'Запись {data} добавлена'}, status=status.HTTP_201_CREATED)
        return Response({'message': f'Ошибка: {data}'}, status=status.HTTP_400_BAD_REQUEST)


class UserData(APIView):
    """Отдаём данные пользователя/
    создаем профиль пользователя"""

    def get(self, request):
        user = request.query_params.get('user')
        if user:
            return Response(get_user_data(user), status=status.HTTP_200_OK)
        return Response({'message': 'Передайте user'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        check, data = add_user_data(request.data)
        if check:
            return Response({'message': f'Запись {data} добавлена'}, status=status.HTTP_201_CREATED)
        return Response({'message': f'Ошибка: {data}'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        check, data = update_user_data(request.data)
        if check:
            return Response({'message': f'Запись {data} обновлена'}, status=status.HTTP_202_ACCEPTED)
        return Response({'message': f'Ошибка: {data}'}, status=status.HTTP_400_BAD_REQUEST)


class CategoriesData(APIView):
    """Отдаём все категории"""
    def get(self, request):
        return Response(get_all_categories(), status=status.HTTP_200_OK)

    def post(self, request):
        check, data = add_category(request.data)
        if check:
            return Response({'message': f'Запись {data} добавлена'}, status=status.HTTP_201_CREATED)
        return Response({'message': f'Ошибка: {data}'}, status=status.HTTP_400_BAD_REQUEST)


class WordForStudy(APIView):
    """Отдаём слово, которое еще не изучалось/
    добавляем новые слова в словарь"""

    def get(self, request):
        user = request.query_params.get('user')
        name_category = request.query_params.get('name_category')
        pk = int(request.query_params.get('pk'))
        if user and name_category:
            return Response(get_word_for_study(
                user=user,
                name_category=name_category,
                pk=pk
            ), status=status.HTTP_200_OK)
        return Response({'message': 'Передайте user и название категории'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        check, data = add_word_for_study(request.data)
        if check:
            return Response({'message': f'Запись {data} добавлена'}, status=status.HTTP_201_CREATED)
        return Response({'message': f'Ошибка: {data}'}, status=status.HTTP_400_BAD_REQUEST)


class WordFromUserDictionary(APIView):
    """Отдаем изученное наполовину слово или для повторения/
     добавляем изученное слово"""

    def get(self, request):
        user = request.query_params.get('user')
        is_learn = request.query_params.get('is_learn')
        if user:
            return Response(get_studied_word(user), status=status.HTTP_200_OK)
        return Response({'message': 'Передайте user'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        check, data = add_word_studied(request.data)
        if check:
            return Response({'message': f'Запись {data} добавлена'}, status=status.HTTP_201_CREATED)
        return Response({'message': f'Ошибка: {data}'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        check, data = update_word_studied(request.data)
        if check:
            return Response({'message': f'Запись {data} обновлена'}, status=status.HTTP_202_ACCEPTED)
        return Response({'message': f'Ошибка: {data}'}, status=status.HTTP_400_BAD_REQUEST)
