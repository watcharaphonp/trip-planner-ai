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
                style_attr = anchor_iusc.get("style")
                img_width = 1
                img_height = 0
                url: str = ""
                label: str = ""

                m_dict = json.loads(m_value)
                label = m_dict.get("t")
                url = m_dict.get("murl")

                if style_attr and "height" in style_attr and "width" in style_attr:
                    img_height = int(
                        style_attr.split(";")[0].split(":")[1].replace("px", "")
                    )
                    img_width = int(
                        style_attr.split(";")[1].split(":")[1].replace("px", "")
                    )

                if (
                    # check if the label contains the query
                    query in label
                    # validate url format
                    and url.startswith("https://")
                    # check image size
                    and img_height < img_width
                    # validate file type
                    and (".jpg" in url or ".jpeg" in url or ".png" in url)
                    and not url.endswith(".svg")
                ):
                    # validate if the url can be accessed
                    # try:
                    #     response = requests.get(url, timeout=5)
                    #     if response.status_code != 200:
                    #         continue
                    # except requests.Timeout:
                    #     continue
                    # except requests.RequestException as e:
                    #     continue

                    image_urls.append(url)
                else:
                    continue

            if len(image_urls) >= limit:
                break

        if len(image_urls) == 0:
            return "Cannot find any image from Bing Image Search"

        return image_urls
