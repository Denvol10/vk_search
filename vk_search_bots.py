# -*- coding: utf-8 -*-
import vk_api
import config
import model
from model import VkPage, VkPhoto, VkWall

# Двухфакторная аутентификация
def auth_handler():
    key = input('Введите код аутентификации: ')
    remember_device = True

    return key, remember_device

# Создание сессии в VK
def get_session():
    login, password, client_secret, token = config.LOGIN, config.PASSWORD, config.SERVIS_KEY, config.TOKEN
    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler,
        scope = 'friend',
        api_version = '5.101',
        app_id = 7060768,
        token = token,
        client_secret = client_secret
    )
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    return vk_session

# Получение информации о вк страницах, которые находятся в списке друзей
def get_friends_ids(vk_session):
    tools = vk_api.VkTools(vk_session)
    tmp_peop = tools.get_all(method='friends.get', max_count=100, values = {'fields': 'nickname, domain'})
    return tmp_peop.get('items')

# Получение информации о вк страницах, которые находятся в текстовом документе
def get_company_ids():
    with open('company.txt', 'r', encoding='ptcp154') as company_file:
        company_list = list(company_file.read().split('\n'))
    vk_session = vk_api.VkApi(app_id = config.APP_ID, token = config.TOKEN, client_secret = config.SERVIS_KEY)
    vk_session.server_auth()
    vk_session.token = {'access_token': config.TOKEN, 'expires_in': 0}
    vk = vk_session.get_api()
    tmp_comp = vk.users.get(user_ids = company_list)
    print(tmp_comp)
    return tmp_comp

# Получение информации о фотографиях находящихся на стене страницы
def get_photos(owner_id, vk_session):
    tools = vk_api.VkTools(vk_session)
    try:
        info_photo = tools.get_all(method='photos.get', max_count=100, values = {'owner_id' : owner_id, 'album_id' : 'wall'})
    except Exception:
        return
    return info_photo

# Получение информации о записях на стене
def get_walls(owner_id, vk_session):
    tools = vk_api.VkTools(vk_session)
    try:
        wall_info = tools.get_all(method='wall.get', max_count=100, values = {'owner_id' : owner_id, 'count' : 20, 'filter' : 'owner'})
    except Exception:
        return
    return wall_info

# Функция добавления VK страниц в базу данных
def save_vk_page(vk_session):
    for man in get_friends_ids(vk_session):
        page_exists = (VkPage.query.filter(VkPage.page_id == man['id']).first())
        if not page_exists and man['first_name'] != 'DELETED':
            page = VkPage(page_id = man['id'], pagename = f"{man['first_name']} {man['last_name']}")
            model.db_session.add(page)
            model.db_session.commit()
    return 'vk_pages saved'

# Функция сохранения информации в базу данных о фотографиях, расположенных на стене страницы VK
def save_photo_data(vk_session):
    print('Сохранение информации о фотографиях')
    for man in get_friends_ids(vk_session):
        print(man['id'], man['last_name'])
        photos_info = get_photos(owner_id=man['id'], vk_session=vk_session)
        photos_exists = VkPhoto.query.filter(VkPhoto.photo_id == man['id']).first()
        if not photos_exists:
            page_id = VkPage.query.filter(VkPage.page_id == man['id']).first().id
            photo_id = VkPage.query.filter(VkPage.page_id == man['id']).first().page_id
            count_photos = photos_info.get('count') # количество фотографий
            photography = VkPhoto(page_id = page_id, photo_id = photo_id, count_photos = count_photos)
            model.db_session.add(photography)
            model.db_session.commit()
    return 'photo_info saved'

