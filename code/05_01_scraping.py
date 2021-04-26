from bs4 import BeautifulSoup as Soup
import pandas as pd
import requests
from pandas import DataFrame

bal_response = requests.get('https://www.baseball-almanac.com/opening_day/odschedule.php?t=BAL')

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
    team_response = requests.get(f'https://www.baseball-almanac.com/opening_day/odschedule.php?t={team}')
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

mlb_response = requests.get('https://www.baseball-almanac.com/opening_day/opening_day.shtml')
mlb_soup = Soup(mlb_response.text)

all_link_tags = mlb_soup.find_all('a')
all_opening_day_link_tags = [x for x in all_link_tags if
                             str(x.string).endswith('Opening Day Games')]

teams = [str(x.get('href'))[-3:] for x in all_opening_day_link_tags]

df = pd.concat([scrape_opening_day_single_team(team) for team in teams[:3]])

df_mil = parse_opening_day_by_team('MIL')

ffc_response = requests.get('https://fantasyfootballcalculator.com/adp/ppr/12-team/all/2017')

print(ffc_response.text)

adp_soup = Soup(ffc_response.text)

# adp_soup is a nested tag, so call find_all on it

tables = adp_soup.find_all('table')

# find_all always returns a list, even if there's only one element, which is
# the case here
len(tables)

# get the adp table out of it
adp_table = tables[0]

# adp_table another nested tag, so call find_all again
rows = adp_table.find_all('tr')

# this is a header row
rows[0]

# data rows
first_data_row = rows[1]
first_data_row

# get columns from first_data_row
first_data_row.find_all('td')

# comprehension to get raw data out -- each x is simple tag
[str(x.string) for x in first_data_row.find_all('td')]

# put it in a function
def parse_row(row):
    """
    Take in a tr tag and get the data out of it in the form of a list of
    strings.
    """
    return [str(x.string) for x in row.find_all('td')]

# call function
list_of_parsed_rows = [parse_row(row) for row in rows[1:]]

# put it in a dataframe
df = DataFrame(list_of_parsed_rows)
df.head()

# clean up formatting
df.columns = ['ovr', 'pick', 'name', 'pos', 'team', 'adp', 'std_dev',
              'high', 'low', 'drafted', 'graph']

float_cols =['adp', 'std_dev']
int_cols =['ovr', 'drafted']

df[float_cols] = df[float_cols].astype(float)
df[int_cols] = df[int_cols].astype(int)

df.drop('graph', axis=1, inplace=True)

# done
df.head()
