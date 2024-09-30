"""Download music from YouTube."""

from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import URLError, HTTPError
from json import loads
from bs4 import BeautifulSoup
from subprocess import run, CalledProcessError


def download(entry_id):
    """Download an entry from query results or queue."""
    try:
        with open('session.log', 'a', encoding='utf-8') as log:
            run(["yt-dlp", "-x", "--audio-format", "flac", entry_id],
                check=True, stdout=log)
    except (URLError, HTTPError, CalledProcessError) as cerr:
        raise ConnectionError("Connection error!") from cerr


class RipboxRequest:
    """Manages search requests and downloads."""

    def __init__(self, query):
        self.query = query
        self.raw_results = self.get_results()
        self.results = self.create_list()

    def get_results(self):
        """Fetch results from YouTube."""

        url = ("https://www.youtube.com/results?search_query="
               + quote(self.query))
        try:
            with urlopen(url) as page:
                html = page.read().decode('utf-8')
                soup = BeautifulSoup(html, 'html.parser')
        except (URLError, HTTPError) as cerr:
            raise ConnectionError("Connection error!") from cerr
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
                          'channel': r['ownerText']['runs'][0]['text'],
                          'type': "video",
                          'downloaded': False, 'queued': False}
                if 'publishedTimeText' in r:
                    result['uploaded'] = r['publishedTimeText']['simpleText']
                else:
                    result['uploaded'] = None
                results.append(result)
            elif 'radioRenderer' in r:
                r = r['radioRenderer']
                result = {'id': r['playlistId'],
                          'title': r['title']['simpleText'],
                          'type': "playlist",
                          'downloaded': False, 'queued': False}
                results.append(result)

        return results


class RipboxQueue:
    """Manages a download queue."""

    def __init__(self):
        self.entries = []

    def remove(self):
        """Remove active queue."""

        self.entries = []

    def remove_entry(self, entry_id):
        """Remove an entry from the queue."""

        self.entries = [e for e in self.entries if e['id'] != entry_id]

    def serve(self):
        """Serve the queue after removing duplicates."""

        entries, ids = [], []
        for entry in self.entries:
            if entry['id'] not in ids:
                entries.append(entry)
                ids.append(entry['id'])
        return entries
