import re

from scrap_funcs import get_soup, get_hrefs, DESIRED_CARD_INFO

base_url = "https://cardfight.fandom.com"  # Will append with card anchor links
url = "https://cardfight.fandom.com/wiki/D_Start_Deck_01:_Yu-yu_Kondo_-Holy_Dragon-"

soup = get_soup(url) # Request the page

# Find the table with class "card-list"
table = soup.find_all("table", class_="sortable")
t_rows = table[0].find_all("tr")

# PART 1: Get all href to combine with base url later for cycling
hrefs_placeholder = get_hrefs(t_rows)

# TEST: Focusing on 1 card for easier coding
# hrefs = [hrefs_placeholder[10]]
hrefs = get_hrefs(t_rows)

# PART 2: Cycle through the links and extract card info

# PRACTICE TEST: Get card info of one card

all_cards = []
# Cycle through EACH card"s page for info
for i, href in enumerate(hrefs):
  # print(i)
  soup = get_soup(base_url + href)

  # Get card info, excluding effect
  div_ctnr = soup.find("div", class_="info-main")
  table = div_ctnr.find_all("table")
  t_rows = table[0].find_all("tr")
  # print(t_rows)

  # Cycle through rows get the first two td of each
  card_dict = {}

  # Info in wiki that needs to cleaned
  grade = None
  skill = None
  triggerType = None
  triggerEffect = None

  for row in t_rows:
    t_data_header = row.find_all("td")[0].text.lower().strip()
    t_data_info = row.find_all("td")[1].text.strip()
    # print(f"{t_data_header}: {t_data_info}")

    # Check if card info is in DESIRED_CARD_INFO, then add to dict if it is
    if any(desired_info in t_data_header for desired_info in DESIRED_CARD_INFO):

      requireCleaning = False

      # Handle "grade / skill" split
      if "grade" in t_data_header:
        if "/" in t_data_info:
          grade, skill = [info.strip() for info in t_data_info.split("/")]
          grade = int(grade.split()[1].strip())  # Extract grade number

          # Remove non-letter characters (e.g., "!!") from skill
          skill = re.sub(r"[^a-zA-Z\s]", "", skill)

          # print(f"skill: {skill}")
          card_dict["skill"] = skill
        else:
          grade = int(t_data_info.split()[1])  # Order card do not have skills
        
        # print(f"grade: {grade}")
        card_dict["grade"] = grade

        requireCleaning = True
      
      # Handle "trigger effect" split
      if "trigger" in t_data_header:
        triggerType = t_data_info.split("/")[0].strip()
        triggerEffect = int(t_data_info.split("+")[-1].strip())
        card_dict["triggerType"] = triggerType
        card_dict["triggerEffect"] = triggerEffect

        requireCleaning = True
        
        # print(f"trigger type: {triggerType}")
        # print(f"trigger effect: {triggerEffect}")
      
      # Handle "card type" key name
      if "card type" in t_data_header:
        card_dict["cardType"] = t_data_info
        requireCleaning = True

      if requireCleaning == False:
        card_dict[t_data_header] = t_data_info
        # print(f"{t_data_header}: {t_data_info}")
  
  all_cards.append(card_dict)
  
  # if i == 4:
  #   break

for i, card in enumerate(all_cards):
  print(i)
  for info in card:
    print(f"{info}: {card[info]}")