"""Download music from YouTube."""

from sys import exit as close
from colorama import Style
from ripbox_common import Request


HELP_MSG = (Style.BRIGHT + "Valid commands:\n" + Style.RESET_ALL
            + "  q<n>: add n. entry to queue\n"
            "  d<n>: download n. entry\n"
            "  i<n>: entry info\n"
            "  lq: list queue\n"
            "  dq: download queue\n"
            "  lr: list results\n"
            "  ns: new search\n"
            "  exit: close application\n"
            "  help: show this help message")


def list_results(results):
    """List query results."""
    print("\nResults:\n")
    for result, n in zip(results, range(len(results))):
        # rtype = result['type']
        title = result['title']
        length = result['length'] if 'length' in result else None
        # print(Style.NORMAL if rtype == 'video' else Style.BRIGHT, end="")
        print(f"{n + 1:<2}", end="")
        print(f" {title[:95] + '...' if len(title) > 95 else title}  "
              + (f"[{length}]" if length else ""))


def main():
    """CLI application for Ripbox."""
    request = None
    while True:

        # Enter search query
        if not request:
            query = "no woman no cry"
            # query = input(Style.BRIGHT + "\nSearch: " + Style.RESET_ALL)
            request = Request(query)
            list_results(request.results)

        # Enter command
        cmd = input("\n> ")

        # Parse q/d/i command
        if cmd[0] in ("q", "d", "i") and len(cmd) > 1:
            c, n = cmd[0], cmd[1:]
        else:
            c, n = None, None

        # Interpret commands
        if cmd == "help":
            # Show help message
            print("\n" + HELP_MSG)
        elif cmd == "exit":
            # Close application
            close(Style.BRIGHT + "\nGoodbye!\n" + Style.RESET_ALL)
        elif cmd == "dq":
            # Download entries in the queue
            print("\nDownload queue...")  # TODO download queue
        elif cmd == "lq":
            # List queue
            print("\nList queue...")  # TODO list queue
        elif cmd == "lr":
            # List results
            list_results(request.results)
        elif cmd == "ns":
            # New search query
            request = None
        elif c in ("q", "d", "i") and n.isnumeric():
            # Add to queue / download / info
            n = int(n)
            if n < 1 or n > len(request.results):
                print(Style.BRIGHT + f"\nInvalid entry: {n}" + Style.RESET_ALL
                      + f"  Choose from 1-{len(request.results)}!")
            else:
                print(f"{c} {n}")  # TODO add to queue/download/info
        else:
            print(Style.BRIGHT + "\nUnknown command! " + Style.RESET_ALL
                  + HELP_MSG)


if __name__ == '__main__':
    main()

# run(["yt-dlp", "-x", "--audio-format", "flac", yt_id], check=False)
