import requests
from django.conf import settings
from users.models import UserExtention


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = f'https://api.vk.com/method/users.get/?fields=sex,about&access_token={response["access_token"]}&v=5.92'

    response = requests.get(api_url)

    if response.status_code != 200:
        return

    data = response.json()['response'][0]

    if 'sex' in data:
        if data['sex'] == 1:
            user.userextention.gender = UserExtention.FEMALE
        elif data['sex'] == 2:
            user.userextention.gender = UserExtention.MALE

    if 'about' in data:
        user.userextention.about_me = data['about']

    user.save()
