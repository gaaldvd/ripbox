"""Download music from YouTube."""

from urllib.request import urlopen
from urllib.parse import quote
from json import loads
from bs4 import BeautifulSoup


class Request:
    """Manages search requests."""

    def __init__(self, query):
        self.query = query
        self.raw_results = self.get_results()
        self.results = self.create_list()

    def get_results(self):
        """Fetch results from YouTube."""

        url = ("https://www.youtube.com/results?search_query="
               + quote(self.query))
        with urlopen(url) as page:
            html = page.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
        script_tags = soup.find_all('script')
        json_data = script_tags[23].text[19:-1]
        data = loads(json_data)
        results = (data['contents']['twoColumnSearchResultsRenderer']
                       ['primaryContents']['sectionListRenderer']['contents']
                       [0]['itemSectionRenderer']['contents'])

        return results

    def create_list(self):
        """Create a list of dictionaries from the raw results."""

        results = []
        for r in self.raw_results:
            if 'videoRenderer' in r:
                r = r['videoRenderer']
                result = {'id': r['videoId'],
                          'title': r['title']['runs'][0]['text'],
                          'length': r['lengthText']['simpleText'],
                          'type': "video"}
                results.append(result)
            elif 'radioRenderer' in r:
                r = r['radioRenderer']
                result = {'id': r['playlistId'],
                          'title': r['title']['simpleText'],
                          'type': "playlist"}
                results.append(result)

        return results


class Queue:
    """Manages a download queue."""

    def __init__(self):
        pass
