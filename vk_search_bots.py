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

def main():
    vk_session = get_session()
    tools = vk_api.VkTools(vk_session)
    friends = tools.get_all(method='friends.get', max_count=1, values = {'fields' : 'nickname, domain, sex, bdate, city, country,' 
                                                                        'timezone, photo_50, photo_100, photo_200_orig, has_mobile,' 
                                                                        'contacts, education, online, relation, last_seen, status,' 
                                                                        'can_write_private_message, can_see_all_posts, can_post, universities'})
    for friend in friends['items']:
        print(friend['first_name'], friend['last_name'])


if __name__ == '__main__':
    main()