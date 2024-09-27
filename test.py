"""Download music from YouTube."""

from sys import exit as close
from colorama import Style
from ripbox_common import Request, Queue


HELP_MSG = (Style.BRIGHT + "Valid commands:\n" + Style.RESET_ALL
            + "  q<n>: add n. entry to queue\n"
            "  r<n>: remove n. entry from queue\n"
            "  d<n>: download n. entry\n"
            "  i<n>: entry info\n"
            "  lq: list queue\n"
            "  dq: download queue\n"
            "  rq: remove queue\n"
            "  lr: list results\n"
            "  ns: new search\n"
            "  exit: close application\n"
            "  help: show this help message")

COMMANDS = ("help", "exit", "dq", "lq", "rq", "lr", "ns", "d", "q", "i", "r")


def list_entries(entries):
    """List query results or queue."""
    for result, n in zip(entries, range(len(entries))):
        # TODO check if marked as downloaded/in queue
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
    queue = Queue()

    while True:

        # Enter search query
        if not request:
            query = "no woman no cry"
            # query = input(Style.BRIGHT + "\nSearch: " + Style.RESET_ALL)
            try:
                request = Request(query)
            except ConnectionError as cerr:
                close(cerr)
            print(Style.BRIGHT + "\nResults:\n" + Style.RESET_ALL)
            list_entries(request.results)

        # Enter command
        cmd = input("\n> ")

        # Parse q/d/i command
        if len(cmd) > 1 and cmd[0] in COMMANDS:
            c = cmd[0]
            n = int(cmd[1:]) if cmd[1:].isnumeric() else None
        else:
            c, n = None, None

        # Interpret commands
        if cmd in COMMANDS:
            if cmd == "help":
                # Show help message
                print("\n" + HELP_MSG)
            elif cmd == "exit":
                # Close application
                close(Style.BRIGHT + "\nGoodbye!\n" + Style.RESET_ALL)
            elif cmd == "dq":
                # Download entries in the queue
                print("\nDownload queue...")
                queue.download()
                print("Done.")
            elif cmd == "lq":
                # List queue
                if len(queue.entries) != 0:
                    print(Style.BRIGHT + "\nQueue:\n" + Style.RESET_ALL)
                    list_entries(queue.entries)
                else:
                    print("\nQueue empty!")
            elif cmd == "rq":
                # Remove queue
                queue.remove()
                print("\nQueue removed.")
            elif cmd == "lr":
                # List results
                print(Style.BRIGHT + "\nResults:\n" + Style.RESET_ALL)
                list_entries(request.results)
            elif cmd == "ns":
                # New search query
                request = None
        elif c in ("q", "d", "i") and n:
            # Add to queue / download / info
            if 1 <= n <= len(request.results):
                entry = request.results[n - 1]
                if c == "q":
                    queue.entries.append(entry)
                    # Mark as queued in results
                    for r in request.results:
                        if r['id'] == entry['id']:
                            r['queued'] = True
                    print(f"\n{entry['title']} added to queue.")
                elif c == "d":
                    try:
                        print(f"\nDownloading {entry['title']}...")
                        request.download_entry(entry['id'])
                        # Mark as downloaded in queue
                        for e in queue.entries:
                            if e['id'] == entry['id']:
                                e['downloaded'] = True
                        print("Done.")
                    except ConnectionError as cerr:
                        print(cerr)
                        continue
                elif c == "i":
                    if entry['type'] == "video":
                        print(f"\nTitle:    {entry['title']}\n"
                              f"Length:   {entry['length']}\n"
                              f"Channel:  {entry['channel']}")
                        if 'uploaded' in entry:
                            print(f"Uploaded: {entry['uploaded']}")
                    else:
                        print(f"\nPlaylist title: {entry['title']}")
            else:
                print(Style.BRIGHT + f"\nInvalid entry: {n}" + Style.RESET_ALL
                      + f"  Choose from 1-{len(request.results)}!")
        elif c == "r" and n:
            # Remove from queue
            if 1 <= n <= len(queue.entries):
                entry = queue.entries[n - 1]
                queue.remove_entry(entry['id'])
                print(f"\n{entry['title']} removed from queue.")
            else:
                print(Style.BRIGHT + f"\nInvalid entry: {n}" + Style.RESET_ALL
                      + f"  Choose from 1-{len(queue.entries)}!")
        else:
            print(Style.BRIGHT + "\nUnknown command! " + Style.RESET_ALL
                  + HELP_MSG)


if __name__ == '__main__':
    main()
