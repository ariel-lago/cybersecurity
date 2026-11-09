import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

def crawl(current_url, save_dir):
    response = requests.get(current_url, timeout=10)
    print(response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    for img in soup.find_all("img", src=True):
        image_url = urljoin(current_url, img["src"])
        path = urlparse(image_url).path

        if not path.lower().endswith(VALID_EXTENSIONS):
            continue

        img_name = os.path.basename(path)
        filename = os.path.join(save_dir, img_name)
        
        try:
            data = requests.get(image_url, timeout=10)
            data.raise_for_status()
            with open(filename, "wb") as f:
                f.write(data.content)
            print("Saved:", filename)
        except Exception as e:
            print("Skipped:", image_url, e)

def main():
    parser = argparse.ArgumentParser(usage="./spider [-rlp] URL")
    parser.add_argument("-r", action="store_true", help="recursive download")
    parser.add_argument("-l", type=int, default=5, help="max depth level")
    parser.add_argument("-p", type=str, default="./data/", help="save path")
    parser.add_argument("url", help="URL")

    if "-l" in sys.argv and "-r" not in sys.argv:
        print("error: -l requires -r")
        sys.exit(1)

    args = parser.parse_args()
    os.makedirs(args.p, exist_ok=True)

    crawl(args.url, args.p)

if __name__== "__main__":
    main()
