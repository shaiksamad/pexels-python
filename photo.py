
class PhotoSrc:
    def __init__(self,
                 original: str,
                 large2x: str,
                 large: str,
                 medium: str,
                 small: str,
                 portrait: str,
                 landscape: str,
                 tiny: str
                 ):
        self.original = original
        self.large2x = large2x
        self.large = large
        self.medium = medium
        self.small = small
        self.portrait = portrait
        self.landscape = landscape
        self.tiny = tiny


class Photo:
    def __init__(self,
                 id: int,
                 width: int,
                 height: int,
                 url: str,
                 photographer: str,
                 photographer_url: str,
                 photographer_id: int,
                 avg_color: str,
                 src: PhotoSrc | dict,
                 liked: bool,
                 alt: str,
                 type: str = "Photo"
                 ):
        self.type = type
        self.id: int = id
        self.width = width
        self.height = height
        self.url = url
        self.photographer = photographer
        self.photographer_url = photographer_url
        self.photographer_id = photographer_id
        self.avg_color = avg_color

        if isinstance(src, dict):
            src = PhotoSrc(**src)
        self.src = src
        self.liked = liked
        self.alt = alt


class PhotosResponse:
    def __init__(self,
                 total_results: int,
                 page: int,
                 per_page: int,
                 photos: list[Photo],
                 prev_page: str = "",
                 next_page: str = "",
                 **kwargs
                 ):
        self.total_results = total_results
        self.page = page
        self.per_page = per_page
        self.next_page = next_page
        self.prev_page = prev_page

        self.photos = []

        if isinstance(photos, (list, dict)):
            for photo in photos:
                self.photos.append(Photo(**photo))  # noqa

        # for navigation
        self.fetch_next_page = None
        self.fetch_prev_page = None

        self._create_nav = kwargs.get('create_nav', None)

        if self._create_nav:
            if next_page:
                self.fetch_next_page = self._create_nav(next_page)
            if prev_page:
                self.fetch_prev_page = self._create_nav(prev_page)
