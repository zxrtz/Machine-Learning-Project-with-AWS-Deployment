from bs4 import BeautifulSoup as bs
import requests
import cloudscraper

import pandas as pd


def get_recent_fights() :
    # grab in the soup
    scraper = cloudscraper.create_scraper()

    url = "https://box.live/fight-results/"

    page = scraper.get(url)

    soup = bs(page.text, 'html.parser')


    # find table
    recent_fights_table = soup.find('table')

    # get columns
    recent_fights_cols = recent_fights_table.find_all('th')
    recent_fights_cols = [col.text.strip() for col in recent_fights_cols]

    # Deduplicate column names
    recent_fights_cols = pd.Series(recent_fights_cols).apply(
        lambda x: x if recent_fights_cols.count(x) == 1 else f"{x}.{recent_fights_cols[:recent_fights_cols.index(x)].count(x) + 1}"
    ).tolist()

    # create new df to append data to
    recent_fights_df = pd.DataFrame(columns = recent_fights_cols)
    recent_fights_df


    # get all column row data
    column_rows = recent_fights_table.find_all('tr')


    # append
    for row in column_rows[1:] :
        row_data = row.find_all('td') # get all individual rows using td

        # get individual row to be appended
        individual_row_data = [data.text.strip() for data in row_data]
        print(individual_row_data)

        if individual_row_data[len(individual_row_data) - 1] == '' :
            individual_row_data[len(individual_row_data) - 1] = 'NaN'

        # append
        length = len(recent_fights_df)
        recent_fights_df.loc[length] = individual_row_data
    

    # make sure to deal with duplicate column names
    recent_fights_df.columns = ['Date', 'Fighter 1', 'Result Fighter 1', 'Method / Round Fighter 1',
       'Fighter 2', 'Result Fighter 2', 'Method / Round Fighter 2', 'Venue', 'Undercard fights']
    
    print(recent_fights_df.columns)
    
    return recent_fights_df
