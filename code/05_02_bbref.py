from bs4 import BeautifulSoup as Soup
import pandas as pd
import requests
from pandas import DataFrame

# NEW - this doesn't work as of 2/2022, see a 403 error
bal_response = requests.get('https://www.baseball-almanac.com/opening_day/odschedule.php?t=BAL')
print(bal_response.text)

# to fix: need to add a user agent to headers
# see: https://stackoverflow.com/questions/38489386/python-requests-403-forbidden

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

bal_response = requests.get('https://www.baseball-almanac.com/opening_day/odschedule.php?t=BAL', headers=HEADERS)

print(bal_response.text)

bal_soup = Soup(bal_response.text)

tables = bal_soup.find_all('table')
len(tables)

bal_table = tables[0]
rows = bal_table.find_all('tr')
rows[0]
rows[1]

first_data_row = rows[2]
first_data_row

first_data_row.find_all('td')
[str(x.string) for x in first_data_row.find_all('td')]

def parse_row(row):
    """
    Take in a tr tag and get the data out of it in the form of a list of
    strings.
    """
    return [str(x.string) for x in row.find_all('td')]

list_of_parsed_rows = [parse_row(row) for row in rows[2:-2]]

df = DataFrame(list_of_parsed_rows)

df.columns = parse_row(rows[1])

def scrape_opening_day_single_team(team):
    team_response = requests.get(f'https://www.baseball-almanac.com/opening_day/odschedule.php?t={team}', headers=HEADERS)
    team_soup = Soup(team_response.text)

    tables = team_soup.find_all('table')

    team_table = tables[0]
    rows = team_table.find_all('tr')

    list_of_parsed_rows = [parse_row(row) for row in rows[2:-2]]
    df = DataFrame(list_of_parsed_rows)
    df.columns = parse_row(rows[1])

    # let's add in team as a column
    df['team'] = team

    return df

df_mil = scrape_opening_day_single_team('MIL')
df_mil.head()

## now get list of teams

mlb_response = requests.get('https://www.baseball-almanac.com/opening_day/opening_day.shtml', headers=HEADERS)
mlb_soup = Soup(mlb_response.text)

all_link_tags = mlb_soup.find_all('a')
all_opening_day_link_tags = [x for x in all_link_tags if
                             str(x.string).endswith('Opening Day Games')]

teams = [str(x.get('href'))[-3:] for x in all_opening_day_link_tags]

df = pd.concat([scrape_opening_day_single_team(team) for team in teams[:3]])

