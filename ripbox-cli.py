"""Download music from YouTube."""

from sys import exit as close
from colorama import Style, Back
from progress.bar import Bar
from ripbox_common import RipboxRequest, RipboxQueue, download


HELP_MSG = (Style.BRIGHT + "Valid commands:\n" + Style.RESET_ALL
            + "\n  q<n>: add n. entry to queue\n"
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

downloaded, queued = set(), set()


def list_entries(entries):
    """List query results or the queue."""
    for result, n in zip(entries, range(len(entries))):

        title = result['title']
        length = result['length'] if 'length' in result else None

        if result['id'] in downloaded and result['id'] in queued:
            print(Back.MAGENTA + " " + Style.RESET_ALL, end="")
        elif result['id'] in downloaded:
            print(Back.BLUE + " " + Style.RESET_ALL, end="")
        elif result['id'] in queued:
            print(Back.GREEN + " " + Style.RESET_ALL, end="")
        else:
            print(" ", end="")

        if result['type'] == "video":
            print(Back.YELLOW + " " + Style.RESET_ALL, end=" ")
        elif result['type'] == "playlist":
            print(Back.CYAN + " " + Style.RESET_ALL, end=" ")
        else:
            print(" ", end=" ")

        print(f"{n + 1:<2}", end="")
        print(f" {title[:95] + '...' if len(title) > 95 else title}  "
              + (f"[{length}]" if length else ""))


def main():
    """CLI application for Ripbox."""
    request = None
    queue = RipboxQueue()
    open('session.log', 'w').close()

    print(Style.BRIGHT + "\nWelcome to Ripbox!\n" + Style.RESET_ALL
          + "\nType 'help' for available commands!")

    while True:

        # Enter search query
        if not request:
            try:
                query = "no woman no cry"
                # query = input(Style.BRIGHT + "\nSearch: " + Style.RESET_ALL)
                request = RipboxRequest(query)
            except ConnectionError as cerr:
                close(cerr)
            else:
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

            # Show help message
            if cmd == "help":
                print("\n" + HELP_MSG)

            # Close application
            elif cmd == "exit":
                close(Style.BRIGHT + "\nGoodbye!\n" + Style.RESET_ALL)

            # Download entries in the queue
            elif cmd == "dq":
                print("\nDownloading queue...\n")
                with Bar("  Progress:",
                         max=len(queue.serve())) as bar:
                    for entry in queue.serve():
                        if entry['id'] not in downloaded:
                            try:
                                download(entry['id'])
                                downloaded.add(entry['id'])
                            except ConnectionError:
                                continue
                            else:
                                queue.remove_entry(entry['id'])
                                queued.remove(entry['id'])
                                bar.next()
                        else:
                            queue.remove_entry(entry['id'])
                            queued.remove(entry['id'])
                            bar.next()
                            continue
                print(Style.BRIGHT + "\nDone." + Style.RESET_ALL)

            # List queue
            elif cmd == "lq":
                if len(queue.entries) != 0:
                    print(Style.BRIGHT + "\nQueue:\n" + Style.RESET_ALL)
                    list_entries(queue.serve())
                else:
                    print("\nQueue empty!")

            # Remove queue
            elif cmd == "rq":
                queue.clear()
                queued.clear()
                print("\nQueue removed.")

            # List results
            elif cmd == "lr":
                print(Style.BRIGHT + "\nResults:\n" + Style.RESET_ALL)
                list_entries(request.results)

            # New search query
            elif cmd == "ns":
                request = None

        # Add to queue / download / info
        elif c in ("q", "d", "i") and n:
            if 1 <= n <= len(request.results):
                entry = request.results[n - 1]

                # Add to queue
                if c == "q":
                    if entry['id'] not in queued:
                        queue.entries.append(entry)
                        queued.add(entry['id'])
                        print(f"\n{entry['title']} added to queue.")
                    else:
                        print("\nAlready in queue!")

                # Download entry
                elif c == "d":
                    if entry['id'] not in downloaded:
                        try:
                            print(f"\nDownloading {entry['title']}...")
                            download(entry['id'])
                            downloaded.add(entry['id'])
                            print("Done.")
                        except ConnectionError as cerr:
                            print(cerr)
                            continue
                    else:
                        print("\nAlready downloaded!")

                # Entry info
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

        # Remove from queue
        elif c == "r" and n:
            if 1 <= n <= len(queue.entries):
                entry = queue.entries[n - 1]
                queue.remove_entry(entry['id'])
                queued.remove(entry['id'])
                print(f"\n{entry['title']} removed from queue.")
            else:
                print(Style.BRIGHT + f"\nInvalid entry: {n}" + Style.RESET_ALL
                      + f"  Choose from 1-{len(queue.entries)}!")

        else:
            print(Style.BRIGHT + "\nUnknown command! " + Style.RESET_ALL
                  + HELP_MSG)


if __name__ == '__main__':
    main()
