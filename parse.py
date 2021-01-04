from bs4 import BeautifulSoup
from collections import defaultdict

def parse(soup):
    entries = []
    for entry in soup.find_all('tr', attrs={"class":"disk"}):
        e = {}
        e["price-per-gb"], e["price-per-tb"], e["price"], e["capacity"], e["warranty"], e["form-factor"], e["technology"], e["condition"], name = entry.find_all("td")
        e = {key: value.text for key, value in e.items()}
        e["name"] = name.text
        e["link"] = name.find("a")["href"]
        for attr, val in entry.attrs.items():
            if attr.startswith("data-"):
                e[attr.removeprefix("data-")] = val
        entries.append(e)
    return entries

from functools import total_ordering

@total_ordering
class Capacity():
    def __init__(self, s):
        self.text = s
        self.unit_cap = s.split(" x")[0]
        count, unit = self.unit_cap.split(" ")
        assert unit in ("MB", "GB", "TB")
        count = float(count)
        self.size = count * {"MB": 1, "GB": 1000, "TB": 1000000}[unit]
    def __hash__(self):
        return hash(self.unit_cap) # Same unit cap, equal--ignore counts
    def __lt__(self, other):
        return self.size < other.size
    def __eq__(self, other):
        return self.size == other.size
    def __str__(self):
        return str(self.text)

def class_for(entry):
    if e["condition"] == "used":
        return None
    return e["technology"], Capacity(e["capacity"])

if __name__ == '__main__':
    with open("index.html") as f:
        html_text = f.read()
    soup = BeautifulSoup(html_text, 'html.parser')
    entries = parse(soup)
    classes = defaultdict(list)
    for e in entries:
        c = class_for(e)
        if c is None:
            continue
        classes[c].append(e)
    for c in sorted(classes.keys()):
        e = classes[c][0]
        if len(classes[c]) > 5:
            print(c[0], c[1], e["price"], e["price-per-tb"], e["form-factor"], e["link"])
