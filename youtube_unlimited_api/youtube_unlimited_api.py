import datetime
import json
import re
from typing import Dict, List

import requests


class Video:
    def __init__(self, video_data: Dict) -> None:
        self.id: str = video_data['currentVideoEndpoint']['watchEndpoint']['videoId']
        self.title: str = video_data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']['title']['runs'][0]['text']
        self.channel: str = video_data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']['title']['runs'][0]['text']
        self.description: str = video_data['engagementPanels'][1]['engagementPanelSectionListRenderer']['content']['structuredDescriptionContentRenderer']['items'][1]['expandableVideoDescriptionBodyRenderer']['descriptionBodyText']['runs'][0]['text']
        self.channel_thumbnails: List[Dict] = video_data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']['thumbnail']['thumbnails']
        self.thumbnail: str = f'https://img.youtube.com/vi/{self.id}/0.jpg'
        self.view_count: int = int(video_data['engagementPanels'][1]['engagementPanelSectionListRenderer']['content']['structuredDescriptionContentRenderer']['items'][0]['videoDescriptionHeaderRenderer']['factoid'][1]['factoidRenderer']['value']['simpleText'].replace(',', ''))
        self.like_count = int(video_data['engagementPanels'][1]['engagementPanelSectionListRenderer']['content']['structuredDescriptionContentRenderer']['items'][0]['videoDescriptionHeaderRenderer']['factoid'][0]['factoidRenderer']['value']['simpleText'].replace(',', ''))

        published_at = video_data['engagementPanels'][1]['engagementPanelSectionListRenderer']['content']['structuredDescriptionContentRenderer']['items'][0]['videoDescriptionHeaderRenderer']['factoid'][2]['factoidRenderer']['accessibilityText']
        related_video_list = video_data['contents']['twoColumnWatchNextResults']['secondaryResults']['secondaryResults']['results']

        year, month, day = published_at.split('/')
        self.published_at: datetime.datetime = datetime.datetime(int(year), int(month), int(day))

        self.related_videos: List[RelatedVideo] = []

        for related_video in related_video_list:
            try:
                self.related_videos.append(RelatedVideo(related_video))
            except KeyError:
                pass

    def __repr__(self) -> str:
        return f'<Video {self.id}>'


class RelatedVideo:
    def __init__(self, video_data: Dict) -> None:
        self.id: str = video_data['compactVideoRenderer']['videoId']
        self.title: str = video_data['compactVideoRenderer']['title']['simpleText']
        self.channel: str = video_data['compactVideoRenderer']['longBylineText']['runs'][0]['text']
        self.thumbnail: str = f'https://img.youtube.com/vi/{self.id}/0.jpg'
        self.view_count: int = int(video_data['compactVideoRenderer']['viewCountText']['simpleText'].split()[0].replace(',', ''))
        length = video_data['compactVideoRenderer']['lengthText']['simpleText']

        if len(length.split(':')) == 3:
            h, m, s = length.split(':')
            self.length: int = int(h) * 3600 + int(m) * 60 + int(s)
        else:
            m, s = length.split(':')
            self.length: int = int(m) * 60 + int(s)

    def __repr__(self) -> str:
        return f'<RelatedVideo {self.id}>'


def get_video_data(url: str) -> Video:
    res = requests.get(url).text
    json_data = re.findall(r'ytInitialData = ({.+});</script>', res)[0]
    video_data = json.loads(json_data)
    return Video(video_data)
