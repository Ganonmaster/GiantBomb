import requests
from collections import Iterable

__author__ = "Leandro Voltolino <xupisco@gmail.com>"
__author__ = "Hidde Jansen <hidde@hiddejansen.com>"
__version__ = "0.7"


class GiantBombError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class Api:
    def __init__(self, api_key, user_agent):
        self.api_key = api_key
        self.base_url = 'https://giantbomb.com/api/'
        self.headers = {'User-Agent': user_agent}
        self.default_parameters = {'api_key': self.api_key, 'format': 'json'}

    @staticmethod
    def defaultRepr(obj):
        return "<{}: {}>".format(obj.id, obj.name)

    def validate_response(self, resp):
        if resp['status_code'] == 1:
            return resp['results']
        else:
            raise GiantBombError('Error code {}: {}}'.format(
                resp['status_code'],
                resp['error']
            ))

    def perform_request(self, url_path, parameters={}):
        url = self.base_url + url_path

        url_parameters = self.default_parameters.copy()
        url_parameters.update(parameters)

        response = requests.get(url, headers=self.headers,
                                params=url_parameters)

        return self.validate_response(response.json())

    def search(self, query, offset=0):
        url_path = 'search/'
        parameters = {
            'resources': 'game',
            'query': query,
            'field_list': ",".join([
                'id',
                'name',
                'image'
            ]),
            'offset': offset
        }
        results = self.perform_request(url_path, parameters)

        return [SearchResult.NewFromJsonDict(x) for x in results]

    def get_game(self, id):
        if not type(id) is int:
            id = id.id
        url_path = 'game/' + str(id) + '/'
        parameters = {
            'field_list': ",".join([
                'id',
                'name',
                'deck',
                'publishers',
                'developers',
                'franchises',
                'image',
                'images',
                'genres',
                'original_release_date',
                'platforms',
                'videos',
                'api_detail_url',
                'site_detail_url',
                'date_added',
                'date_last_updated'
            ]),
        }
        results = self.perform_request(url_path, parameters)

        return Game.NewFromJsonDict(results)

    def list_games(self, plat, offset=0):
        if not type(plat) is int:
            plat = plat.id

        url_path = 'games/'
        parameters = {
            'platforms': plat,
            'field_list': ",".join([
                'id',
                'name',
                'image'
            ]),
            'offset': offset
        }
        results = self.perform_request(url_path, parameters)

        return [SearchResult.NewFromJsonDict(x) for x in results]

    def get_platform(self, id):
        if not type(id) is int:
            id = id.id
        url_path = 'platform/' + str(id) + '/'
        parameters = {
            'field_list': ",".join([
                'id',
                'name',
                'abbreviation',
                'deck',
                'api_detail_url',
                'image'
            ])
        }

        results = self.perform_request(url_path, parameters)
        return Platform.NewFromJsonDict(results)

    def list_platforms(self, offset=0):
        url_path = 'platforms/'
        parameters = {
            'field_list': ",".join([
                'id',
                'name',
                'abbreviation',
                'deck'
            ]),
            'offset': offset
        }
        results = self.perform_request(url_path, parameters)

        return [SearchResult.NewFromJsonDict(x) for x in results]


class Game:
    def __init__(self,
                 id=None,
                 name=None,
                 deck=None,
                 platforms=None,
                 developers=None,
                 publishers=None,
                 franchises=None,
                 image=None,
                 images=None,
                 genres=None,
                 original_release_date=None,
                 videos=None,
                 api_detail_url=None,
                 site_detail_url=None,
                 date_added_gb=None,
                 date_last_updated_gb=None):

        self.id = id
        self.name = name
        self.deck = deck
        self.platforms = platforms
        self.developers = developers
        self.publishers = publishers
        self.franchises = franchises
        self.image = image
        self.images = images
        self.genres = genres
        self.original_release_date = original_release_date
        self.videos = videos
        self.api_detail_url = api_detail_url
        self.site_detail_url = site_detail_url
        self.date_added_gb = date_added_gb
        self.date_last_updated_gb = date_last_updated_gb

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            franchises_check = data.get('franchises', [])
            platforms_check = data.get('platforms', [])
            images_check = data.get('images', [])
            genres_check = data.get('genres', [])
            videos_check = data.get('videos_check', [])
            list_check = {
                'franchise': franchises_check,
                'platform': platforms_check,
                'image': images_check,
                'genre': genres_check,
                'video': videos_check
            }

            for item in list_check:
                if not isinstance(list_check[item], Iterable):
                    list_check[item] = None

            return Game(id=data.get('id'),
                        name=data.get('name', None),
                        deck=data.get('deck', None),
                        platforms=list_check['platform'],
                        developers=data.get('developers', None),
                        publishers=data.get('publishers', None),
                        franchises=list_check['franchise'],
                        image=Image.NewFromJsonDict(data.get('image', [])),
                        images=list_check['image'],
                        genres=list_check['genre'],
                        original_release_date=data.get('original_release_date', None),
                        videos=list_check['video'],
                        api_detail_url=data.get('api_detail_url', None),
                        site_detail_url=data.get('site_detail_url', None),
                        date_added_gb=data.get('date_added', None),
                        date_last_updated_gb=data.get('date_last_updated', None))
        return None

    def __repr__(self):
        return Api.defaultRepr(self)


