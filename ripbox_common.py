"""Ripbox shared library.

This module contains the classes and functions used by the Ripbox
applications (both CLI and GUI).

Functions:

    download(entry_id)
        Download an entry from the query results or the queue.

Classes:

    RipboxRequest
        Manages search requests and results.
    RipboxQueue
        Manages a download queue.
"""

from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import URLError, HTTPError
from json import loads
from subprocess import run, CalledProcessError
from bs4 import BeautifulSoup


def download(entry_id):
    """Download an entry from the query results or the queue.

    Parameters
    ----------
    entry_id : str
        The 'id' value of the entry.

    Raises
    ------
    ConnectionError
        If there's a problem with the connection or subprocess.run()
        returns a value other than 0.
    """
    try:
        with open('session.log', 'a', encoding='utf-8') as log:
            run(["yt-dlp", "-x", "--audio-format", "flac", "-P", "download" entry_id],
                check=True, stdout=log)
    except (URLError, HTTPError, CalledProcessError) as cerr:
        raise ConnectionError("Connection error!") from cerr


class RipboxRequest:
    """Manages search requests and results.
    Usage: request = RipboxRequest(query)

    Attributes
    ----------
    query : str
        The search query provided by the user.
    results : list
        Contains the search results in a list of dictionaries.
    """

    def __init__(self, query):
        """
        Parameters
        ----------
        query : str
            The search query provided by the user.
        """
        self.query = query
        self.raw_results = self.get_results()
        self.results = self.create_list()

    def get_results(self):
        """Fetch results from YouTube.
        Scrapes the search results page, extracts results in JSON format
        and returns them as a raw list of dictionaries.

        Raises
        ------
        ConnectionError
            If there is a connection error while scraping the site.
        Returns
        -------
        results : list
            The raw list of results as a list of dictionaries.
        """

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
        """Create a list of standardized dictionaries from the raw results.

        Returns
        -------
        results : list
            The list of results as a list of standardized dictionaries.
        """

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
    """Manages a download queue.
    Usage: queue = RipboxQueue()

    Attributes
    ----------
    entries : list
        Queue entries as a list of standardized dictionaries.

    Methods
    -------
    clear
        Clears the queue.
    remove_entry(entry_id)
        Removes an entry from the queue.
    serve
        Serves the queue after removing duplicates.
    """

    def __init__(self):
        self.entries = []

    def clear(self):
        """Clear active queue."""

        self.entries = []

    def remove_entry(self, entry_id):
        """Remove an entry from the queue.

        Parameters
        ----------
        entry_id : str
            The 'id' value of the entry.
        """

        self.entries = [e for e in self.entries if e['id'] != entry_id]

    def serve(self):
        """Serve the queue after removing duplicates.
        Use this method for listing or downloading queue entries.

        Returns
        -------
        entries : list
            The list of results as a list of standardized dictionaries.
        """

        entries, ids = [], []
        for entry in self.entries:
            if entry['id'] not in ids:
                entries.append(entry)
                ids.append(entry['id'])
        return entries