# Функция сохранения информации в базу данных о стене пользователя
def save_wall_data(vk_session):
    print('Сохранение информации о стене пользователя')
    for man in get_friends_ids(vk_session):
        print(man['id'], man['last_name'])
        wall_info = get_walls(owner_id=man['id'], vk_session=vk_session)
        wall_exists = VkWall.query.filter(VkWall.wall_id == man['id']).first()
        if not wall_exists:
            page_id = VkPage.query.filter(VkPage.page_id == man['id']).first().id
            try:
                wall_id = wall_info.get('items')[0]['owner_id']
            except (IndexError, TypeError):
                continue
            posts_count = wall_info.get('count') # количество постов
            print(posts_count, wall_id)
            try:
                likes_count = 0
                reposts_count = 0
                for wall in wall_info.get('items'):
                    likes_count += wall['likes'].get('count')
                    reposts_count += wall['reposts'].get('count')
                print(likes_count, reposts_count)
            except (IndexError, TypeError):
                continue
        wall = VkWall(page_id=page_id, wall_id=wall_id, posts_count=posts_count, likes_count=likes_count, reposts_count=reposts_count)
        model.db_session.add(wall)
        model.db_session.commit()
    return 'wall info saved'

# Функция добавления VK страниц компаний в базу данных
def save_vk_page_company():
    for company in get_company_ids():
        page_exists = (VkPage.query.filter(VkPage.page_id == company['id']).first())
        if not page_exists and company['first_name'] != 'DELETED':
            page = VkPage(page_id = company['id'], pagename = f"{company['first_name']} {company['last_name']}")
            model.db_session.add(page)
            model.db_session.commit()
    return 'vk_pages saved'

# Функция сохранения информации в базу данных о фотографиях, расположенных на стене страницы VK рекламных страниц
def save_photo_data_company(vk_session):
    print('Сохранение информации о фотографиях')
    for company in get_company_ids():
        print(company['id'], company['last_name'])
        photos_info = get_photos(owner_id=company['id'], vk_session=vk_session)
        photos_exists = VkPhoto.query.filter(VkPhoto.photo_id == company['id']).first()
        if not photos_exists:
            page_id = VkPage.query.filter(VkPage.page_id == company['id']).first().id
            photo_id = VkPage.query.filter(VkPage.page_id == company['id']).first().page_id
            count_photos = photos_info.get('count') # количество фотографий
            photography = VkPhoto(page_id = page_id, photo_id = photo_id, count_photos = count_photos)
            model.db_session.add(photography)
            model.db_session.commit()
    return 'photo_info saved'

# Функция сохранения информации в базу данных о стене рекламной страницы
def save_wall_data_company(vk_session):
    print('Сохранение информации о стене пользователя')
    for company in get_company_ids():
        print(company['id'], company['last_name'])
        wall_info = get_walls(owner_id=company['id'], vk_session=vk_session)
        wall_exists = VkWall.query.filter(VkWall.wall_id == company['id']).first()
        if not wall_exists:
            page_id = VkPage.query.filter(VkPage.page_id == company['id']).first().id
            try:
                wall_id = wall_info.get('items')[0]['owner_id']
            except (IndexError, TypeError, AttributeError):
                continue
            print(wall_id)
            try:
                posts_count = wall_info.get('count') # количество постов
                likes_count = 0
                reposts_count = 0
                for wall in wall_info.get('items'):
                    likes_count += wall['likes'].get('count')
                    reposts_count += wall['reposts'].get('count')
                print(likes_count, reposts_count)
            except (IndexError, TypeError, AttributeError):
                continue
            wall = VkWall(page_id=page_id, wall_id=wall_id, posts_count=posts_count, likes_count=likes_count, reposts_count=reposts_count)
            model.db_session.add(wall)
            model.db_session.commit()
    return 'wall info saved'

def main():
    vk_session = get_session()
    # сохранение страниц VK в базу данных
    save_vk_page(vk_session)

    # сохранение информации о фотографиях страниц VK в базу данных
    save_photo_data(vk_session)

    # сохранение информации о стенах
    save_wall_data(vk_session)

    # сохранение рекламных страниц в базу данных
    save_vk_page_company()

    # сохранение информации о фотографиях рекламных страниц VK в базу данных
    save_photo_data_company(vk_session)

    # сохранение информации о стенах рекламных страниц
    save_wall_data_company(vk_session)


if __name__ == '__main__':
    main()