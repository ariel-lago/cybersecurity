import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = input("Enter website URL: ")
os.makedirs("images", exist_ok=True)

response = requests.get(url, timeout=10)
print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

for i, img in enumerate(soup.find_all("img", src=True), 1):
    image_url = urljoin(url, img["src"])
    try:
        data = requests.get(image_url, timeout=10)
        data.raise_for_status()
        filename = f"images/image_{i}.jpg"
        with open(filename, "wb") as f:
            f.write(data.content)
        print("Saved:", filename)
    except Exception as e:
        print("Skipped:", image_url, e)
