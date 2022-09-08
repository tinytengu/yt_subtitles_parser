# yt_subtitles_parser

Parse YouTube videos by subtitles using Python 3.
> Script uses [filmot.com](https://filmot.com) service under the hood because the last thing I want is to gather subtitles from all videos on YT.

> I only use the latest versions of Python to have access to the latest and coolest features, so Poetry requires one to use Python ^3.10, although I'm pretty sure this script may work on earlier versions, figure it out by yourself.

![Version 0.1](https://img.shields.io/badge/version-0.1-informational) ![Python 3.10](https://img.shields.io/badge/python-3.10-blue) ![Poetry 1.2.0](https://img.shields.io/badge/poetry-1.2.0-informational)

## Installation:
### Poetry:
```sh
poetry install
```
### Pip:
```sh
pip3 install -r requirements.txt
```

## Usage:
```sh
python3 parser.py --help

usage: parser.py [-h] -q QUERY [-o OUT] [-s SEPARATOR] [-p PAGES] [-l {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                 [-f FORMAT]

Parse YouTube videos by subtitles using Python 3

options:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        Search query
  -o OUT, --out OUT     File to write results out
  -s SEPARATOR, --separator SEPARATOR
                        Output items separator. Defaults to: ,
  -p PAGES, --pages PAGES
                        Number of pages to process. Defaults to: 1
  -l {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Logging level. Defaults to: INFO
  -f FORMAT, --format FORMAT
                        Output data format. Defaults to: %(yt_url)s%(video_id)s
```

## License
[GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html)
