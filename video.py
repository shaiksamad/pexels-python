class User:
    def __init__(self,
                 id: int,  # noqa
                 name: str,
                 url: str):
        self.id = id
        self.name = name
        self.url = url


class VideoFile:
    def __init__(self,
                 id: int,  # noqa
                 quality: str,
                 file_type: str,
                 width: int,
                 height: int,
                 fps: float,
                 link: str):
        self.id = id
        self.quality = quality
        self.file_type = file_type
        self.width = width
        self.height = height
        self.fps = fps
        self.link = link


class VideoPicture:
    def __init__(self,
                 id: int,  # noqa
                 picture: str,
                 nr: int):
        self.id = id
        self.picture = picture
        self.nr = nr


class Video:
    def __init__(self,
                 id: int,  # noqa
                 width: int,
                 height: int,
                 url: str,
                 image: str,
                 duration: int,
                 user: User | dict,
                 video_files: list[VideoFile],
                 video_pictures: list[VideoPicture],
                 full_res: None = None,
                 tags: list = None,
                 avg_color: str | None = None,
                 type: str = "Video"
                 ):
        self.type = type
        self.id = id
        self.width = width
        self.height = height
        self.url = url
        self.full_res = full_res
        self.tags = tags
        self.avg_color = avg_color
        self.image = image
        self.duration = duration
        self.user = User(**user)
        self.video_files = []

        if isinstance(video_files, (list, dict)):
            for video_file in video_files:
                self.video_files.append(VideoFile(**video_file))  # noqa

        self.video_pictures = []

        if isinstance(video_pictures, (list, dict)):
            for video_picture in video_pictures:
                self.video_pictures.append(VideoPicture(**video_picture))  # noqa


class VideosResponse:
    def __init__(self,
                 total_results: int,
                 page: int,
                 per_page: int,
                 prev_page: str = "",
                 next_page: str = "",
                 videos: list[Video] | None = None,
                 url: str | None = None,
                 ):

        self.total_results = total_results
        self.page = page
        self.per_page = per_page
        self.next_page = next_page
        self.prev_page = prev_page

        self.videos = []
        if isinstance(videos, (list, dict)):
            for video in videos:
                self.videos.append(Video(**video))

        self.url = url

    def fetch_next_page(self, params: dict = None):
        pass


VideosResponse.fetch_next_page = lambda x: print(x)

