"""Download music from YouTube."""

from urllib.request import urlopen
from urllib.parse import quote
from json import loads
from bs4 import BeautifulSoup


def get_results(query=None):
    """Fetch results from YouTube."""

    url = "https://www.youtube.com/results?search_query=" + quote(query)

    with urlopen(url) as page:
        html = page.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
    script_tags = soup.find_all('script')
    json_data = script_tags[23].text[19:-1]
    data = loads(json_data)

    results_raw = (data['contents']['twoColumnSearchResultsRenderer']
                   ['primaryContents']['sectionListRenderer']['contents'][0]
                   ['itemSectionRenderer']['contents'])

    results = []
    for r in results_raw:
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
