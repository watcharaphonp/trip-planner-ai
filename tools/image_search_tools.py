from langchain.tools import tool

# from bing_image_urls import bing_image_urls
import requests
from bs4 import BeautifulSoup
import json
import random


class ImageSearchTools:
    @tool("Search the image from Bing Image Search")
    def search_image(query):
        """Useful to search image from Bing Image Search"""
        limit = 5
        search_url = f"https://www.bing.com/images/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract image URLs from the HTML response
        image_urls = []
        for anchor_iusc in soup.find_all("a", class_="iusc"):
            if anchor_iusc.get("m"):
                m_value = anchor_iusc.get("m")
                style_value = anchor_iusc.get("style")
                img_width = 0
                img_height = 0
                url: str = ""
                label: str = ""

                m_dict = json.loads(m_value)
                dimensions_list = style_value.split(";")
                url = m_dict.get("murl")

                # validate if the url can be accessed
                try:
                    response = requests.get(url, timeout=3)
                    if response.status_code != 200:
                        continue
                except requests.Timeout:
                    continue
                except requests.RequestException as e:
                    continue

                for dimension in dimensions_list:
                    key, value = dimension.split(":")
                    if key == "height":
                        img_height = int(value.replace("px", ""))
                    elif key == "width":
                        img_width = int(value.replace("px", ""))

                    label = m_dict.get("t")

                def check_banned(url):
                    url_ban_list = [
                        "wikimedia.org",
                        "imgur.com",
                        "example.com",
                        "via.placeholder.com",
                        "live.staticflickr.com",
                    ]

                    for item in url_ban_list:
                        if item in url:
                            return True
                        else:
                            return False

                if (
                    # check ban list
                    # not check_banned(url)
                    # check if the label contains the query
                    query in label
                    # validate url format
                    and url.startswith("https://")
                    # check image size
                    and img_width > 200
                    and img_height < img_width
                    # validate file type
                    and (".jpg" in url or ".jpeg" in url or ".png" in url)
                    and not url.endswith(".svg")
                ):
                    image_urls.append(url)
                    # break
                    # return url
                else:
                    continue

            if len(image_urls) >= limit:
                break

        if len(image_urls) == 0:
            return "Cannot find any image from Bing Image Search"

        # return image_urls[random.randint(0, len(image_urls) - 1)]
        return image_urls
