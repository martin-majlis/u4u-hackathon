import logging
import shutil
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import requests
from bs4 import BeautifulSoup

from lindat_translation_master.app.text_utils import split_text_into_sentences

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

SLEEP = 1

DIR_DATA = Path("data")
INPUT_FILE = DIR_DATA / "pages-cs-and-ua.txt"
DIR_DOWNLOAD = DIR_DATA / "ukrainer-download"
DIR_PROCESSED = DIR_DATA / "ukrainer-processed"


@dataclass
class ExtractInfo:
    element: Any
    href: str
    active: bool


def extract_info(el: Any) -> Optional[ExtractInfo]:
    if not el:
        return None
    element = el.find_parents("a", limit=1)
    return ExtractInfo(
        element=element, active=bool(element[0]["class"]), href=element[0]["href"]
    )


CS2UA: Dict[Path, Path] = defaultdict(Path)
UA2CS: Dict[Path, Path] = defaultdict(Path)


def combine_url(path: Path, href: str) -> str:
    if href.startswith("https://"):
        return href
    if "index.html" in str(path):
        path = path.parent
    for p in href.split("/"):
        if p == "..":
            path = path.parent
        else:
            path /= p
    url = str(path).replace(str(DIR_DATA), "https:/")
    if url.endswith("index.html"):
        url = url.replace("index.html", "")
    return url


def url_to_path(u: str) -> str:
    return u.replace("/", "-")


def download_page(url: str, path: Path):
    logger.info(f"Downloading {url} into {path}")
    r = requests.get(url, allow_redirects=True)
    open(path, "wb").write(r.content)
    time.sleep(SLEEP)


def download_pages(
    original_file: Path, cs_info: ExtractInfo, ua_info: ExtractInfo
) -> Tuple[Path, Path]:
    cs_url = combine_url(original_file, cs_info.href)
    ua_url = combine_url(original_file, ua_info.href)

    cs_path = DIR_DOWNLOAD / url_to_path(cs_url)
    ua_path = DIR_DOWNLOAD / url_to_path(ua_url)

    if not cs_path.exists():
        download_page(cs_url, cs_path)
    if not ua_path.exists():
        download_page(ua_url, ua_path)

    return cs_path, ua_path


def splitter_lang(lang: str) -> str:
    if lang == "ua":
        return "uk"
    return lang


def extract_file(html_file: Path, output_path: Path, lang: str) -> bool:
    logger.info(f"Processing {html_file} for language {lang} into {output_path}")
    output_path.mkdir(parents=True, exist_ok=True)
    output_txt_file = output_path / f"{lang}.txt"
    output_sententences_file = output_path / f"{lang}_sentences.txt"
    output_original_file = output_path / f"{lang}_orig.html"
    if output_txt_file.exists():
        logger.warning(f"{html_file} - skipped, already processed - {output_txt_file}")
        return False

    with open(html_file) as fh_file:
        soup = BeautifulSoup(fh_file.read(), "html.parser")
        texts = []

        for txt_section in soup.find_all("div", class_="text-section"):
            for ps in txt_section.find_all("p"):
                for p in ps.contents:
                    texts.append(str(p))

        with output_txt_file.open(mode="w") as fh_txt_out:
            fh_txt_out.write("\n".join(texts))

        with output_sententences_file.open(mode="w") as fh_sent_out:
            for txt in texts:
                sentences = split_text_into_sentences(txt, splitter_lang(lang))
                fh_sent_out.write("\n".join(sentences))

        shutil.copy(html_file, output_original_file)

        log_file = output_path / "_log.txt"
        with log_file.open(mode="w") as fh_log:
            fh_log.write(
                f"{datetime.utcnow().isoformat()}\t{lang}\t"
                f"{html_file}\t{output_txt_file}"
            )

    return True


def process_file(file: Path) -> bool:
    logger.info(f"{file} - processing")
    if file.is_dir():
        file /= "index.html"
    if not file.exists():
        logger.error(f"{file} does not exist!")
        return False

    with open(file) as fh_file:
        soup = BeautifulSoup(fh_file.read(), "html.parser")

        cs_info = extract_info(soup.find(string="(CS) Čeština"))
        if not cs_info:
            logger.warning(f"{file} - skipped, missing CS")
            return False

        ua_info = extract_info(soup.find(string="(UA) Українська"))
        if not ua_info:
            logger.warning(f"{file} - skipped, missing UA")
            return False

        cs_html_path, ua_html_path = download_pages(file, cs_info, ua_info)
        CS2UA[cs_html_path] = ua_html_path
        UA2CS[ua_html_path] = cs_html_path

        output_dir = DIR_PROCESSED / cs_html_path.name
        cs_processed = extract_file(cs_html_path, output_dir, "cs")
        ua_processed = extract_file(ua_html_path, output_dir, "ua")

        return cs_processed or ua_processed


def main() -> None:
    logger.info(f"Using output dir {DIR_PROCESSED}")
    DIR_PROCESSED.mkdir(parents=True, exist_ok=True)
    DIR_DOWNLOAD.mkdir(parents=True, exist_ok=True)

    logger.info(f"Processing input file - {INPUT_FILE}")
    with open(INPUT_FILE) as fh:
        for line in fh:
            parts = line.split()
            if len(parts) > 1:
                process_file(DIR_DATA / parts[1])
            else:
                logger.warning(f"Skipping line {line}")


if __name__ == "__main__":
    main()
