# -*- coding: utf-8 -*-
import vk_api
import config

VK_ABOUT = '''Информация из вк:
Деятельность: {activities}
О себе: {about}

Интересы: {interests}
Музыка: {music}
Книги: {books}
Фильмы: {movies}
Игры: {games}
Тв шоу: {tv}


Цитаты: {quotes}'''

# Двухфакторная аутентификация
def auth_handler():
    key = input('Введите код аутентификации: ')
    remember_device = True

    return key, remember_device

def get_session():
    login, password = config.LOGIN, config.PASSWORD
    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler,
        scope = 'friend',
        api_version = '5.101'
    )
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    return vk_session

def get_friends_ids(vk_session):
    tools = vk_api.VkTools(vk_session)
    tmp_peop = tools.get_all(method='friends.get', max_count=1, values = {'fields' : 'nickname, domain, sex, bdate, city, country,' 
                                                                        'timezone, photo_50, photo_100, photo_200_orig, has_mobile,' 
                                                                        'contacts, education, online, relation, last_seen, status,' 
                                                                        'can_write_private_message, can_see_all_posts, can_post, universities'})
    return tmp_peop.get('items')

def get_photos(owner_id, vk_session):
    tools = vk_api.VkTools(vk_session)
    info_photo = tools.get_all(method='photos.get', max_count=100, values = {'owner_id' : owner_id, 'album_id' : 'wall'})
    return info_photo.get('items')

def main():
    vk_session = get_session()
    for man in get_friends_ids(vk_session):
        print(man['id'], man['last_name'])
        photos_info = get_photos(owner_id=man['id'], vk_session=vk_session)
        try:
            for photo in photos_info:
                print(photo['date'])
        except IndexError:
            continue


if __name__ == '__main__':
    main()