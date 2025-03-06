from bs4 import BeautifulSoup
import requests

DESIRED_CARD_INFO = [
  "name",
  "grade",
  "skill",
  "icon",
  "power",
  "critical",
  "shield",
  "nation",
  "clan",
  "race",
  "card type",
  "trigger effect",
  "format",
  "text",
]

def get_soup(url):
  response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
  soup = BeautifulSoup(response.text, "html.parser")

  return soup


def get_hrefs(t_rows):
  hrefs = []

  for row in t_rows:
    # a_tag = row.find("a")
    a_tag = row.find("a", href=True)
    if a_tag:
      # print(a_tag["href"])
      hrefs.append(a_tag["href"])

  return hrefs