class Platform:
    def __init__(self,
                 id=None,
                 name=None,
                 abbreviation=None,
                 deck=None,
                 api_detail_url=None,
                 image=None):

        self.id = id
        self.name = name
        self.abbreviation = abbreviation
        self.deck = deck
        self.api_detail_url = api_detail_url
        self.image = image

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            return Platform(id=data.get('id'),
                            name=data.get('name', None),
                            abbreviation=data.get('abbreviation', None),
                            deck=data.get('deck', None),
                            api_detail_url=data.get('api_detail_url', None),
                            image=Image.NewFromJsonDict(data.get('image', None)))
        return None

    def __repr__(self):
        return Api.defaultRepr(self)


class Franchise:
    def __init__(self,
                 id=None,
                 name=None,
                 deck=None,
                 api_detail_url=None,
                 image=None):

        self.id = id
        self.name = name
        self.deck = deck
        self.api_detail_url = api_detail_url
        self.image = image

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            return Franchise(id=data.get('id'),
                             name=data.get('name', None),
                             deck=data.get('deck', None),
                             api_detail_url=data.get('api_detail_url', None),
                             image=Image.NewFromJsonDict(data.get('image', None)))
        return None

    def __repr__(self):
        return Api.defaultRepr(self)


class Image:
    def __init__(self,
                 icon=None,
                 medium=None,
                 tiny=None,
                 small=None,
                 thumb=None,
                 screen=None,
                 super=None):

        self.icon = icon
        self.medium = medium
        self.tiny = tiny
        self.small = small
        self.thumb = thumb
        self.screen = screen
        self.super = super

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            return Image(icon=data.get('icon_url', None),
                         medium=data.get('medium_url', None),
                         tiny=data.get('tiny_url', None),
                         small=data.get('small_url', None),
                         thumb=data.get('thumb_url', None),
                         screen=data.get('screen_url', None),
                         super=data.get('super_url', None),)
        return None

class Genre:
    def __init__(self,
                 id=None,
                 name=None,
                 api_detail_url=None):

        self.id = id
        self.name = name
        self.api_detail_url = api_detail_url

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            return Genre(id=data.get('id'),
                         name=data.get('name', None),
                         api_detail_url=data.get('api_detail_url', None))
        return None

    def __repr__(self):
        return Api.defaultRepr(self)


class Videos:
    def __init__(self,
                 id=None,
                 name=None,
                 deck=None,
                 image=None,
                 url=None,
                 publish_date=None):

        self.id = id
        self.name = name
        self.deck = deck
        self.image = image
        self.url = url
        self.publish_date = publish_date

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            return Videos(id=data.get('id'),
                          name=data.get('name', None),
                          deck=data.get('deck', None),
                          image=Image.NewFromJsonDict(data.get('image', None)),
                          url=data.get('url', None),
                          publish_date=data.get('publish_date', None),)
        return None

    def __repr__(self):
        return Api.defaultRepr(self)


class Video:
    def __init__(self,
                 id=None,
                 name=None,
                 deck=None,
                 image=None,
                 url=None,
                 publish_date=None,
                 site_detail_url=None):

        self.id = id
        self.name = name
        self.deck = deck
        self.image = image
        self.url = url
        self.publish_date = publish_date
        self.site_detail_url = site_detail_url

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            return Video(id=data.get('id'),
                         name=data.get('name', None),
                         deck=data.get('deck', None),
                         image=Image.NewFromJsonDict(data.get('image', None)),
                         url=data.get('url', None),
                         publish_date=data.get('publish_date', None),
                         site_detail_url=data.get('site_detail_url', None))
        return None

    def __repr__(self):
        return Api.defaultRepr(self)


class SearchResult:
    def __init__(self,
                 id=None,
                 name=None,
                 api_detail_url=None,
                 image=None):

        self.id = id
        self.name = name
        self.api_detail_url = api_detail_url
        self.image = image

    @staticmethod
    def NewFromJsonDict(data):
        if data:
            return SearchResult(id=data.get('id'),
                                name=data.get('name', None),
                                api_detail_url=data.get('api_detail_url', None),
                                image=data.get('image', None))
        return None

    def __repr__(self):
        return Api.defaultRepr(self)
