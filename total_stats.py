import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = "https://www.nba.com/stats"

request = requests.get(URL)

soup = BeautifulSoup(request.content, "html.parser")

categories = []
start_scrap = soup.find_all("h2", class_="LeaderBoardCard_lbcTitleLink__MXurG")
for scrap in start_scrap:
    categories.append(scrap.text)
categories.pop(8)

players = []
players_scrap = soup.select(".LeaderBoardPlayerCard_lbpcTableLink__MDNgL")
for player in players_scrap:
    player.find_all("table", "a", class_="Anchor_anchor__cSc3P LeaderBoardPlayerCard_lbpcTableLink__MDNgL")
    players.append(player.text)
clear_data = [name for name in players if not name.isdigit()]
best_players = clear_data[-27:]

value = 3
best_player_in_category = []
temp_list = []
for i in best_players:
    value -= 1
    temp_list.append(i)
    if value == 0:
        best_player_in_category.append(temp_list)
        temp_list = []
        value = 3

data_to_write = {categories[i]: best_player_in_category[i] for i in range(len(categories))}

file = pd.DataFrame.from_dict(data_to_write)
file.index += 1


file.to_csv("best_in_categories.csv")
