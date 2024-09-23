"""Download music from YouTube."""

from sys import exit as close
from colorama import Fore, Back, Style
from subprocess import run
from ripbox_common import Request


def list_results(results):
    """List query results."""
    for result, n in zip(results, range(len(results))):
        rtype = result['type']
        title = result['title']
        length = result['length'] if 'length' in result else None
        print(Back.YELLOW if rtype == 'video' else Back.MAGENTA, end="")
        print(Fore.BLACK + Style.BRIGHT + f"{n + 1:<2}"
              + Style.RESET_ALL, end="")
        print(f" {title[:95] + '...' if len(title) > 95 else title}  "
              + (f"[{length}]" if length else ""))


def parse_cmd(cmd):
    """Interpret commands."""
    if cmd == "exit":
        close("Goodbye!")


def main():
    while True:
        query = "no woman no cry"
        # query = input("Search: ")
        request = Request(query)
        list_results(request.results)
        parse_cmd(input("\n> "))


if __name__ == '__main__':
    main()

# run(["yt-dlp", "-x", "--audio-format", "flac", yt_id], check=False)
