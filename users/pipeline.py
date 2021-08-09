from datetime import datetime
import requests
from django.conf import settings
from social_core.exceptions import AuthForbidden

from users.models import UserExtention


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = f'https://api.vk.com/method/users.get/?fields=bdate,sex,about,photo_max_orig&access_token={response["access_token"]}&v=5.92'

    response = requests.get(api_url)

    if response.status_code != 200:
        return

    data = response.json()['response'][0]

    if 'sex' in data:
        if data['sex'] == 1:
            user.userextention.gender = UserExtention.FEMALE
        elif data['sex'] == 2:
            user.userextention.gender = UserExtention.MALE

    if 'photo_max_orig' in data:
        photo_content = requests.get(data['photo_max_orig'])
        with open(f'{settings.MEDIA_ROOT}/users_images/{user.pk}.jpg', 'wb') as photo_file:
            photo_file.write(photo_content.content)
            user.image = f'users_images/{user.pk}.jpg'

    if 'about' in data:
        user.userextention.about_me = data['about']

    if 'bdate' in data:
        bdate = datetime.strptime(data['bdate'], "%d.%m.%Y").date()

        print(datetime.now().date() - bdate)

        if (datetime.now().date() - bdate).days < 18 * 365.25:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.userextention.age = bdate

    user.save()
