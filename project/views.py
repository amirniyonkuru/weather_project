from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup


def get_content(area):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.9"
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    session.headers["Accept-Language"] = LANGUAGE
    session.headers["Content-Language"] = LANGUAGE
    content_html = session.get(f"https://www.google.com/search?q=weather+{area}").text

    return content_html


def home(request):

    if request.method == "GET":
        area = request.GET.get("area")
        content_html = get_content(area)
        soup = BeautifulSoup(content_html, "html.parser")

        weather = {}
        weather["region"] = soup.find("div", attrs={"id": "wob_loc"}).text
        weather["datetime"] = soup.find("div", attrs={"id": "wob_dts"}).text
        weather["status"] = soup.find("span", attrs={"id": "wob_dc"}).text
        weather["temp"] = soup.find("span", attrs={"id": "wob_tm"}).text
    else:
        weather = None

    context = {"weather": weather}
    return render(request, "project/index.html", context)
