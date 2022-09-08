import re
import os
import argparse
import logging
from multiprocessing.pool import ThreadPool

import requests
from bs4 import BeautifulSoup

FILMOT_URL = "https://filmot.com/search/%(query)s/1/%(page)i?"
YT_VIDEO_URL = "https://www.youtube.com/watch?v="
URL_EXPR = re.compile(r"https:\/\/img\.youtube\.com\/vi\/(.+?)/[\d+].jpg")


def get_logger(level: str = "DEBUG") -> logging.Logger:
    """Get preconfigured logger

    :param level: logging level
    :type level: str

    :return: Logger instance
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s:%(funcName)s:%(lineno)s] %(message)s",
        "%d.%m.%Y %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger


logger = get_logger()


def get_args() -> argparse.Namespace:
    """Builds command line arguments and returns parse result.

    :return: arguments parse result
    """
    parser = argparse.ArgumentParser(
        description="Parse YouTube videos by subtitles using Python 3",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-q", "--query", type=str, required=True, help="Search query")
    parser.add_argument("-o", "--out", type=str, help="File to write results out")
    parser.add_argument(
        "-s",
        "--separator",
        type=str,
        default=",",
        help="Output items separator. Defaults to: %(default)s",
    )
    parser.add_argument(
        "-p",
        "--pages",
        type=int,
        default=1,
        help="Number of pages to process. Defaults to: %(default)s",
    )
    parser.add_argument(
        "-l",
        "--log",
        type=str,
        default="INFO",
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level. Defaults to: %(default)s",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="%(yt_url)s%(video_id)s",
        help="Output data format. Defaults to: %(default)s",
    )
    return parser.parse_args()


def build_url(query: str, page: int = 1) -> str:
    """Build query URL.

    :param query: search query
    :type query: str

    :return: formatted query URL
    """
    query = re.sub(r"\s+", "+", query)
    return FILMOT_URL % {"query": query, "page": page}


def format_separator(separator: str) -> str:
    """Format separator to support new line character.

    :param separator: separator to format
    :type separator: str

    :return: formatted separator
    """
    return separator.replace("\\r", "\r").replace("\\n", "\n")


def get_video_ids(bs: BeautifulSoup) -> list[str]:
    """Returns YT videos ids from the given page.

    :param bs: BeautifulSoup instance
    :type bs: BeautifulSoup

    :return: video ids
    """
    return [
        re.match(URL_EXPR, img["src"]).group(1)
        for img in bs.find_all("img", {"src": URL_EXPR})
    ]


def process_url(url: str) -> list[str]:
    """Get web page and parse its YT video ids.

    :param url: URL
    :type url: str

    :return: video ids
    """

    try:
        logger.debug("Requesting %s" % url)
        response = requests.get(url)
    except Exception as ex:
        logger.error(ex)
        return

    logger.debug("Parsing video ids (%s)" % url)
    bs = BeautifulSoup(response.content, "lxml")
    return get_video_ids(bs)


def format_output(video_id: str, str_format: str) -> str:
    """Converts video id to the specified output string format.

    :param video_id: video id
    :type video_id: str

    :param str_format: format to follow
    :type str_format: str

    :return: formatted string
    """
    return str_format % {
        "yt_url": YT_VIDEO_URL,
        "video_id": video_id,
    }


def main():
    args = get_args()
    logger.setLevel(args.log)

    with ThreadPool(args.pages) as pool:
        ids = pool.map(
            process_url,
            [build_url(args.query, page) for page in range(1, args.pages + 1)],
        )

    ids = [item for ids_sub in ids for item in ids_sub]
    formatted = [format_output(_id, args.format) for _id in ids]
    formatted_joined = format_separator(args.separator).join(formatted)

    if args.out:
        logger.debug("Results: %i" % len(ids))
        logger.debug(formatted_joined)
    else:
        logger.info("Results: %i" % len(ids))
        logger.info(formatted_joined)

    if args.out:
        filepath = os.path.abspath(args.out)
        logger.debug("Writing '%s' file" % filepath)
        try:
            with open(filepath, "w") as file:
                file.write(formatted_joined)
        except Exception as ex:
            logging.error(ex)


if __name__ == "__main__":
    main()
