import requests
from bs4 import BeautifulSoup
import re
import time
import random
import csv
import pandas as pd

# hard coded, found from website tennisradar.gr
postal_codes = [
    10434, 10441, 10443, 10447, 10558, 10676, 11141, 11475, 11476, 11525,
    11528, 11853, 11855, 12043, 12135, 12243, 12351, 12461, 12462, 13121,
    13232, 13561, 13562, 14231, 14233, 14262, 14342, 15001, 15123, 15125,
    15126, 15127, 15231, 15234, 15236, 15237, 15238, 15341, 15342, 15343,
    15344, 15349, 15351, 15354, 15451, 15452, 15562, 15669, 15771, 15772,
    15773, 15780, 16122, 16232, 16233, 16341, 16342, 16344, 16346, 16451,
    16452, 16671, 16672, 16673, 16674, 16675, 16701, 16777, 17122, 17124,
    17341, 17455, 17456, 17561, 17562, 17676, 17778, 18233, 18344, 18454,
    18533, 18534, 18537, 18538, 18541, 18758, 19002, 19400
]


def extract_coords(url) -> tuple | None:
    """

    :param url: tennisradar url
    :return: returns coordinates of tennis field, or None in case the link doesnt work.
    """
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    iframe = soup.find("iframe")
    if not iframe:
        return None

    src = iframe.get("src", "")

    # Look for "?q=LAT,LON"
    match = re.search(r"q=([-0-9.]+),([-0-9.]+)", src)
    if match:
        lat = float(match.group(1))
        lon = float(match.group(2))
        return lat, lon
    time.sleep(random.choice([0.5, 1]))
    return None


def extract_title(url) -> str | None:
    """

    :param url: url of tennis radar.gr
    :return: title (location) of tennis field
    """
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    h1 = soup.find("h1", class_="entry-title")
    if h1:
        title = h1.get_text(strip=True)
        return title

    # Random sleep to mimic human behavior
    time.sleep(random.choice([0.5, 1]))
    return None

df = pd.DataFrame(columns=["postal_code", "area", "latitude", "longitude"])
max = 2000 # dont really need it
c = 0
for tk in postal_codes:
    for court in range(1, max):
        coords = extract_coords(f"https://tennisradar.gr/blog/gipedo-athina-{tk}-{court}/")
        area = extract_title(f"https://tennisradar.gr/blog/gipedo-athina-{tk}-{court}/")
        if coords is None:
            break
        df = pd.concat([df, pd.DataFrame([{"postal_code": tk, "area":area, "latitude": coords[0], "longitude": coords[1]}])], ignore_index=True)
        print(c, tk, area, coords)
        c += 1
df.to_csv('areas_coords_and_tk.csv')