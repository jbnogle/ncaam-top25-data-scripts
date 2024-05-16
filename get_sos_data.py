import requests, pandas, os
from bs4 import BeautifulSoup

# container for rows (arrays) of data to be converted to csv
final_sos_arr = []

URL = "https://www.warrennolan.com/basketball/2024/sos-rpi"
page = requests.get(URL)

# capture entire HTML content of web page
soup = BeautifulSoup(page.content, "html.parser")

# find 'table' element within HTML content that holds the data of interest
html_table = soup.find("table", class_="normal-grid alternating-rows stats-table")

# find 'thead' element for table headers
table_headers = html_table.find("thead").find_all("th")

# array to be filled with headers (column names)
headers = []
for header in table_headers:
    headers.append(header.text)

# add the headers array as first item (row of data) in final array
final_sos_arr.append(headers)

# find 'tbody' element containing the table data (excluding headers)
table_rows =  html_table.find("tbody").find_all("tr")

# iterate through 'tr' elements (rows) in the 'tbody' (table)
for row in table_rows:
    row_data = []
    # find 'a' element with Team name data (nested inside first 'td' element)
    team = row.find("a", class_="blue-black").text
    row_data.append(team)

    # other fields data are directly in 'td' elements
    other_fields = row.find_all("td")
    for field in other_fields[1:]:  # skip first element since we already scraped team
        row_data.append(field.text)

    final_sos_arr.append(row_data)

df = pandas.DataFrame(final_sos_arr)
headers = df.iloc[0]
new_df  = pandas.DataFrame(df.values[1:], columns=headers)

if os.path.isfile('sos_data_scraped.csv'):
    os.remove('sos_data_scraped.csv')

new_df.to_csv('sos_data_scraped.csv', index=False, header=True)