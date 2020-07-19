import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from instagram.items import InstagramItem

# parse_user = ['artificial_intelligence_ml','machinelearning.py']

class InstaspyderSpider(scrapy.Spider):
    name = 'instaspyder'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']

    insta_login = '_golf_r20'
    insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1595059699:AQ1QAI1NQu+cZaRO3S6489MQg5vDMHK/vL5CSwlpHcN3UncdpjcZXxHlUXgwqzF03kWHh0h3gxHgHxl9h1BsbvddZk2BsgyOri5uDzlf+pOSp5wOnJMcp4M60ysPlzy0sFC8+8HWgLpIW6k7'
    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'

    parse_user = 'machinelearning.py' # 2-ой аккаунт просто добавить сделать списком НЕ ПОЛУЧИЛОСЬ

    post_hash = 'c76146de99bb02f6415203be841dd25a'
    graphql_url = 'https://www.instagram.com/graphql/query/?'

    post_hash_podpiski = 'd04b0a864b4b54837c0d870b0e77e076'


    def parse(self, response: HtmlResponse):
        yield scrapy.FormRequest(
            self.insta_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pass},
            headers={'X-CSRFToken': self.fetch_csrf_token(response.text)}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:  # Проверяем ответ после авторизации

            # здесь пишем цикл для нескольких пользователей НЕ ПОЛУЧИЛОСЬ НОРМАЛЬНО РАЗДЕЛИТЬ НА КОЛЛЕКЦИИ. ПОЭТОМУ УБРАЛ
            yield response.follow(
                # Переходим на желаемую страницу пользователя. Сделать цикл для кол-ва пользователей больше 2-ух
                f'/{self.parse_user}',
                callback=self.user_data_parse,
                cb_kwargs={'username': self.parse_user}
                )
    # подписчики

    def user_data_parse(self, response: HtmlResponse, username):

        user_id = self.fetch_user_id(response.text, username)

        variables = {"id": user_id,
                     "include_reel": 'true',
                     "fetch_mutual": 'false',
                     "first":41,
                     }

        url_posts = f'{self.graphql_url}query_hash={self.post_hash}&{urlencode(variables)}'

        yield response.follow(
            url_posts,
            callback= self.user_posts_parse,
            cb_kwargs= {'username': username, 'user_id': user_id, 'variables': deepcopy(variables)}
        )

    # разбор подписчиков

    def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_posts = f'{self.graphql_url}query_hash={self.post_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback= self.user_posts_parse,
                cb_kwargs={'username': username, 'user_id': user_id, 'variables': deepcopy(variables)}
            )

        subscribers = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        for subscriber in subscribers:
            item = InstagramItem(
                user_id = user_id,
                user_name = subscriber['node']['username'],
                full_name = subscriber['node']['full_name'],
                photo = subscriber['node']['profile_pic_url']
            )
            yield item


    # подписки NEW

    def user_data_parse1(self, response: HtmlResponse, username):

        user_id = self.fetch_user_id(response.text, username)

        variables = {"id": user_id,
                     "include_reel": 'true',
                     "fetch_mutual": 'false',
                     "first": 41,
                     }

        url_posts_podpiski = f'{self.graphql_url}query_hash={self.post_hash_podpiski}&{urlencode(variables)}'

        yield response.follow(
            url_posts_podpiski,
            callback=self.user_posts_parse1,
            cb_kwargs={'username': username, 'user_id': user_id, 'variables': deepcopy(variables)}
        )


    # разбор подписок NEW

    def user_posts_parse1(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_posts = f'{self.graphql_url}query_hash={self.post_hash_podpiski}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback= self.user_posts_parse1,
                cb_kwargs={'username': username, 'user_id': user_id, 'variables': deepcopy(variables)}
            )

        subscribers_podpiski = j_data.get('data').get('user').get('edge_follow').get('edges')
        for subscriber in subscribers_podpiski:
            item = InstagramItem(
                user_id = user_id,
                user_name = subscriber['node']['username'],
                full_name = subscriber['node']['full_name'],
                photo = subscriber['node']['profile_pic_url']
            )
            yield item


    # Токен пользователя
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
