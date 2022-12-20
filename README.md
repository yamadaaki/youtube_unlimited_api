# youtube_unlimited_api

```pip install youtube-unlimited-api```

```python
from youtube_unlimited_api import get_video_data

video = get_video_data('URL')

video.channel  # channel name
video.title  # video title
video.view_count  # view count
video.like_count  # like count
video.description  # video description
video.published_at  # published at
video.thumbnail  # video thumbnail url
video.channel_thumbnails  # channel thumbnails
video.id  # video id
video.related_videos  # related video list
```
