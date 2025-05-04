from web_scraping_SCRIPT import get_recent_fights
from player_data_expansion import get_all_expanded_player_fight_data

import pandas as pd
import numpy as np
from pathlib import Path
import io

import os

def expanded_player_fight_data_appender() :
    new_data = get_all_expanded_player_fight_data()

    # get current path of this file, set it to path
    curr_dir = os.path.dirname(os.path.abspath(''))

    # csv file path - by appending file name and current directory
    my_file_path = Path(curr_dir + "\\" + "fight_data.csv")

    # change file path later in AWS
    if not my_file_path.exists():
        new_data.to_csv(
            "C:/Users/Dylan/Desktop/ROAD TO DATASCI/PYTHON/PYTHON PERSONAL PROJECTS/END-TO-END Boxing Predictions Project/Machine-Learning-Project-with-AWS-Deployment/fight_data.csv",
            index=False
        )
    else:
        old_df = pd.read_csv(
            "C:/Users/Dylan/Desktop/ROAD TO DATASCI/PYTHON/PYTHON PERSONAL PROJECTS/END-TO-END Boxing Predictions Project/Machine-Learning-Project-with-AWS-Deployment/fight_data.csv"
        )
        # Concatenate and reset index to avoid duplicate index issues
        appended_df = pd.concat([old_df, new_data], axis=0)

        # Drop duplicates and reset index
        appended_df = appended_df.drop_duplicates(keep='first')

        # Save the updated DataFrame
        appended_df.to_csv(
            "C:/Users/Dylan/Desktop/ROAD TO DATASCI/PYTHON/PYTHON PERSONAL PROJECTS/END-TO-END Boxing Predictions Project/Machine-Learning-Project-with-AWS-Deployment/fight_data.csv",
            index=False
        )
# test
expanded_player_fight_data_appender()

