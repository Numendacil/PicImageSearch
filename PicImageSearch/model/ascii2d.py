from typing import Dict, List

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


class Ascii2DItem:
    def __init__(self, data: PyQuery):
        self.origin: PyQuery = data  # 原始数据
        info = self._get_info(data("div.detail-box.gray-link"))
        # 原图长宽，类型，大小
        self.hash: str = data("div.hash").eq(0).text()
        self.detail: str = data("small").eq(0).text()
        self.thumbnail: str = "https://ascii2d.net" + data("img").eq(0).attr("src")
        self.url: str = info["url"]
        self.title: str = info["title"]
        self.author: str = info["author"]
        self.author_url: str = info["author_url"]
        self.mark: str = info["mark"]

    @staticmethod
    def _get_info(data: PyQuery) -> Dict[str, str]:
        info = {
            "url": "",
            "title": "",
            "author_url": "",
            "author": "",
            "mark": "",
        }

        infos = data.find("h6")
        if infos:
            links = infos.find("a")
            if links:
                info["url"] = links.eq(0).attr("href")
                info["mark"] = infos("small").eq(0).text()
                if len(list(links.items())) > 1:
                    info["title"] = links.eq(0).text()
                    info["author_url"] = links.eq(1).attr("href")
                    info["author"] = links.eq(1).text()
                elif links.eq(0).parents("small"):
                    info["title"] = infos.contents().eq(0).text()

        infos = data.find(".external")
        if infos:
            if info["url"] == "":
                links = infos.find("a")
                if links:
                    info["url"] = links.eq(0).attr("href")
                    infos.remove("a")
            if info["title"] == "":
                info["title"] = infos.eq(0).text()

        return info


class Ascii2DResponse:
    def __init__(self, resp_text: str, resp_url: str):
        self.origin: str = resp_text  # 原始数据
        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(self.origin, parser=utf8_parser))
        # 结果返回值
        self.raw: List[Ascii2DItem] = [
            Ascii2DItem(i) for i in data.find("div.row.item-box").items()
        ]
        self.url: str = resp_url
