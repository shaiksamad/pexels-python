from photo import Photo
from video import Video


class Collection:
    def __init__(self,
                 id: str,  # noqa
                 title: str,
                 description: str,
                 private: bool,
                 media_count: int,
                 photos_count: int,
                 videos_count: int
                 ):
        self.id = id
        self.title = title
        self.description = description
        self.private = private
        self.media_count = media_count
        self.photos_count = photos_count
        self.videos_count = videos_count


class CollectionsResponse:
    def __init__(self,
                 total_results: int,
                 page: int,
                 per_page: int,
                 collections: list[Collection] = None,
                 prev_page: str = "",
                 next_page: str = "",
                 ):
        self.total_results = total_results
        self.page = page
        self.per_page = per_page
        self.next_page = next_page
        self.prev_page = prev_page

        self.collections = []
        if isinstance(collections, (list, dict)):
            for collection in collections:
                self.collections.append(Collection(**collection))  # noqa


class CollectionMedia(CollectionsResponse):
    def __init__(self,
                 id: str,  # noqa
                 total_results: int,
                 page: int,
                 per_page: int,
                 media: list[Video] | list[Photo],
                 prev_page: str = "",
                 next_page: str = "",
                 ):
        super().__init__(total_results, page, per_page, prev_page=prev_page, next_page=next_page)

        self.id = id
        self.media = []

        if isinstance(media, (list, dict)):
            for item in media:
                if item['type'] == "Photo":
                    self.media.append(Photo(**item))
                else:
                    self.media.append(Video(**item))
