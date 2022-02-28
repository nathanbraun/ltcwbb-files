from bs4 import BeautifulSoup as Soup

table_html = """
<html>
    <table>
      <tr>
       <th>Name</th>
       <th>Team</th>
       <th>Lg</th>
       <th>HR</th>
      </tr>
      <tr>
       <td>Jose Abreu</td>
       <td>CHA</td>
       <td>AL</td>
       <td>22</td>
      </tr>
      <tr>
       <td>Ronald Acuna</td>
       <td>ATL</td>
       <td>NL</td>
       <td>26</td>
      </tr>
    </table>
<html>
"""

html_soup = Soup(table_html)

tr_tag = html_soup.find('tr')
tr_tag
type(tr_tag)

table_tag = html_soup.find('table')
table_tag
type(table_tag)

td_tag = html_soup.find('td')
td_tag
type(td_tag)

td_tag
td_tag.string
str(td_tag.string)

tr_tag.find_all('th')

[str(x.string) for x in tr_tag.find_all('th')]

all_td_tags = table_tag.find_all('td')
all_td_tags

all_rows = table_tag.find_all('tr')
first_data_row = all_rows[1]  # 0 is header
first_data_row.find_all('td')

all_td_and_th_tags = table_tag.find_all(('td', 'th'))
all_td_and_th_tags

[str(x.string) for x in all_td_tags]

all_rows = table_tag.find_all('tr')
list_of_td_lists = [x.find_all('td') for x in all_rows[1:]]
list_of_td_lists

