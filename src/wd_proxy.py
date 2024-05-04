import requests
from model import Group, Lecture, Teacher


class WdProxy:

    def __init__(self, wdauth: str, wd_url: str):
        self.WD_URL = wd_url
        self.wdauth = wdauth

    def get_lectures(self) -> list[Lecture]:
        url = f"{self.WD_URL}/lectures?active=true&wdauth={self.wdauth}"
        res = requests.get(url)
        lectures = res.json()
        nice_lectures = [Lecture(**lct) for lct in lectures]
        return nice_lectures

    def get_teachers(self) -> list[Teacher]:
        url = f"{self.WD_URL}/teachers?wdauth={self.wdauth}"
        res = requests.get(url)
        teachers = res.json()
        teachers = [Teacher(**t) for t in teachers]
        return teachers

    def get_groups(self) -> list[Group]:
        url = f"{self.WD_URL}/groups?active=True&wdauth={self.wdauth}"
        res = requests.get(url)
        groups = res.json()
        groups = [Group(**g) for g in groups]
        return groups


if __name__ == "__main__":
    wdauth = "da770ebd-d479-45d4-86de-9daaf2cfeae5"
    # https: //egzamin-api.wsi.edu.pl/authenticate

    wd = WdProxy(wdauth=wdauth, wd_url="https://wddata.wsi.edu.pl")
    tt = wd.get_teachers()
    for t in tt:
        print(t)
    gg = wd.get_lectures()
    for g in gg:
        print(g)
    ww = wd.get_lectures()
    for w in ww:
        print(ww)
