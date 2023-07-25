import requests
from urllib3.util import parse_url

from ratelimit import RateLimit
from photo import PhotosResponse, Photo
from video import Video, VideosResponse
from collection import CollectionsResponse, CollectionMedia


class Pexels:
    def __init__(self, api: str) -> None:
        # self.__api = api
        self.__base_url = 'https://api.pexels.com/v1/'
        self.__base_video_url = 'https://api.pexels.com/videos/'
        self.__session = requests.session()
        self.__session.headers['Authorization'] = api

        self.ratelimit: RateLimit = RateLimit()

    def _search(self, url: str, params: dict = None):
        resp = self.__session.get(url, params=params)
        resp.raise_for_status()

        self.ratelimit.update(resp)

        parsed_url = parse_url(url)

        if parsed_url.path.startswith("/v1/videos"):
            return VideosResponse(**resp.json())
        elif parsed_url.path.startswith('/v1/collections'):
            return CollectionsResponse(**resp.json())
        return PhotosResponse(**resp.json())

    def _create_navigation_function(self, url: str = None):
        if not url:
            return

        def navigation(params: dict = None):
            resp = self.__session.get(url, params=params)
            resp.raise_for_status()

            self.ratelimit.update(resp)

            parsed_url = parse_url(url)

            if parsed_url.path.startswith("/v1/videos"):
                return VideosResponse(**resp.json())
            elif parsed_url.path.startswith('/v1/collections'):
                return CollectionsResponse(**resp.json())
            return PhotosResponse(**resp.json(), create_nav=self._create_navigation_function)

        return navigation

    def search_photos(self,
                      query: str,
                      orientation: str | None = None,
                      size: str | None = None,
                      color: str | None = None,
                      locale: str | None = None,
                      page: int = 1,
                      per_page: int = 15
                      ) -> PhotosResponse:

        resp = self.__session.get(
            url=f"{self.__base_url}search",
            params={
                "query": query,
                "orientation": orientation,
                "size": size,
                "color": color,
                "locale": locale,
                "page": page,
                "per_page": per_page
            })
        resp.raise_for_status()

        self.ratelimit.update(resp)

        data = resp.json()

        return PhotosResponse(**data, create_nav = self._create_navigation_function)

    def curated_photos(self, page: int = 1, per_page: int = 15) -> PhotosResponse:
        resp = self.__session.get(
            url=f"{self.__base_url}curated",
            params={
                "page": page,
                "per_page": per_page
            }
        )

        resp.raise_for_status()

        self.ratelimit.update(resp)

        return PhotosResponse(**resp.json())

    def get_photo(self, id: int) -> Photo:  # noqa
        resp = self.__session.get(url=f"{self.__base_url}photos/{id}")
        resp.raise_for_status()

        self.ratelimit.update(resp)

        return Photo(**resp.json())

    def search_videos(self,
                      query: str,
                      orientation: str = '',
                      size: str = '',
                      color: str = '',
                      locale: str = '',
                      page: int = 1,
                      per_page: int = 15
                      ) -> VideosResponse:

        resp = self.__session.get(
            url=f"{self.__base_video_url}search",
            params={
                "query": query,
                "orientation": orientation,
                "size": size,
                "color": color,
                "locale": locale,
                "page": page,
                "per_page": per_page
            }
        )

        resp.raise_for_status()

        self.ratelimit.update(resp)

        return VideosResponse(**resp.json())

    def popular_videos(self,
                       min_width: int = None,
                       min_height: int = None,
                       min_duration: int = None,
                       max_duration: int = None,
                       page: int = 1,
                       per_page: int = 15
                       ) -> VideosResponse:
        resp = self.__session.get(
            url=f"{self.__base_video_url}popular",
            params={
                "min_width": min_width,
                "min_height": min_height,
                "min_duration": min_duration,
                "max_duration": max_duration,
                "page": page,
                "per_page": per_page
            }
        )

        resp.raise_for_status()

        self.ratelimit.update(resp)

        return VideosResponse(**resp.json())

    def get_video(self, id: int) -> Video:  # noqa
        resp = self.__session.get(url=f"{self.__base_video_url}videos/{id}")
        resp.raise_for_status()

        self.ratelimit.update(resp)

        return Video(**resp.json())

    def featured_collection(self, page: int = 1, per_page: int = 15) -> CollectionsResponse:
        resp = self.__session.get(f"{self.__base_url}collections/featured", params={"page": page, "per_page": per_page})
        resp.raise_for_status()

        self.ratelimit.update(resp)

        return CollectionsResponse(**resp.json())

    def my_collection(self, page: int = 1, per_page: int = 15) -> CollectionsResponse:
        resp = self.__session.get(f"{self.__base_url}collections", params={"page": page, "per_page": per_page})
        resp.raise_for_status()

        self.ratelimit.update(resp)

        return CollectionsResponse(**resp.json())

    def collection_media(self, id: str, # noqa
                         type: str = None, page: int = 1, per_page: int = 15) -> CollectionMedia:
        resp = self.__session.get(
            url=f"{self.__base_url}collections/{id}",
            params={
                "type": type,
                "page": page,
                "per_page": per_page
            }
        )

        resp.raise_for_status()

        self.ratelimit.update(resp)

        return CollectionMedia(**resp.json())

    def __setattr__(self, key, value):
        if key == 'ratelimit':
            # cant overwrite ratelimit parameter once assigned
            if 'ratelimit' not in self.__dict__:
                self.__dict__[key] = value
            return

        self.__dict__[key] = value


if __name__ == '__main__':
    pass




