# Ripbox

**A simple Python application to download music from YT.**

The application is developed and maintained on [Arch Linux](https://archlinux.org/).

## Requirements

The following packages have to be installed from the package manager:

- [git](https://git-scm.com/downloads)
- [Python 3+](https://www.python.org/downloads/)
- [pipenv](https://pipenv.pypa.io/en/latest/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Setting up

1. Open a console somewhere in your home folder (e.g. ~/src) and clone the git repository:

    `git clone https://github.com/gaaldvd/ripbox.git`

3. cd to the downloaded folder: `cd ripbox`
4. Run the setup script: `sh setup.sh`

## Usage

Start the application from the ripbox directory:

CLI version: `./start -c`
GUI version (not yet implemented): `./start -g`

### CLI

### GUI

*Under development.*

## Updating

The update.sh file prompts the user, then updates the git repository and the Python packages: `./update.sh`

## Reporting errors

Any error can be reported through [e-mail](mailto:gaaldavid[at]tuta.io?subject=[GitHub]%20ripbox%20error) with the exact error message or console screenshot. Please attach the `session.log` file from the ripbox directory.
