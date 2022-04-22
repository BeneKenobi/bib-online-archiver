import argparse
from urllib.parse import urlparse

import bibtexparser
import pdfkit
import requests


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file", help="source .bib-file")
    argparser.add_argument(
        "--outputfolder", nargs="?", help="target folder for .pdf-file(s)", default="./"
    )
    argparser.add_argument(
        "--alltypes",
        nargs="?",
        default=False,
        const=True,
        help='use all entrytypes, not only "Online"',
    )
    args = argparser.parse_args()
    with open(args.file) as bibtex_file:
        parser = bibtexparser.bparser.BibTexParser(
            common_strings=True, ignore_nonstandard_types=False
        )
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

        for entry in bib_database.entries:
            if (
                (entry["ENTRYTYPE"].lower() == "online") or (args.alltypes is True)
            ) and ("url" in entry):
                url = urlparse(entry["url"])._replace(fragment="").geturl()
                retrieve(url, f"{args.outputfolder}{entry['ID']}.pdf")


def retrieve(url, filename):
    proxy = requests.utils.select_proxy(url, requests.utils.get_environ_proxies(url))
    options = {
        "load-error-handling": "ignore",
        "no-stop-slow-scripts": "",
        "no-outline": "",
        "disable-external-links": "",
        "disable-internal-links": "",
        "javascript-delay": 6000,
    }
    if proxy is not None:
        options["proxy"] = proxy
    print(f"Will retrieve {url} as {filename}")
    try:
        pdfkit.from_url(url, filename, options=options)
    except OSError as error:
        print(f"Error while parsing: {error}")


main()
