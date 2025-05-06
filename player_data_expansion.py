import numpy as np
import pandas as pd
import cloudscraper
import time

from bs4 import BeautifulSoup as bs

from web_scraping_SCRIPT import get_recent_fights


def get_all_expanded_player_fight_data() :
    """
    @return gets dataframe of web scraped basic data and the expanded player data
    """

    # initialize scraper
    scraper = cloudscraper.create_scraper()

    # get initial data from main basic scraper
    data = get_recent_fights()
    time.sleep(3)

    ######################################
    # preemptively include appending cols
    ######################################

    # create cols for WDL
    data['fighter1_record_wins'] = pd.NA
    data['fighter1_record_draws'] = pd.NA
    data['fighter1_record_losses'] = pd.NA
    data['fighter2_record_wins'] = pd.NA
    data['fighter2_record_draws'] = pd.NA
    data['fighter2_record_losses'] = pd.NA

    # create cols for heights
    data['fighter1_height_cm'] = pd.NA
    data['fighter2_height_cm'] = pd.NA

    # create cols for KO percentages
    data['fighter1_ko_percentage'] = pd.NA
    data['fighter2_ko_percentage'] = pd.NA

    # create cols for debut years
    data['fighter1_debut'] = pd.NA
    data['fighter2_debut'] = pd.NA
    

    ######################################
    # part 1 record data function
    ######################################
    def append_player_WDL_record(new_soup, index) :

        win_draw_loss = new_soup.find_all(class_='single-fight__record-content d-flex align-items-center justify-content-center w-100')
        
        fighter1_WDL_record = win_draw_loss[0].text.strip().split('-')
        fighter2_WDL_record = win_draw_loss[1].text.strip().split('-')

        data.at[index,'fighter1_record_wins'] = fighter1_WDL_record[0]
        data.at[index,'fighter1_record_losses'] = fighter1_WDL_record[1]
        data.at[index,'fighter1_record_draws'] = fighter1_WDL_record[2]

        data.at[index,'fighter2_record_wins'] = fighter2_WDL_record[0]
        data.at[index,'fighter2_record_losses'] = fighter2_WDL_record[1]
        data.at[index,'fighter2_record_draws'] = fighter2_WDL_record[2]



    ######################################
    # part 2: phys
    ######################################
    # create cols for heights
    def append_fighter_phys_bio(new_soup, index) : 
        soup_with_heights = new_soup.find_all(class_="stats-row__content text-center headings-text-color")

        # fighter 1
        fighter1_height = soup_with_heights[2]
        try : 
            fighter1_height_cm = int(fighter1_height.text.split()[3])
        except (IndexError, TypeError) :
            fighter1_height_cm = pd.NA
        

        # fighter 2
        fighter2_height = soup_with_heights[3]
        try : 
            fighter2_height_cm = int(fighter2_height.text.split()[3])
        except (IndexError, TypeError) :
            fighter2_height_cm = pd.NA

        # append height to cols
        data.at[index, 'fighter1_height_cm'] = fighter1_height_cm
        data.at[index, 'fighter2_height_cm'] = fighter2_height_cm



    ######################################
    # 3rd part: KO %
    ######################################
    def append_player_KO_perc(new_soup, index) : 
        soup_with_KO_perc = new_soup.find_all(class_="stats-row__content text-center headings-text-color")

        fighter1_ko_percentage = soup_with_KO_perc[14].text.split()[0]
        fighter2_ko_percentage = soup_with_KO_perc[15].text.split()[0]
        
        # set values for KO percentages
        data.at[index,'fighter1_ko_percentage'] = fighter1_ko_percentage
        data.at[index,'fighter2_ko_percentage'] = fighter2_ko_percentage

    ######################################
    # part 4: debut year
    ######################################
    def append_fighter_phys_bio(new_soup, index) : 

        # get the data
        class_data = soup.find_all(class_="stats-row__content text-center headings-text-color")

        # fighter 1
        fighter1_debut = class_data[20]
        try : 
            fighter1_debut = int(class_data[20].text.split()[0])
        except (IndexError, TypeError) :
            fighter1_debut = pd.NA
        

        # fighter 2
        fighter2_debut = class_data[21]
        try : 
            fighter2_debut = int(fighter2_debut = class_data[21].text.split()[0])
        except (IndexError, TypeError) :
            fighter2_debut = pd.NA

        # append height to cols
        data.at[index, 'fighter1_height_cm'] = fighter1_debut
        data.at[index, 'fighter2_height_cm'] = fighter2_debut

    ######################################
    # finally, append everything
    ######################################
    row_index = 0
    links = np.array(data['link'])

    for url in links :

        # scrape le website
        page = scraper.get(url)
        soup = bs(page.text, 'html.parser')

        # append certain values/metrics/statistics of players (probably use functions to do it repetitively, iterating by passing in row_index as an argument)
        append_player_WDL_record(soup, row_index)
        append_fighter_phys_bio(soup, row_index)
        append_player_KO_perc(soup, row_index)

        seconds = np.random.randint(1,3)
        time.sleep(seconds)

        row_index += 1
    

    scraper.close()

    return data